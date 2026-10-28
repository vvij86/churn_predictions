/*
Feature Name: insurance_cover_asof_group
Feature Group: Insurance Behaviour / Cover Position

Business Meaning:
    Captures the member's active insurance cover as at the selected AsOfDate.

    Insurance is grouped into the three clean risk-event categories available
    in AccountInsuranceCurrent:
        - Death
        - TPD
        - IP

Source Table:
    edgeSource.AccountInsuranceCurrent

Point-in-Time Rule:
    A cover is considered active only when:
        effectiveDateFrom <= AsOfDate
    AND
        effectiveDateTo IS NULL
        OR effectiveDateTo > AsOfDate

Important:
    coverDescription contains many detailed variants, therefore it is not used
    directly as an ML categorical feature here.

    MAX(coverAmount) is used within each riskEvent as a conservative approach,
    rather than summing potentially different insurance cover components.

Final ML Features:
    has_death_cover_asof
    death_cover_amount_asof

    has_tpd_cover_asof
    tpd_cover_amount_asof

    has_ip_cover_asof
    ip_cover_amount_asof

    insurance_cover_type_count_asof
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

active_insurance AS
(
    SELECT
        aic.accountID,
        aic.riskEvent,
        CAST(aic.coverAmount AS DECIMAL(18,2)) AS cover_amount

    FROM edgeSource.AccountInsuranceCurrent aic

    INNER JOIN eligible_accounts ea
        ON ea.accountID = aic.accountID

    WHERE aic.effectiveDateFrom <= @AsOfDate

      AND
      (
          aic.effectiveDateTo IS NULL
          OR aic.effectiveDateTo > @AsOfDate
      )

      AND aic.riskEvent IN
      (
          'Death',
          'TPD',
          'IP'
      )
),

insurance_summary AS
(
    SELECT
        accountID,

        /* Death cover */
        MAX
        (
            CASE
                WHEN riskEvent = 'Death'
                THEN 1
                ELSE 0
            END
        ) AS has_death_cover_asof,

        MAX
        (
            CASE
                WHEN riskEvent = 'Death'
                THEN cover_amount
            END
        ) AS death_cover_amount_asof,


        /* TPD cover */
        MAX
        (
            CASE
                WHEN riskEvent = 'TPD'
                THEN 1
                ELSE 0
            END
        ) AS has_tpd_cover_asof,

        MAX
        (
            CASE
                WHEN riskEvent = 'TPD'
                THEN cover_amount
            END
        ) AS tpd_cover_amount_asof,


        /* Income Protection cover */
        MAX
        (
            CASE
                WHEN riskEvent = 'IP'
                THEN 1
                ELSE 0
            END
        ) AS has_ip_cover_asof,

        MAX
        (
            CASE
                WHEN riskEvent = 'IP'
                THEN cover_amount
            END
        ) AS ip_cover_amount_asof

    FROM active_insurance

    GROUP BY accountID
)

SELECT
    ea.accountID,

    COALESCE(ins.has_death_cover_asof, 0)
        AS has_death_cover_asof,

    COALESCE(ins.death_cover_amount_asof, 0)
        AS death_cover_amount_asof,

    COALESCE(ins.has_tpd_cover_asof, 0)
        AS has_tpd_cover_asof,

    COALESCE(ins.tpd_cover_amount_asof, 0)
        AS tpd_cover_amount_asof,

    COALESCE(ins.has_ip_cover_asof, 0)
        AS has_ip_cover_asof,

    COALESCE(ins.ip_cover_amount_asof, 0)
        AS ip_cover_amount_asof,


    /* Number of insurance categories active as at AsOfDate */
    (
        COALESCE(ins.has_death_cover_asof, 0)
        +
        COALESCE(ins.has_tpd_cover_asof, 0)
        +
        COALESCE(ins.has_ip_cover_asof, 0)
    ) AS insurance_cover_type_count_asof

FROM eligible_accounts ea

LEFT JOIN insurance_summary ins
    ON ins.accountID = ea.accountID

ORDER BY ea.accountID;
