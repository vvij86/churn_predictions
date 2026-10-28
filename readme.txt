/*
Feature Name: workflow_member_behaviour_12m_group
Feature Group: Workflow Behaviour

Business Meaning:
    Captures strong member-driven workflow activity only.
    jobDescription is used to determine the business meaning.
    jobSourceDescription is used mainly as supporting/source information.

Included behaviour groups:
    - Member Inquiry / Service
    - Complaint / Escalation
    - Member Detail / Contact Change
    - Beneficiary Activity

Excluded:
    - RF-Processor
    - SUPERFACTS / SUPERFACTSS
    - Transaction Reports
    - DigitalCardBatchLoad
    - Transition Fail
    - Internal Transfer
    - rollover / transfer / payment activity
    - contribution processing
    - investment processing already covered by dedicated source
    - insurance claims / death / TPD / SCI processing
    - generic or unidentified Inquiry IDs
    - technical/admin workflow

Feature Window:
    Previous 12 months from AsOfDate

Recent Windows:
    90 days
    30 days

Point-in-Time Rule:
    jobStartDate must be on or before AsOfDate.
    jobCompletionDate is used only when <= AsOfDate.
*/

DECLARE @AsOfDate DATE = '2024-03-31';

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

workflow_base AS
(
    SELECT
        wf.accountID,
        CAST(wf.jobStartDate AS DATE) AS jobStartDate,
        CAST(wf.jobCompletionDate AS DATE) AS jobCompletionDate,
        wf.jobCompletedFlag,
        wf.jobSourceDescription,
        wf.jobDescription,

        CASE

            /* Complaint / Escalation */
            WHEN
                LOWER(wf.jobDescription) LIKE '%complaint%'
                OR LOWER(wf.jobDescription) LIKE '%escalation%'
            THEN 'COMPLAINT_ESCALATION'


            /* Member Detail / Contact Change */
            WHEN
                LOWER(wf.jobDescription) LIKE '%update contact%'
                OR LOWER(wf.jobDescription) LIKE '%address change%'
                OR LOWER(wf.jobDescription) LIKE '%update basic detail%'
                OR LOWER(wf.jobDescription) LIKE '%communication preference%'
            THEN 'MEMBER_DETAIL_CHANGE'


            /* Beneficiary Activity */
            WHEN
                LOWER(wf.jobDescription) LIKE '%beneficiar%'
            THEN 'BENEFICIARY_ACTIVITY'


            /* Strong Member Inquiry / Service */
            WHEN
                wf.jobDescription IN
                (
                    'Inquiry - Website',
                    'Inquiry - General',
                    'Inquiry - Contribution',
                    'Inquiry - Pension',
                    'Inquiry - Insurance',
                    'Inquiry - Investment Performance',
                    'Member Contact'
                )
                OR LOWER(wf.jobDescription) LIKE '%online enquiry form%'
            THEN 'MEMBER_INQUIRY_SERVICE'


            ELSE NULL

        END AS workflow_category

    FROM edgeSource.accountEngagementWorkflow wf

    INNER JOIN eligible_accounts ea
        ON ea.accountID = wf.accountID

    WHERE wf.jobStartDate >= @FeatureStartDate
      AND wf.jobStartDate <= @AsOfDate

      AND
      (
          wf.jobSourceDescription IS NULL
          OR wf.jobSourceDescription NOT IN
          (
              'RF-Processor',
              'SUPERFACTS',
              'SUPERFACTSS',
              'Transaction Reports',
              'DigitalCardBatchLoad',
              'Transition Fail',
              'Internal Transfer'
          )
      )
),

meaningful_workflow AS
(
    SELECT
        accountID,
        jobStartDate,
        jobCompletionDate,
        jobCompletedFlag,
        jobSourceDescription,
        jobDescription,
        workflow_category
    FROM workflow_base
    WHERE workflow_category IS NOT NULL
),

workflow_features AS
(
    SELECT
        mw.accountID,

        /* Overall meaningful workflow activity */
        COUNT(*) AS meaningful_workflow_count_12m,

        COUNT(DISTINCT mw.jobStartDate)
            AS meaningful_workflow_active_days_12m,

        DATEDIFF
        (
            DAY,
            MAX(mw.jobStartDate),
            @AsOfDate
        ) AS days_since_last_meaningful_workflow,

        SUM
        (
            CASE
                WHEN mw.jobStartDate >= @Recent90Start
                THEN 1
                ELSE 0
            END
        ) AS recent_meaningful_workflow_count_90d,

        SUM
        (
            CASE
                WHEN mw.jobStartDate >= @Recent30Start
                THEN 1
                ELSE 0
            END
        ) AS recent_meaningful_workflow_count_30d,


        /* Completed / Open workflow */
        SUM
        (
            CASE
                WHEN mw.jobCompletedFlag = 1
                 AND mw.jobCompletionDate IS NOT NULL
                 AND mw.jobCompletionDate <= @AsOfDate
                THEN 1
                ELSE 0
            END
        ) AS completed_meaningful_workflow_count_12m,

        SUM
        (
            CASE
                WHEN
                (
                    mw.jobCompletedFlag = 0
                    OR mw.jobCompletionDate IS NULL
                    OR mw.jobCompletionDate > @AsOfDate
                )
                THEN 1
                ELSE 0
            END
        ) AS open_meaningful_workflow_count_asof,


        /* Member Inquiry / Service */
        SUM
        (
            CASE
                WHEN mw.workflow_category = 'MEMBER_INQUIRY_SERVICE'
                THEN 1
                ELSE 0
            END
        ) AS member_inquiry_service_count_12m,

        SUM
        (
            CASE
                WHEN mw.workflow_category = 'MEMBER_INQUIRY_SERVICE'
                 AND mw.jobStartDate >= @Recent90Start
                THEN 1
                ELSE 0
            END
        ) AS recent_member_inquiry_service_count_90d,


        /* Complaint / Escalation */
        SUM
        (
            CASE
                WHEN mw.workflow_category = 'COMPLAINT_ESCALATION'
                THEN 1
                ELSE 0
            END
        ) AS complaint_escalation_count_12m,

        SUM
        (
            CASE
                WHEN mw.workflow_category = 'COMPLAINT_ESCALATION'
                 AND mw.jobStartDate >= @Recent90Start
                THEN 1
                ELSE 0
            END
        ) AS recent_complaint_escalation_count_90d,


        /* Member Detail Change */
        SUM
        (
            CASE
                WHEN mw.workflow_category = 'MEMBER_DETAIL_CHANGE'
                THEN 1
                ELSE 0
            END
        ) AS member_detail_change_count_12m,


        /* Beneficiary Activity */
        SUM
        (
            CASE
                WHEN mw.workflow_category = 'BENEFICIARY_ACTIVITY'
                THEN 1
                ELSE 0
            END
        ) AS beneficiary_change_count_12m

    FROM meaningful_workflow mw
    GROUP BY mw.accountID
)

SELECT
    accountID,
    meaningful_workflow_count_12m,
    meaningful_workflow_active_days_12m,
    days_since_last_meaningful_workflow,
    recent_meaningful_workflow_count_90d,
    recent_meaningful_workflow_count_30d,
    completed_meaningful_workflow_count_12m,
    open_meaningful_workflow_count_asof,
    member_inquiry_service_count_12m,
    recent_member_inquiry_service_count_90d,
    complaint_escalation_count_12m,
    recent_complaint_escalation_count_90d,
    member_detail_change_count_12m,
    beneficiary_change_count_12m
FROM workflow_features
ORDER BY accountID;
