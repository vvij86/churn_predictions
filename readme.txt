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
      AND (a.exitDateRecorded IS NULL
           OR a.exitDateRecorded > @AsOfDate)
      AND (a.dateOfDeath IS NULL
           OR a.dateOfDeath > @AsOfDate)
      AND (a.deathIndicatorFlag IS NULL
           OR a.deathIndicatorFlag = 0)
),

helpline_base AS
(
    SELECT
        h.accountID,
        h.callDate,
        h.inquiryCode,
        h.inquiryDescription,

        CASE

            /* Advice / Financial Planning */
            WHEN h.inquiryDescription IN
            (
                'SOA',
                'Projection advice',
                'Financial Advice',
                'Financial Adviser Contact',
                'MST workplace advice',
                'Retirement planning',
                'TTR advice'
            )
            THEN 'ADVICE'

            /* Contribution / Money In */
            WHEN h.inquiryDescription IN
            (
                'Contribution',
                'Contributions splitting',
                'Roll in'
            )
            OR h.inquiryDescription LIKE 'Contributions (pre tax%'
            THEN 'CONTRIBUTION'

            /* Consolidation / Rollover */
            WHEN h.inquiryDescription IN
            (
                'Consolidation Inbound',
                'Consolidation Outbound'
            )
            OR h.inquiryDescription LIKE 'Choice/Consolidate%'
            THEN 'CONSOLIDATION_ROLLOVER'

            /* Retirement / Pension */
            WHEN h.inquiryDescription IN
            (
                'Retirement / Pension',
                'Retirement Optimiser',
                'Redundancy',
                'Commutation'
            )
            THEN 'RETIREMENT'

            /* Investment */
            WHEN h.inquiryDescription IN
            (
                'Choice of Fund',
                'Investments',
                'MST good choices'
            )
            OR h.inquiryDescription LIKE 'Investment Choice%'
            THEN 'INVESTMENT'

            /* Insurance */
            WHEN h.inquiryDescription IN
            (
                'Insurance Claim',
                'Insurance Underwriting'
            )
            OR h.inquiryDescription LIKE 'Insurance/ Insurance%'
            THEN 'INSURANCE'

            /* Digital / Account Access */
            WHEN h.inquiryDescription IN
            (
                'Member Online Access',
                'Website'
            )
            THEN 'DIGITAL_ACCESS'

            /* Complaint / Negative Experience */
            WHEN h.inquiryDescription = 'Complaint'
            THEN 'COMPLAINT'

            /* Account Administration */
            WHEN h.inquiryDescription IN
            (
                'Annual Statement',
                'Beneficiary',
                'Change Address',
                'Update Contact Details',
                'Fee query',
                'Fund General Info',
                'Benefit Quote'
            )
            THEN 'ACCOUNT_ADMIN'

            /* Campaign related */
            WHEN h.inquiryDescription LIKE 'Campaign %'
            THEN 'CAMPAIGN'

            ELSE 'OTHER_REVIEW'

        END AS inquiry_category

    FROM edgeSource.accountEngagementHelpline h

    INNER JOIN eligible_accounts ea
        ON ea.accountID = h.accountID

    WHERE h.callDate >= @FeatureStartDate
      AND h.callDate <= @AsOfDate
      AND h.inquiryCode IS NOT NULL
      AND h.inquiryDescription IS NOT NULL
)

SELECT
    accountID,

    /* Existing general helpline behaviour */
    COUNT(*) AS helpline_contact_count_12m,

    COUNT(DISTINCT inquiryCode)
        AS helpline_inquiry_count_12m,

    COUNT(DISTINCT CAST(callDate AS DATE))
        AS helpline_active_days_12m,

    DATEDIFF
    (
        DAY,
        MAX(callDate),
        @AsOfDate
    ) AS days_since_last_helpline_contact,

    SUM
    (
        CASE
            WHEN callDate >= @Recent90Start
             AND callDate <= @AsOfDate
            THEN 1
            ELSE 0
        END
    ) AS recent_helpline_contact_count_90d,

    SUM
    (
        CASE
            WHEN callDate >= @Recent30Start
             AND callDate <= @AsOfDate
            THEN 1
            ELSE 0
        END
    ) AS recent_helpline_contact_count_30d,


    /* Proposed inquiry-description features */

    SUM(CASE WHEN inquiry_category = 'ADVICE'
             THEN 1 ELSE 0 END)
        AS advice_inquiry_count_12m,

    SUM(CASE WHEN inquiry_category = 'CONTRIBUTION'
             THEN 1 ELSE 0 END)
        AS contribution_inquiry_count_12m,

    SUM(CASE WHEN inquiry_category = 'CONSOLIDATION_ROLLOVER'
             THEN 1 ELSE 0 END)
        AS consolidation_rollover_inquiry_count_12m,

    SUM(CASE WHEN inquiry_category = 'RETIREMENT'
             THEN 1 ELSE 0 END)
        AS retirement_inquiry_count_12m,

    SUM(CASE WHEN inquiry_category = 'INVESTMENT'
             THEN 1 ELSE 0 END)
        AS investment_inquiry_count_12m,

    SUM(CASE WHEN inquiry_category = 'INSURANCE'
             THEN 1 ELSE 0 END)
        AS insurance_inquiry_count_12m,

    SUM(CASE WHEN inquiry_category = 'COMPLAINT'
             THEN 1 ELSE 0 END)
        AS complaint_inquiry_count_12m,

    SUM(CASE WHEN inquiry_category = 'DIGITAL_ACCESS'
             THEN 1 ELSE 0 END)
        AS digital_access_inquiry_count_12m,


    /* Selective recent 90-day features */

    SUM
    (
        CASE
            WHEN inquiry_category = 'ADVICE'
             AND callDate >= @Recent90Start
            THEN 1 ELSE 0
        END
    ) AS recent_advice_inquiry_count_90d,

    SUM
    (
        CASE
            WHEN inquiry_category = 'CONSOLIDATION_ROLLOVER'
             AND callDate >= @Recent90Start
            THEN 1 ELSE 0
        END
    ) AS recent_consolidation_rollover_inquiry_count_90d,

    SUM
    (
        CASE
            WHEN inquiry_category = 'RETIREMENT'
             AND callDate >= @Recent90Start
            THEN 1 ELSE 0
        END
    ) AS recent_retirement_inquiry_count_90d,

    SUM
    (
        CASE
            WHEN inquiry_category = 'COMPLAINT'
             AND callDate >= @Recent90Start
            THEN 1 ELSE 0
        END
    ) AS recent_complaint_inquiry_count_90d,


    /* Very recent indicators */

    MAX
    (
        CASE
            WHEN inquiry_category = 'COMPLAINT'
             AND callDate >= @Recent30Start
            THEN 1 ELSE 0
        END
    ) AS recent_complaint_flag_30d,

    MAX
    (
        CASE
            WHEN inquiry_category = 'CONSOLIDATION_ROLLOVER'
             AND callDate >= @Recent30Start
            THEN 1 ELSE 0
        END
    ) AS recent_rollover_inquiry_flag_30d

FROM helpline_base

GROUP BY accountID

ORDER BY accountID;
