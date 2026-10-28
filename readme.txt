/*
Feature Name: investment_position_asof_group
Feature Group: Investment Behaviour / Position

Business Meaning:
    Captures the member's latest known investment position as at AsOfDate.

Business Confirmation:
    - value = value of the investment / stock
    - use the newest record based on MAX(investmentDate)

Source Table:
    edgeSource.accountInvestments

Important:
    accountInvestments appears to contain periodic investment snapshots.
    Therefore snapshot row counts are NOT treated as investment-change events.

Point-in-Time Rule:
    Only investment records with investmentDate <= AsOfDate are used.

Final ML Features:
    investment_option_count_asof
    total_investment_value_asof
    direct_investment_flag
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

ranked_investments AS
(
    SELECT
        ai.accountID,
        ai.investmentCode,
        CAST(ai.investmentDate AS DATE) AS investmentDate,
        CAST(ai.value AS DECIMAL(18,2)) AS investment_value,
        ai.directInvestmentFlag,

        ROW_NUMBER() OVER
        (
            PARTITION BY
                ai.accountID,
                ai.investmentCode

            ORDER BY
                ai.investmentDate DESC
        ) AS rn

    FROM edgeSource.accountInvestments ai

    INNER JOIN eligible_accounts ea
        ON ea.accountID = ai.accountID

    WHERE ai.investmentDate <= @AsOfDate
      AND ai.investmentCode IS NOT NULL
),

latest_investments AS
(
    SELECT
        accountID,
        investmentCode,
        investment_value,
        directInvestmentFlag

    FROM ranked_investments

    WHERE rn = 1
)

SELECT
    accountID,

    /* Number of distinct investment options held as at AsOfDate */
    COUNT(DISTINCT investmentCode)
        AS investment_option_count_asof,


    /* Total latest investment value across all investment options */
    SUM
    (
        COALESCE(investment_value, 0)
    ) AS total_investment_value_asof,


    /* Whether account has any direct-investment exposure */
    MAX
    (
        CASE
            WHEN COALESCE(directInvestmentFlag, 0) = 1
            THEN 1
            ELSE 0
        END
    ) AS direct_investment_flag

FROM latest_investments

GROUP BY accountID

ORDER BY accountID;
