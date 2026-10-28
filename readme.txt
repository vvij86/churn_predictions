/*
Feature Name: campaign_event_behaviour_12m_group
Feature Group: Campaign / Event Behaviour
Business Meaning:
    Captures meaningful member behaviour from campaign/event activity using grouped
    event names rather than creating one ML feature for every individual event.

Source Table(s):
    edgeSource.campaignEventDetails
    edgeSource.campaignEvents

Source Column(s):
    campaignEventDetails.accountID
    campaignEventDetails.eventDate
    campaignEventDetails.eventID
    campaignEvents.eventID
    campaignEvents.eventName

Feature Window:
    Previous 12 months from AsOfDate.
    Selected 90-day and 30-day recent features are also included.

Point-in-Time Rule:
    eventDate must be between FeatureStartDate and AsOfDate.

Leakage Risk:
    MEMBER_EXIT is excluded.
    ROLLOVER / PAYMENT_EXTERNAL are retained separately for business/leakage review
    and are not included in the general behavioural counts.

Recommendation:
    REVIEW REQUIRED

Business Confirmation Needed:
    Confirm grouped event categories and confirm which events represent genuine
    member behaviour versus system/business-generated activity.
*/

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

event_base AS
(
    SELECT
        ced.accountID,
        ced.eventDate,
        ced.eventID,
        ce.eventName,

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


            /* Investment behaviour */
            WHEN ce.eventName = 'INVESTMENT_CHANGE'
            THEN 'INVESTMENT'


            /* Contribution behaviour */
            WHEN ce.eventName IN
            (
                'SG_CONTRIBUTIONS',
                'SALARY_SACRIFICE',
                'POST_TAX_CONTRIBUTION'
            )
            THEN 'CONTRIBUTION'


            /* Roll-in */
            WHEN ce.eventName = 'ROLLIN'
            THEN 'ROLLIN'


            /* Retirement / Pension */
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


            /* Business initiated contact - review separately */
            WHEN ce.eventName = 'OUTBOUND_CALL'
            THEN 'OUTBOUND_CONTACT'


            /* Payment behaviour - business confirmation needed */
            WHEN ce.eventName IN
            (
                'PAYMENT_ATO',
                'PAYMENT_MEMBER',
                'PAYMENT_UNCONTROLLED'
            )
            THEN 'PAYMENT'


            /* Potential near-exit behaviour - do not combine with normal events */
            WHEN ce.eventName IN
            (
                'PAYMENT_EXTERNAL',
                'ROLLOVER'
            )
            THEN 'ROLLOVER_EXIT_REVIEW'


            /* Meaning needs confirmation */
            WHEN ce.eventName = 'CONSENT_TO_SEARCH'
            THEN 'OTHER_REVIEW'


            /* Direct target leakage */
            WHEN ce.eventName = 'MEMBER_EXIT'
            THEN 'EXCLUDE_TARGET_LEAKAGE'

            ELSE 'OTHER_REVIEW'

        END AS event_category

    FROM edgeSource.campaignEventDetails ced

    INNER JOIN edgeSource.campaignEvents ce
        ON ce.eventID = ced.eventID

    INNER JOIN eligible_accounts ea
        ON ea.accountID = ced.accountID

    WHERE ced.eventDate >= @FeatureStartDate
      AND ced.eventDate <= @AsOfDate

      /* Explicitly exclude churn outcome */
      AND ce.eventName <> 'MEMBER_EXIT'
)

SELECT
    accountID,


    /* =========================================================
       Overall useful campaign/event behaviour
       ========================================================= */

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


    /* =========================================================
       Advice behaviour
       ========================================================= */

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
        MAX
        (
            CASE
                WHEN event_category = 'ADVICE'
                THEN eventDate
            END
        ),
        @AsOfDate
    ) AS days_since_last_advice_event,


    /* =========================================================
       Website / Digital behaviour
       ========================================================= */

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
        MAX
        (
            CASE
                WHEN event_category = 'DIGITAL'
                THEN eventDate
            END
        ),
        @AsOfDate
    ) AS days_since_last_website_login,


    /* =========================================================
       Member service/contact
       ========================================================= */

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


    /* =========================================================
       Investment behaviour
       ========================================================= */

    SUM
    (
        CASE WHEN event_category = 'INVESTMENT'
             THEN 1 ELSE 0 END
    ) AS investment_change_event_count_12m,

    SUM
    (
        CASE
            WHEN event_category = 'INVESTMENT'
             AND eventDate >= @Recent90Start
            THEN 1 ELSE 0
        END
    ) AS recent_investment_change_event_count_90d,

    DATEDIFF
    (
        DAY,
        MAX
        (
            CASE
                WHEN event_category = 'INVESTMENT'
                THEN eventDate
            END
        ),
        @AsOfDate
    ) AS days_since_last_investment_change_event,


    /* =========================================================
       Contribution behaviour
       ========================================================= */

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


    /* =========================================================
       Roll-in behaviour
       ========================================================= */

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


    /* =========================================================
       Retirement / pension
       ========================================================= */

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


    /* =========================================================
       Insurance
       ========================================================= */

    MAX
    (
        CASE WHEN event_category = 'INSURANCE'
             THEN 1 ELSE 0 END
    ) AS insurance_opt_in_12m_flag,


    /* =========================================================
       Beneficiary behaviour
       ========================================================= */

    SUM
    (
        CASE WHEN event_category = 'BENEFICIARY'
             THEN 1 ELSE 0 END
    ) AS beneficiary_event_count_12m,


    /* =========================================================
       Business initiated contact - keep separate
       ========================================================= */

    SUM
    (
        CASE WHEN event_category = 'OUTBOUND_CONTACT'
             THEN 1 ELSE 0 END
    ) AS outbound_contact_count_12m,


    /* =========================================================
       Payment events - review meaning with business
       ========================================================= */

    SUM
    (
        CASE WHEN event_category = 'PAYMENT'
             THEN 1 ELSE 0 END
    ) AS payment_event_count_12m,


    /* =========================================================
       Potential near-exit / leakage events
       Keep separate for review - DO NOT mix into total useful
       behavioural risk features until business confirms
       ========================================================= */

    SUM
    (
        CASE WHEN event_category = 'ROLLOVER_EXIT_REVIEW'
             THEN 1 ELSE 0 END
    ) AS rollover_exit_review_event_count_12m,


    /* =========================================================
       Unclassified / business review
       ========================================================= */

    SUM
    (
        CASE WHEN event_category = 'OTHER_REVIEW'
             THEN 1 ELSE 0 END
    ) AS other_review_event_count_12m

FROM event_base

GROUP BY accountID

ORDER BY accountID;
