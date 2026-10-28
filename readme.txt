/*
Feature Name: inflow_change_signal_12m_group
Feature Group: Inflow Signals / Contribution Change

Business Meaning:
    Compares the previous 12 months with the current 12 months
    for Employer SG, Salary Sacrifice and Member Voluntary contributions.

    Captures:
    - current contribution amount
    - previous contribution amount
    - amount change
    - percentage change
    - contribution cessation
    - contribution increase / decline

Source Table:
    edgeSource.accountMoneyInflow

Point-in-Time Rule:
    Only data available on or before @AsOfDate is used.

Comparison:
    Previous 12 months vs Current 12 months

Note:
    Rollover-in is not included in this query.
    Rollover behaviour should use the dedicated approved rollover logic/source.
*/


DECLARE @AsOfDate DATE = '2024-03-31';

/* Current 12-month period */
DECLARE @FeatureStartDate DATE =
    DATEADD(DAY, 1, DATEADD(MONTH, -12, @AsOfDate));

/* Previous 12-month period */
DECLARE @BaselineStart DATE =
    DATEADD(DAY, 1, DATEADD(MONTH, -24, @AsOfDate));

DECLARE @BaselineEnd DATE =
    DATEADD(DAY, -1, @FeatureStartDate);


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

inflow_fact AS
(
    SELECT
        ami.accountID,

        CAST(ami.inflowDateReceived AS DATE) AS event_date,


        /* Employer SG */
        CASE
            WHEN ami.inflowDescription IN
            (
                'Employer',
                'Employer Additional Conts',
                'DB Employer Compulsory'
            )
            THEN CAST(ami.inflowAmount AS DECIMAL(18,2))

            ELSE 0.00
        END AS employer_sg_amount,


        /* Salary Sacrifice */
        CASE
            WHEN ami.inflowDescription IN
            (
                'Voluntary Member Salary Sacrifice',
                'DB Member Salary Sacrifice Compulsory'
            )
            THEN CAST(ami.inflowAmount AS DECIMAL(18,2))

            ELSE 0.00
        END AS salary_sacrifice_amount,


        /* Member Voluntary */
        CASE
            WHEN ami.inflowDescription IN
            (
                'Member Voluntary',
                'DB Member Compulsory'
            )
            THEN CAST(ami.inflowAmount AS DECIMAL(18,2))

            ELSE 0.00
        END AS member_voluntary_amount

    FROM edgeSource.accountMoneyInflow ami

    INNER JOIN eligible_accounts ea
        ON ea.accountID = ami.accountID

    /*
      IMPORTANT:
      Use @BaselineStart here, not @FeatureStartDate.

      We need both:
      - previous 12 months
      - current 12 months

      available inside inflow_fact.
    */
    WHERE ami.inflowDateReceived >= @BaselineStart
      AND ami.inflowDateReceived <= @AsOfDate

      AND ami.inflowAmount > 0

      /*
        Only retain the approved contribution descriptions.
        This avoids unrelated inflow records.
      */
      AND ami.inflowDescription IN
      (
          'Employer',
          'Employer Additional Conts',
          'DB Employer Compulsory',
          'Voluntary Member Salary Sacrifice',
          'DB Member Salary Sacrifice Compulsory',
          'Member Voluntary',
          'DB Member Compulsory'
      )

      /* Exclude internal transfer activity */
      AND COALESCE(ami.inflowInternalTransferFlag, 0) = 0

      /* Exclude rollover types */
      AND
      (
          ami.inflowRolloverType IS NULL
          OR ami.inflowRolloverType NOT IN ('I', 'F')
      )
),

inflow_summary AS
(
    SELECT
        i.accountID,


        /* =====================================================
           Employer SG
           ===================================================== */

        SUM
        (
            CASE
                WHEN i.event_date >= @FeatureStartDate
                 AND i.event_date <= @AsOfDate
                THEN i.employer_sg_amount
                ELSE 0
            END
        ) AS employer_sg_current_amount_12m,


        SUM
        (
            CASE
                WHEN i.event_date >= @BaselineStart
                 AND i.event_date <= @BaselineEnd
                THEN i.employer_sg_amount
                ELSE 0
            END
        ) AS employer_sg_previous_amount_12m,


        /* =====================================================
           Salary Sacrifice
           ===================================================== */

        SUM
        (
            CASE
                WHEN i.event_date >= @FeatureStartDate
                 AND i.event_date <= @AsOfDate
                THEN i.salary_sacrifice_amount
                ELSE 0
            END
        ) AS salary_sacrifice_current_amount_12m,


        SUM
        (
            CASE
                WHEN i.event_date >= @BaselineStart
                 AND i.event_date <= @BaselineEnd
                THEN i.salary_sacrifice_amount
                ELSE 0
            END
        ) AS salary_sacrifice_previous_amount_12m,


        /* =====================================================
           Member Voluntary
           ===================================================== */

        SUM
        (
            CASE
                WHEN i.event_date >= @FeatureStartDate
                 AND i.event_date <= @AsOfDate
                THEN i.member_voluntary_amount
                ELSE 0
            END
        ) AS member_voluntary_current_amount_12m,


        SUM
        (
            CASE
                WHEN i.event_date >= @BaselineStart
                 AND i.event_date <= @BaselineEnd
                THEN i.member_voluntary_amount
                ELSE 0
            END
        ) AS member_voluntary_previous_amount_12m

    FROM inflow_fact i

    GROUP BY i.accountID
)

SELECT
    s.accountID,


    /* =========================================================
       Employer SG
       ========================================================= */

    s.employer_sg_current_amount_12m,

    s.employer_sg_previous_amount_12m,

    (
        s.employer_sg_current_amount_12m
        - s.employer_sg_previous_amount_12m
    ) AS employer_sg_change_12m,


    CASE
        WHEN s.employer_sg_previous_amount_12m > 0
        THEN CAST
        (
            (
                s.employer_sg_current_amount_12m
                - s.employer_sg_previous_amount_12m
            ) * 100.0
            / s.employer_sg_previous_amount_12m
            AS DECIMAL(10,2)
        )
        ELSE NULL
    END AS employer_sg_change_pct_12m,


    CASE
        WHEN s.employer_sg_previous_amount_12m > 0
         AND s.employer_sg_current_amount_12m = 0
        THEN 1
        ELSE 0
    END AS employer_sg_cessation_flag,


    CASE
        WHEN s.employer_sg_previous_amount_12m > 0
         AND s.employer_sg_current_amount_12m
             < s.employer_sg_previous_amount_12m
        THEN 1
        ELSE 0
    END AS employer_sg_decline_flag,


    /* =========================================================
       Salary Sacrifice
       ========================================================= */

    s.salary_sacrifice_current_amount_12m,

    s.salary_sacrifice_previous_amount_12m,

    (
        s.salary_sacrifice_current_amount_12m
        - s.salary_sacrifice_previous_amount_12m
    ) AS salary_sacrifice_change_12m,


    CASE
        WHEN s.salary_sacrifice_previous_amount_12m > 0
        THEN CAST
        (
            (
                s.salary_sacrifice_current_amount_12m
                - s.salary_sacrifice_previous_amount_12m
            ) * 100.0
            / s.salary_sacrifice_previous_amount_12m
            AS DECIMAL(10,2)
        )
        ELSE NULL
    END AS salary_sacrifice_change_pct_12m,


    CASE
        WHEN s.salary_sacrifice_previous_amount_12m > 0
         AND s.salary_sacrifice_current_amount_12m = 0
        THEN 1
        ELSE 0
    END AS salary_sacrifice_cessation_flag,


    CASE
        WHEN s.salary_sacrifice_current_amount_12m
             > s.salary_sacrifice_previous_amount_12m
         AND s.salary_sacrifice_current_amount_12m > 0
        THEN 1
        ELSE 0
    END AS salary_sacrifice_increase_flag,


    CASE
        WHEN s.salary_sacrifice_previous_amount_12m > 0
         AND s.salary_sacrifice_current_amount_12m
             < s.salary_sacrifice_previous_amount_12m
        THEN 1
        ELSE 0
    END AS salary_sacrifice_decline_flag,


    /* =========================================================
       Member Voluntary
       ========================================================= */

    s.member_voluntary_current_amount_12m,

    s.member_voluntary_previous_amount_12m,

    (
        s.member_voluntary_current_amount_12m
        - s.member_voluntary_previous_amount_12m
    ) AS member_voluntary_change_12m,


    CASE
        WHEN s.member_voluntary_previous_amount_12m > 0
        THEN CAST
        (
            (
                s.member_voluntary_current_amount_12m
                - s.member_voluntary_previous_amount_12m
            ) * 100.0
            / s.member_voluntary_previous_amount_12m
            AS DECIMAL(10,2)
        )
        ELSE NULL
    END AS member_voluntary_change_pct_12m,


    CASE
        WHEN s.member_voluntary_previous_amount_12m > 0
         AND s.member_voluntary_current_amount_12m = 0
        THEN 1
        ELSE 0
    END AS member_voluntary_cessation_flag,


    CASE
        WHEN s.member_voluntary_current_amount_12m
             > s.member_voluntary_previous_amount_12m
         AND s.member_voluntary_current_amount_12m > 0
        THEN 1
        ELSE 0
    END AS member_voluntary_increase_flag,


    CASE
        WHEN s.member_voluntary_previous_amount_12m > 0
         AND s.member_voluntary_current_amount_12m
             < s.member_voluntary_previous_amount_12m
        THEN 1
        ELSE 0
    END AS member_voluntary_decline_flag


FROM inflow_summary s

ORDER BY s.accountID;
