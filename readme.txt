/*
Feature Name: account_net_money_flow_12m_group
Feature Group: Net Money Flow Behaviour

Business Meaning:
    Measures the overall movement of money into and out of an account
    during the 12 months before the AsOfDate.

    It also compares the most recent 90 days with the previous 90 days
    to identify whether net cash flow is declining.

Source Table:
    edgeSource.accountNetMoneyFlow

Point-in-Time Rule:
    Only records with:
        referenceDate >= FeatureStartDate
        referenceDate <= AsOfDate
    are used.

Internal Transfers:
    Excluded because they are movements within the fund rather than
    genuine external inflow/outflow behaviour.

Final Features:
    net_flow_12m
    total_positive_flow_12m
    total_negative_flow_12m
    negative_net_flow_months_12m
    avg_active_monthly_net_flow_12m
    recent_net_flow_90d
    prior_net_flow_90d
    net_flow_decline_flag
    days_since_last_negative_flow
    cashflow_active_months_12m
*/


DECLARE @AsOfDate DATE = '2024-03-31';

DECLARE @FeatureStartDate DATE =
    DATEADD(DAY, 1, DATEADD(MONTH, -12, @AsOfDate));

DECLARE @Recent90Start DATE =
    DATEADD(DAY, -89, @AsOfDate);

DECLARE @Prior90Start DATE =
    DATEADD(DAY, -179, @AsOfDate);

DECLARE @Prior90End DATE =
    DATEADD(DAY, -90, @AsOfDate);


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

net_flow_fact AS
(
    SELECT
        n.accountID,

        CAST(n.referenceDate AS DATE) AS event_date,

        /*
        Standardise the direction:

        cashFlowSign =  1 -> positive inflow
        cashFlowSign = -1 -> negative outflow
        */
        CAST
        (
            CASE
                WHEN COALESCE(n.cashFlowSign, 0) = -1
                    THEN -1 * ABS(CAST(n.amount AS DECIMAL(18,2)))

                WHEN COALESCE(n.cashFlowSign, 0) = 1
                    THEN ABS(CAST(n.amount AS DECIMAL(18,2)))

                ELSE CAST(n.amount AS DECIMAL(18,2))
            END
            AS DECIMAL(18,2)
        ) AS net_amount,

        n.cashflowtype,
        n.cashflowDescription

    FROM edgeSource.accountNetMoneyFlow n

    INNER JOIN eligible_accounts ea
        ON ea.accountID = n.accountID

    WHERE n.referenceDate >= @FeatureStartDate
      AND n.referenceDate <= @AsOfDate

      -- Ignore zero-value records
      AND COALESCE(n.amount, 0) <> 0

      -- Exclude internal transfers
      AND COALESCE(n.internalTransferFlag, 0) = 0
),

monthly_net_flow AS
(
    SELECT
        nf.accountID,

        DATEFROMPARTS
        (
            YEAR(nf.event_date),
            MONTH(nf.event_date),
            1
        ) AS flow_month,

        SUM(nf.net_amount) AS monthly_net_flow

    FROM net_flow_fact nf

    GROUP BY
        nf.accountID,
        DATEFROMPARTS
        (
            YEAR(nf.event_date),
            MONTH(nf.event_date),
            1
        )
),

flow_summary AS
(
    SELECT
        nf.accountID,

        /* Overall 12-month net flow */
        SUM(nf.net_amount)
            AS net_flow_12m,


        /* Total money coming in */
        SUM
        (
            CASE
                WHEN nf.net_amount > 0
                    THEN nf.net_amount
                ELSE 0
            END
        ) AS total_positive_flow_12m,


        /* Total money going out - stored as positive amount */
        ABS
        (
            SUM
            (
                CASE
                    WHEN nf.net_amount < 0
                        THEN nf.net_amount
                    ELSE 0
                END
            )
        ) AS total_negative_flow_12m,


        /* Most recent 90 days */
        SUM
        (
            CASE
                WHEN nf.event_date >= @Recent90Start
                 AND nf.event_date <= @AsOfDate
                    THEN nf.net_amount
                ELSE 0
            END
        ) AS recent_net_flow_90d,


        /* Previous 90 days */
        SUM
        (
            CASE
                WHEN nf.event_date >= @Prior90Start
                 AND nf.event_date <= @Prior90End
                    THEN nf.net_amount
                ELSE 0
            END
        ) AS prior_net_flow_90d,


        /*
        Has recent net flow decreased compared with
        the immediately preceding 90 days?
        */
        CASE
            WHEN
                SUM
                (
                    CASE
                        WHEN nf.event_date >= @Recent90Start
                         AND nf.event_date <= @AsOfDate
                            THEN nf.net_amount
                        ELSE 0
                    END
                )
                <
                SUM
                (
                    CASE
                        WHEN nf.event_date >= @Prior90Start
                         AND nf.event_date <= @Prior90End
                            THEN nf.net_amount
                        ELSE 0
                    END
                )
            THEN 1
            ELSE 0
        END AS net_flow_decline_flag,


        /*
        Exact recency based on the actual negative-flow transaction date.
        */
        DATEDIFF
        (
            DAY,
            MAX
            (
                CASE
                    WHEN nf.net_amount < 0
                        THEN nf.event_date
                END
            ),
            @AsOfDate
        ) AS days_since_last_negative_flow

    FROM net_flow_fact nf

    GROUP BY nf.accountID
),

monthly_summary AS
(
    SELECT
        mnf.accountID,

        /*
        Number of months where the overall monthly
        net flow was negative.
        */
        COUNT
        (
            DISTINCT CASE
                WHEN mnf.monthly_net_flow < 0
                    THEN mnf.flow_month
            END
        ) AS negative_net_flow_months_12m,


        /*
        Average net flow across months with activity.
        */
        AVG
        (
            CAST(mnf.monthly_net_flow AS DECIMAL(18,2))
        ) AS avg_active_monthly_net_flow_12m,


        /*
        Number of months with cash-flow activity.
        */
        COUNT(DISTINCT mnf.flow_month)
            AS cashflow_active_months_12m

    FROM monthly_net_flow mnf

    GROUP BY mnf.accountID
)

SELECT
    ea.accountID,

    COALESCE(fs.net_flow_12m, 0)
        AS net_flow_12m,

    COALESCE(fs.total_positive_flow_12m, 0)
        AS total_positive_flow_12m,

    COALESCE(fs.total_negative_flow_12m, 0)
        AS total_negative_flow_12m,

    COALESCE(ms.negative_net_flow_months_12m, 0)
        AS negative_net_flow_months_12m,

    COALESCE(ms.avg_active_monthly_net_flow_12m, 0)
        AS avg_active_monthly_net_flow_12m,

    COALESCE(fs.recent_net_flow_90d, 0)
        AS recent_net_flow_90d,

    COALESCE(fs.prior_net_flow_90d, 0)
        AS prior_net_flow_90d,

    COALESCE(fs.net_flow_decline_flag, 0)
        AS net_flow_decline_flag,

    fs.days_since_last_negative_flow,

    COALESCE(ms.cashflow_active_months_12m, 0)
        AS cashflow_active_months_12m

FROM eligible_accounts ea

LEFT JOIN flow_summary fs
    ON fs.accountID = ea.accountID

LEFT JOIN monthly_summary ms
    ON ms.accountID = ea.accountID

ORDER BY ea.accountID;
