/* Original standalone query with ONLY two requested feature groups added.
   NEW: INVESTMENT_CHANGE (ID 7), PAYMENT_MEMBER (ID 28).
   PAYMENT_MEMBER exit-date exclusion is provisional pending SME validation. */

DECLARE @AsOfDate DATE = '2026-10-20';

DECLARE @FeatureStartDate DATE =
    DATEADD(DAY, 1, DATEADD(MONTH, -12, @AsOfDate));

DECLARE @Recent90Start DATE =
    DATEADD(DAY, -89, @AsOfDate);

DECLARE @Recent30Start DATE =
    DATEADD(DAY, -29, @AsOfDate);

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
          'MIAPD',
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
/* NEW: one exit date per account for provisional PAYMENT_MEMBER screening. */
account_exit AS
(
    SELECT accountID, MIN(CAST(exitDate AS DATE)) AS exitDate
    FROM edgeSource.accountSummary
    WHERE exitDate IS NOT NULL
    GROUP BY accountID
),
event_base AS
(
    SELECT
        ced.accountID,
        ced.eventDate,
        ced.eventID,
        ce.eventName,
        ced.eventAmount,  -- NEW: for PAYMENT_MEMBER amount feature
        CASE
            /* Advice */
            WHEN ce.eventName IN
            (
                'FINANCIAL_ADVICE',
                'STRATEGIC_ADVICE',
                'STRATEGIC_ADVICE_REVENUE'
            )
            THEN 'ADVICE'

            /* Digital engagement */
            WHEN ce.eventName = 'WEBSITE_LOGIN'
            THEN 'DIGITAL'

            /* Member service / contact */
            WHEN ce.eventName IN
            (
                'HELP_DESK_CALL',
                'CONTACT_UPDATE'
            )
            THEN 'MEMBER_SERVICE'

            /* Contribution behaviour */
            WHEN ce.eventName IN
            (
                'SG_CONTRIBUTIONS',
                'SALARY_SACRIFICE',
                'POST_TAX_CONTRIBUTION'
            )
            THEN 'CONTRIBUTION'

            /* Roll-in / consolidation */
            WHEN ce.eventName = 'ROLLIN'
            THEN 'ROLLIN'

            /* Retirement / pension */
            WHEN ce.eventName IN
            (
                'PENSION',
                'ALLOCATED_PENSION',
                'TTR'
            )
            THEN 'RETIREMENT_PENSION'

            /* Insurance */
            WHEN ce.eventName = 'INSURANCE_OPT_IN'
            THEN 'INSURANCE'

            /* Beneficiary activity */
            WHEN ce.eventName IN
            (
                'NOMINATED_BENEFICIARY',
                'NOMINATED_BINDING_BENEFICIARY'
            )
            THEN 'BENEFICIARY'

            /* NEW: investment change, business event ID 7 */
            WHEN ce.eventID = 7 THEN 'INVESTMENT_CHANGE'

            /* NEW: payment to member, business event ID 28 */
            WHEN ce.eventID = 28 THEN 'PAYMENT_MEMBER'

            ELSE NULL
        END AS event_category
    FROM edgeSource.campaignEventDetails ced
    INNER JOIN edgeSource.campaignEvents ce
        ON ce.eventID = ced.eventID
    INNER JOIN eligible_accounts ea
        ON ea.accountID = ced.accountID
    /* NEW: provisional payment-member exit-date screen */
    LEFT JOIN account_exit ax
        ON ax.accountID = ced.accountID
    WHERE ced.eventDate >= @FeatureStartDate
      AND ced.eventDate <= @AsOfDate
      /* Exclude target / near-exit events */
      AND ce.eventName NOT IN
      (
          'MEMBER_EXIT',
          'ROLLOVER',
          'PAYMENT_EXTERNAL'
      )
      /* NEW: for PAYMENT_MEMBER only, omit events on/after known exit date.
         This is NOT a validated full-withdrawal classifier. */
      AND (
          ce.eventID <> 28
          OR ax.exitDate IS NULL
          OR CAST(ced.eventDate AS DATE) < ax.exitDate
      )
)
SELECT
    accountID,

    /* Overall campaign/event behaviour */
    COUNT(*) AS campaign_event_count_12m,
    COUNT(DISTINCT eventName)
        AS distinct_campaign_event_type_count_12m,
    DATEDIFF
    (
        DAY,
        MAX(eventDate),
        @AsOfDate
    ) AS days_since_last_campaign_event,
    SUM
    (
        CASE
            WHEN eventDate >= @Recent90Start
            THEN 1
            ELSE 0
        END
    ) AS recent_campaign_event_count_90d,

    /* Advice */
    SUM
    (
        CASE WHEN event_category = 'ADVICE'
             THEN 1 ELSE 0 END
    ) AS advice_event_count_12m,
    SUM
    (
        CASE
            WHEN event_category = 'ADVICE'
             AND eventDate >= @Recent90Start
            THEN 1 ELSE 0
        END
    ) AS recent_advice_event_count_90d,
    DATEDIFF
    (
        DAY,
        MAX(CASE WHEN event_category = 'ADVICE'
                 THEN eventDate END),
        @AsOfDate
    ) AS days_since_last_advice_event,

    /* Website / digital */
    SUM
    (
        CASE WHEN event_category = 'DIGITAL'
             THEN 1 ELSE 0 END
    ) AS website_login_count_12m,
    SUM
    (
        CASE
            WHEN event_category = 'DIGITAL'
             AND eventDate >= @Recent90Start
            THEN 1 ELSE 0
        END
    ) AS website_login_count_90d,
    SUM
    (
        CASE
            WHEN event_category = 'DIGITAL'
             AND eventDate >= @Recent30Start
            THEN 1 ELSE 0
        END
    ) AS website_login_count_30d,
    DATEDIFF
    (
        DAY,
        MAX(CASE WHEN event_category = 'DIGITAL'
                 THEN eventDate END),
        @AsOfDate
    ) AS days_since_last_website_login,

    /* Member service */
    SUM
    (
        CASE WHEN event_category = 'MEMBER_SERVICE'
             THEN 1 ELSE 0 END
    ) AS member_service_event_count_12m,
    SUM
    (
        CASE
            WHEN event_category = 'MEMBER_SERVICE'
             AND eventDate >= @Recent90Start
            THEN 1 ELSE 0
        END
    ) AS recent_member_service_event_count_90d,

    /* Contribution */
    SUM
    (
        CASE WHEN event_category = 'CONTRIBUTION'
             THEN 1 ELSE 0 END
    ) AS contribution_event_count_12m,
    SUM
    (
        CASE
            WHEN event_category = 'CONTRIBUTION'
             AND eventDate >= @Recent90Start
            THEN 1 ELSE 0
        END
    ) AS recent_contribution_event_count_90d,

    /* Roll-in */
    SUM
    (
        CASE WHEN event_category = 'ROLLIN'
             THEN 1 ELSE 0 END
    ) AS rollin_event_count_12m,
    SUM
    (
        CASE
            WHEN event_category = 'ROLLIN'
             AND eventDate >= @Recent90Start
            THEN 1 ELSE 0
        END
    ) AS recent_rollin_event_count_90d,

    /* Retirement / Pension */
    SUM
    (
        CASE WHEN event_category = 'RETIREMENT_PENSION'
             THEN 1 ELSE 0 END
    ) AS retirement_pension_event_count_12m,
    SUM
    (
        CASE
            WHEN event_category = 'RETIREMENT_PENSION'
             AND eventDate >= @Recent90Start
            THEN 1 ELSE 0
        END
    ) AS recent_retirement_pension_event_count_90d,

    /* Insurance */
    MAX
    (
        CASE WHEN event_category = 'INSURANCE'
             THEN 1 ELSE 0 END
    ) AS insurance_opt_in_12m_flag,

    /* Beneficiary */
    SUM
    (
        CASE WHEN event_category = 'BENEFICIARY'
             THEN 1 ELSE 0 END
    ) AS beneficiary_event_count_12m,

    /* NEW: investment change (ID 7) */
    SUM(CASE WHEN event_category = 'INVESTMENT_CHANGE'
             THEN 1 ELSE 0 END) AS investment_change_count_12m,
    SUM(CASE WHEN event_category = 'INVESTMENT_CHANGE'
              AND eventDate >= @Recent90Start
             THEN 1 ELSE 0 END) AS recent_investment_change_count_90d,
    DATEDIFF(DAY,
        MAX(CASE WHEN event_category = 'INVESTMENT_CHANGE' THEN eventDate END),
        @AsOfDate) AS days_since_last_investment_change,

    /* NEW: payment member (ID 28) - provisional */
    SUM(CASE WHEN event_category = 'PAYMENT_MEMBER'
             THEN 1 ELSE 0 END) AS payment_member_count_12m,
    SUM(CASE WHEN event_category = 'PAYMENT_MEMBER'
              AND eventDate >= @Recent90Start
             THEN 1 ELSE 0 END) AS recent_payment_member_count_90d,
    SUM(CASE WHEN event_category = 'PAYMENT_MEMBER'
             THEN COALESCE(eventAmount, 0) ELSE 0 END) AS payment_member_amount_12m,
    DATEDIFF(DAY,
        MAX(CASE WHEN event_category = 'PAYMENT_MEMBER' THEN eventDate END),
        @AsOfDate) AS days_since_last_payment_member

FROM event_base
GROUP BY accountID
ORDER BY accountID;
