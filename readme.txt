/*
Feature Name: third_party_authority_asof_group
Feature Group: Third Party Authority

Business Meaning:
    Captures whether an account has an active third-party authority
    as at the selected AsOfDate, including key authority categories.

Source Table:
    edgeSource.thirdPartyAuthority

Point-in-Time Rule:
    An authority is active only when:
        dateAuthorityRequested <= AsOfDate
    AND
        terminationDate IS NULL
        OR terminationDate > AsOfDate

Notes:
    - Future request dates are naturally excluded.
    - Far-future termination dates are treated as still active.
    - Raw adviser/company names and external IDs are not used as ML features.

Final ML Features:
    active_third_party_authority_flag_asof
    active_adviser_authority_flag_asof
    active_family_or_legal_authority_flag_asof
    active_poa_authority_flag_asof
    active_third_party_authority_count_asof
*/

DECLARE @AsOfDate DATE = '2024-03-31';


WITH eligible_accounts AS
(
    SELECT DISTINCT
        a.accountID
    FROM edgeSource.accountSummary a
    WHERE a.fundJoinDate <= @AsOfDate
      AND a.databaseCode IN
      (
          'MASTA',
          'MASTP',
          'MASTR',
          'MASTS',
          'MASTM',
          'MTAPD',
          'ST000',
          'MASTR_AP'
      )
      AND
      (
          a.exitDateRecorded IS NULL
          OR a.exitDateRecorded > @AsOfDate
      )
      AND
      (
          a.dateOfDeath IS NULL
          OR a.dateOfDeath > @AsOfDate
      )
      AND
      (
          a.deathIndicatorFlag IS NULL
          OR a.deathIndicatorFlag = 0
      )
),

active_authority AS
(
    SELECT
        tpa.accountID,
        tpa.thirdPartyAuthorityType

    FROM edgeSource.thirdPartyAuthority tpa

    INNER JOIN eligible_accounts ea
        ON ea.accountID = tpa.accountID

    WHERE tpa.dateAuthorityRequested <= @AsOfDate
      AND
      (
          tpa.terminationDate IS NULL
          OR CAST(tpa.terminationDate AS DATE) > @AsOfDate
      )
),

authority_summary AS
(
    SELECT
        accountID,

        COUNT(*) AS active_third_party_authority_count_asof,

        1 AS active_third_party_authority_flag_asof,

        MAX
        (
            CASE
                WHEN thirdPartyAuthorityType = 'Adviser'
                THEN 1
                ELSE 0
            END
        ) AS active_adviser_authority_flag_asof,

        MAX
        (
            CASE
                WHEN thirdPartyAuthorityType IN
                (
                    'Family Representative',
                    'Legal Representative'
                )
                THEN 1
                ELSE 0
            END
        ) AS active_family_or_legal_authority_flag_asof,

        MAX
        (
            CASE
                WHEN thirdPartyAuthorityType = 'PoA'
                THEN 1
                ELSE 0
            END
        ) AS active_poa_authority_flag_asof

    FROM active_authority

    GROUP BY accountID
)

SELECT
    ea.accountID,

    COALESCE(
        aus.active_third_party_authority_flag_asof,
        0
    ) AS active_third_party_authority_flag_asof,

    COALESCE(
        aus.active_adviser_authority_flag_asof,
        0
    ) AS active_adviser_authority_flag_asof,

    COALESCE(
        aus.active_family_or_legal_authority_flag_asof,
        0
    ) AS active_family_or_legal_authority_flag_asof,

    COALESCE(
        aus.active_poa_authority_flag_asof,
        0
    ) AS active_poa_authority_flag_asof,

    COALESCE(
        aus.active_third_party_authority_count_asof,
        0
    ) AS active_third_party_authority_count_asof

FROM eligible_accounts ea

LEFT JOIN authority_summary aus
    ON aus.accountID = ea.accountID

ORDER BY ea.accountID;
