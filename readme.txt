/*
Feature Name: contribution_behaviour_12m_group
Feature Group: Contribution Behaviour

Business Meaning:
    Captures contribution frequency, amount, recency, recent change,
    cessation and contribution-type-specific behaviour.

Source Table:
    edgeSource.accountMoneyInflow

Contribution Types Included:
    Employer SG
    Salary Sacrifice
    Post Tax Voluntary

Excluded:
    Internal transfers
    Rollovers in
    Adjustments
    Insurance claim proceeds
    Other unrelated inflows

Feature Window:
    Previous 12 months from AsOfDate

Recent Comparison:
    Recent 90 days vs previous 90 days

Point-in-Time Rule:
    inflowDateReceived must be <= AsOfDate.

Note:
    No 30-day contribution window is added initially because contributions
    may be monthly/fortnightly and a 30-day window can be unnecessarily noisy.
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

contribution_fact AS
(
    SELECT
        ami.accountID,

        CAST(ami.inflowDateReceived AS DATE) AS event_date,

        CAST(ami.inflowAmount AS DECIMAL(18,2)) AS amount,

        CASE

            /* Explicit exclusions */

            WHEN ami.inflowInternalTransferFlag = 1
                THEN 'EXCLUDE'

            WHEN ami.inflowRolloverType IN ('I', 'R')
                THEN 'EXCLUDE'

            WHEN ami.inflowDescription = 'Rollovers-In'
             AND ami.inflowSourceDescription LIKE '%ADJUSTMENT%'
                THEN 'EXCLUDE'

            WHEN ami.inflowDescription = 'Rollovers-In'
             AND ami.inflowSourceDescription LIKE '%Transfer%'
                THEN 'EXCLUDE'


            /* Contribution mappings */

            WHEN ami.inflowDescription IN
            (
                'Employer',
                'Employer Additional Conts'
            )
                THEN 'Employer SG'

            WHEN ami.inflowDescription = 'Voluntary Member Salary Sacrifice'
                THEN 'Salary Sacrifice'

            WHEN ami.inflowDescription = 'Member Voluntary'
                THEN 'Post Tax Voluntary'

            ELSE 'EXCLUDE'

        END AS contribution_type

    FROM edgeSource.accountMoneyInflow ami

    INNER JOIN eligible_accounts ea
        ON ea.accountID = ami.accountID

    WHERE ami.inflowDateReceived >= @FeatureStartDate
      AND ami.inflowDateReceived <= @AsOfDate
      AND ami.inflowAmount > 0
),

valid_contributions AS
(
    SELECT
        accountID,
        event_date,
        amount,
        contribution_type

    FROM contribution_fact

    WHERE contribution_type IN
    (
        'Employer SG',
        'Salary Sacrifice',
        'Post Tax Voluntary'
    )
),

contribution_summary AS
(
    SELECT
        vc.accountID,


        /* =====================================================
           Overall 12-month contribution behaviour
           ===================================================== */

        COUNT(*)
            AS contribution_count_12m,

        SUM(vc.amount)
            AS contribution_amount_12m,

        AVG(vc.amount)
            AS avg_contribution_transaction_amount_12m,

        COUNT
        (
            DISTINCT DATEFROMPARTS
            (
                YEAR(vc.event_date),
                MONTH(vc.event_date),
                1
            )
        ) AS contribution_active_months_12m,

        DATEDIFF
        (
            DAY,
            MAX(vc.event_date),
            @AsOfDate
        ) AS days_since_last_contribution,


        /* =====================================================
           Recent 90 days
           ===================================================== */

        SUM
        (
            CASE
                WHEN vc.event_date >= @Recent90Start
                THEN vc.amount
                ELSE 0
            END
        ) AS recent_contribution_amount_90d,

        COUNT
        (
            CASE
                WHEN vc.event_date >= @Recent90Start
                THEN 1
            END
        ) AS recent_contribution_count_90d,


        /* =====================================================
           Previous 90 days
           ===================================================== */

        SUM
        (
            CASE
                WHEN vc.event_date >= @Prior90Start
                 AND vc.event_date <= @Prior90End
                THEN vc.amount
                ELSE 0
            END
        ) AS prior_contribution_amount_90d,

        COUNT
        (
            CASE
                WHEN vc.event_date >= @Prior90Start
                 AND vc.event_date <= @Prior90End
                THEN 1
            END
        ) AS prior_contribution_count_90d,


        /* =====================================================
           Employer SG
           ===================================================== */

        SUM
        (
            CASE
                WHEN vc.contribution_type = 'Employer SG'
                THEN vc.amount
                ELSE 0
            END
        ) AS employer_sg_amount_12m,

        SUM
        (
            CASE
                WHEN vc.contribution_type = 'Employer SG'
                 AND vc.event_date >= @Recent90Start
                THEN vc.amount
                ELSE 0
            END
        ) AS employer_sg_amount_90d,


        /* =====================================================
           Salary Sacrifice
           ===================================================== */

        SUM
        (
            CASE
                WHEN vc.contribution_type = 'Salary Sacrifice'
                THEN vc.amount
                ELSE 0
            END
        ) AS salary_sacrifice_amount_12m,

        SUM
        (
            CASE
                WHEN vc.contribution_type = 'Salary Sacrifice'
                 AND vc.event_date >= @Recent90Start
                THEN vc.amount
                ELSE 0
            END
        ) AS salary_sacrifice_amount_90d,


        /* =====================================================
           Member Voluntary / Post Tax
           ===================================================== */

        SUM
        (
            CASE
                WHEN vc.contribution_type = 'Post Tax Voluntary'
                THEN vc.amount
                ELSE 0
            END
        ) AS member_voluntary_amount_12m,

        SUM
        (
            CASE
                WHEN vc.contribution_type = 'Post Tax Voluntary'
                 AND vc.event_date >= @Recent90Start
                THEN vc.amount
                ELSE 0
            END
        ) AS member_voluntary_amount_90d

    FROM valid_contributions vc

    GROUP BY vc.accountID
)

SELECT
    cs.accountID,


    /* Long-term behaviour */

    cs.contribution_count_12m,

    cs.contribution_amount_12m,

    cs.avg_contribution_transaction_amount_12m,

    cs.contribution_active_months_12m,

    cs.days_since_last_contribution,


    /* Recent vs previous 90 days */

    cs.recent_contribution_amount_90d,

    cs.prior_contribution_amount_90d,

    cs.recent_contribution_count_90d,

    cs.prior_contribution_count_90d,


    /* Absolute change */

    (
        cs.recent_contribution_amount_90d
        - cs.prior_contribution_amount_90d
    ) AS contribution_amount_change_90d,


    /* Percentage change */

    CASE
        WHEN cs.prior_contribution_amount_90d > 0
        THEN
            CAST
            (
                (
                    cs.recent_contribution_amount_90d
                    - cs.prior_contribution_amount_90d
                ) * 100.0
                / cs.prior_contribution_amount_90d

                AS DECIMAL(10,2)
            )
        ELSE NULL
    END AS contribution_change_pct_90d,


    /*
       Cessation:
       Member had contribution activity in previous 90 days
       but no contribution in recent 90 days.
    */

    CASE
        WHEN cs.prior_contribution_amount_90d > 0
         AND cs.recent_contribution_amount_90d = 0
        THEN 1
        ELSE 0
    END AS contribution_ceased_90d_flag,


    /*
       Decline flag:
       Keep as supporting feature.
       Actual change amount / percentage is more informative.
    */

    CASE
        WHEN cs.prior_contribution_amount_90d > 0
         AND cs.recent_contribution_amount_90d
             < cs.prior_contribution_amount_90d
        THEN 1
        ELSE 0
    END AS contribution_decline_flag,


    /* Employer SG */

    cs.employer_sg_amount_12m,

    cs.employer_sg_amount_90d,


    /* Salary Sacrifice */

    cs.salary_sacrifice_amount_12m,

    cs.salary_sacrifice_amount_90d,


    /* Member Voluntary */

    cs.member_voluntary_amount_12m,

    cs.member_voluntary_amount_90d


FROM contribution_summary cs

ORDER BY cs.accountID;
