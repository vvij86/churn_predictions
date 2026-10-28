/*
Feature Name: partial_rollover_behaviour_12m_group
Feature Group: Partial Rollover / Withdrawal Behaviour

Business Meaning:
    Captures partial external rollover / withdrawal behaviour that occurred
    before the AsOfDate.

    Full external rollover features are intentionally excluded because they
    may occur very close to actual churn / account exit and can introduce
    target leakage.

Source Table:
    edgeSource.accountRolloverPayment

Included:
    Partial rollover / withdrawal activity only

Excluded:
    Full external rollover
    Internal transfers
    Post-AsOfDate activity

Feature Window:
    Previous 12 months from AsOfDate

Recent Window:
    Previous 90 days from AsOfDate

Point-in-Time Rule:
    processedDate must be between FeatureStartDate and AsOfDate.
*/

DECLARE @AsOfDate DATE = '2024-03-31';

DECLARE @FeatureStartDate DATE =
    DATEADD(DAY, 1, DATEADD(MONTH, -12, @AsOfDate));

DECLARE @Recent90Start DATE =
    DATEADD(DAY, -89, @AsOfDate);


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

partial_rollover_fact AS
(
    SELECT
        arp.accountID,

        CAST(arp.processedDate AS DATE) AS processed_date,

        CAST(arp.paymentAmount AS DECIMAL(18,2)) AS payment_amount

    FROM edgeSource.accountRolloverPayment arp

    INNER JOIN eligible_accounts ea
        ON ea.accountID = arp.accountID

    WHERE arp.processedDate >= @FeatureStartDate
      AND arp.processedDate <= @AsOfDate

      /* Partial rollover / withdrawal only */
      AND arp.paymentType IN
      (
          'Rollover to External Fund',
          'Other',
          'Rollover/Transfer to Annuity'
      )

      AND arp.partialWithdrawalFlag = 1

      /* Explicitly exclude internal transfers */
      AND COALESCE(arp.internalTransferFlag, 0) = 0

      /* Keep genuine payment activity only */
      AND arp.paymentAmount <> 0
),

partial_rollover_summary AS
(
    SELECT
        pr.accountID,

        /* Number of partial rollovers during previous 12 months */
        COUNT(*) AS partial_rollover_count_12m,


        /* Total amount partially rolled out during previous 12 months */
        SUM(pr.payment_amount)
            AS partial_rollover_amount_12m,


        /* How recently the member made a partial rollover */
        DATEDIFF
        (
            DAY,
            MAX(pr.processed_date),
            @AsOfDate
        ) AS days_since_last_partial_rollover,


        /* Number of partial rollovers during recent 90 days */
        SUM
        (
            CASE
                WHEN pr.processed_date >= @Recent90Start
                THEN 1
                ELSE 0
            END
        ) AS recent_partial_rollover_count_90d,


        /* Amount partially rolled out during recent 90 days */
        SUM
        (
            CASE
                WHEN pr.processed_date >= @Recent90Start
                THEN pr.payment_amount
                ELSE 0
            END
        ) AS recent_partial_rollover_amount_90d

    FROM partial_rollover_fact pr

    GROUP BY pr.accountID
)

SELECT
    accountID,

    partial_rollover_count_12m,

    partial_rollover_amount_12m,

    days_since_last_partial_rollover,

    recent_partial_rollover_count_90d,

    recent_partial_rollover_amount_90d

FROM partial_rollover_summary

ORDER BY accountID;
