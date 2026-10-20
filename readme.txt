Read member_retention_ml_copilot_instructions.md completely and follow all rules in it.

Also review these reference files before generating anything:

- MemberRetention_01-AccountBase_v006.sql
- MemberRetention_03-MemberRetentionMetrics_v005.sql
- MercerEdge_ML_Churn_Driver_EDA_Phase2.xlsx
- MercerEdge_ML_Churn_Driver_EDA_Remaining_Tables_part2.xlsx
- All_table_scripts.sql
- All_Other_tables_Not_explored.sql

Use behaviorial.sql only as an output-style reference for how I want individual standalone SQL queries presented. Do not copy its old logic blindly.

I am restarting feature engineering from scratch.

Create a new file only:

behavioural_features_business_review.sql

Do not modify or overwrite behaviorial.sql.

Objective

Create one SQL file containing all proposed standalone feature-engineering queries so I can share the file with business and the wider team for feature confirmation before building the final consolidated ML dataset.

Each query must be:

- self-contained
- independently runnable in SQL Server
- easy to understand
- easy to copy/paste and execute individually
- clearly documented with business meaning, source and filters

Do not build the final modelling dataset yet.

Important date handling

Do not define common/shared date parameters once at the top of the file.

Each standalone query must declare its own required date parameters immediately before that query.

For a normal 12-month feature query, use:

DECLARE @AsOfDate DATE = '2024-03-31';

DECLARE @FeatureStartDate DATE =
    DATEADD(DAY, 1, DATEADD(MONTH, -12, @AsOfDate));

If a query needs recent/prior 90-day comparison periods, declare these inside that query block as well:

DECLARE @Recent90Start DATE =
    DATEADD(DAY, -89, @AsOfDate);

DECLARE @Prior90Start DATE =
    DATEADD(DAY, -179, @AsOfDate);

DECLARE @Prior90End DATE =
    DATEADD(DAY, -90, @AsOfDate);

Every query block must be independently executable and must not depend on variables, temp tables, CTEs or setup created by an earlier query block.

If a mapping is needed, include the required mapping logic inside the same standalone query block.

Do not make one feature query depend on another query having been executed first.

Important distinction:

- Overall training history is approximately 36 months.
- Default behavioural feature window per AsOfDate is previous 12 months.
- Do not confuse the 36-month training history with the 12-month feature window.
- Do not automatically use a 36-month feature window.

Approved account eligibility logic

Use the latest approved business logic:

fundJoinDate <= @AsOfDate
AND (
    exitDateRecorded IS NULL
    OR exitDateRecorded > @AsOfDate
)

Apply the approved death exclusion logic.

Important:

- Use exitDateRecorded, not exitDate.
- exitDateRecorded may be used only for eligibility and target creation.
- It must never be used as a predictive feature.
- Do not create features such as days-until-exit or future-exit indicators.

Where eligibility is required, include the eligible account logic within the same standalone query block.

Do not rely on a common/shared eligible_accounts temp table.

Point-in-time safety

Every predictive feature must only use information available on or before @AsOfDate.

Where appropriate, use:

event_date >= @FeatureStartDate
AND event_date <= @AsOfDate

No feature may use future events or future outcome information.

Do not use:

- exitDateRecorded as a model feature
- MEMBER_EXIT
- future account closure
- future rollover completion
- future outcome-window events
- post-AsOfDate activity

Business reference logic

Use:

MemberRetention_01-AccountBase_v006.sql

for relevant:

- account population logic
- account/reference mappings
- eligibility-related source logic
- source filtering

Use:

MemberRetention_03-MemberRetentionMetrics_v005.sql

for relevant:

- flow mappings
- inflow/outflow classification
- contribution mapping
- rollover mapping
- lookup logic
- description filters
- type filters
- source-direction logic
- other financial/member-flow rules

Do not invent:

- join keys
- flow codes
- lookup values
- description mappings
- business meanings
- event classifications

If reference logic is unclear, mark:

TODO - BUSINESS / REFERENCE CONFIRMATION REQUIRED

Query format

Before every standalone feature query or closely related feature group, add:

/*
Feature Name:
Feature Group:
Business Meaning:
Source Table(s):
Source Column(s):
Reference Mapping Used:
Included Types:
Excluded Types:
Feature Window:
Point-in-Time Rule:
Leakage Risk:
Recommendation:
Business Confirmation Needed:
*/

Then declare that query's own date variables and provide the SQL.

Use only these recommendation values:

- INCLUDE
- REVIEW REQUIRED
- EXCLUDE
- INCLUDE PENDING PROD VALIDATION

1. Account / Tenure / Product Features

Generate standalone queries for valid features such as:

- account_tenure_months
- account_tenure_years
- member_age_years
- member_source
- is_super_flag
- is_pension_flag
- benefit_type
- benefit_class
- database_code
- fund_active_flag
- fund_portal_enabled_flag
- active third-party-authority indicator where point-in-time logic supports it

Use only fields actually supported by the DDL and reference files.

For tenure use fundJoinDate relative to @AsOfDate.

Do not derive AsOfDate from fundJoinDate.

2. Helpline Engagement

Use:

edgeSource.accountEngagementHelpline

Generate standalone queries for:

- helpline_contact_count_12m
- helpline_inquiry_count_12m
- helpline_active_days_12m
- days_since_last_helpline_contact
- recent_helpline_contact_count_90d
- repeat_contact_flag

Apply any relevant filters from the reference SQL for:

- valid calls/events
- useful inquiry types
- duplicate/system/noise records

Do not invent a repeat-contact threshold.

If a threshold is proposed, clearly label it as:

BUSINESS CONFIRMATION REQUIRED

3. Website Engagement

Use:

edgeSource.accountEngagementWeb

Generate standalone queries for:

- web_activity_count_12m
- web_active_days_12m
- days_since_last_web_activity
- recent_web_activity_count_90d

Add this comment clearly:

UAT source not populated. Retain feature definition for Prod/Databricks validation. Do not convert missing UAT web activity to zero.

Recommendation should be:

INCLUDE PENDING PROD VALIDATION

Do not remove these features just because UAT is empty.

4. Workflow Behaviour

Use:

edgeSource.accountEngagementWorkflow

Generate standalone queries for:

- workflow_count_12m
- completed_workflow_count_12m
- open_workflow_count_asof
- days_since_last_workflow
- recent_workflow_count_90d
- repeated workflow indicator where meaningful

Before counting all workflows, inspect/reference workflow types and statuses.

Reduce noise by distinguishing:

- meaningful member-driven workflows
- administrative workflows
- system-generated workflows
- operational/noisy workflows

Do not automatically treat every workflow row as member behaviour.

If meaningful workflow types are not clearly confirmed, mark the feature/query:

REVIEW REQUIRED

5. Contribution Behaviour

Use the exact mapping/filter logic from:

MemberRetention_03-MemberRetentionMetrics_v005.sql

Do not simply count every accountMoneyInflow row.

Generate standalone queries for:

- contribution_count_12m
- contribution_amount_12m
- avg_contribution_amount_12m
- contribution_active_months_12m
- days_since_last_contribution
- recent_contribution_amount_90d
- prior_contribution_amount_90d
- contribution_decline_flag
- months_of_declining_contribution

Use genuine contribution types only where supported by the business reference mapping.

Examples may include, only if confirmed by the reference SQL:

- Employer SG
- Salary Sacrifice
- Post Tax Voluntary

Do not automatically include:

- Rollover In
- Internal Transfer In
- Insurance Claim Proceeds
- Adjustment
- unrelated inflows

Do not use broad logic such as:

inflowDescription NOT IN (...)

if that could allow unrelated inflow types to be counted as contributions.

Reuse the exact business description/type mapping logic where available.

6. Money Flow Behaviour

Use the exact business/reference flow direction and mapping logic.

Generate standalone queries for:

- total_inflow_12m
- total_outflow_12m
- net_flow_12m
- recent_net_flow_90d
- prior_net_flow_90d
- net_flow_decline_flag
- negative_net_flow_count_12m
- negative_net_flow_months_12m
- avg_monthly_net_flow_12m

Do not assume:

- positive amount = inflow
- negative amount = outflow

unless the business reference SQL confirms that interpretation.

Use the actual mapped flow-direction logic.

Prefer monthly aggregation before calculating persistent negative-flow patterns.

7. Rollover / Withdrawal Behaviour

Use the approved/reference rollover mapping logic.

Generate standalone queries for:

- partial_rollover_count_12m
- partial_rollover_amount_12m
- days_since_last_partial_rollover
- recent_partial_rollover_count_90d
- external_rollover_count_12m
- external_rollover_amount_12m
- days_since_last_external_rollover
- recent_external_rollover_count_90d

Keep these concepts separate:

- rollover in
- partial rollover out
- external rollover out
- internal transfer

Internal transfers must be excluded from external rollover risk features.

Any full/external rollover feature that may be too close to actual churn/account closure must be marked:

LEAKAGE REVIEW REQUIRED

Do not use rollover activity after @AsOfDate.

8. Investment Behaviour

Use:

edgeSource.accountInvestments

Generate standalone queries only where supported by actual source/reference semantics, for example:

- investment_change_count_12m
- days_since_last_investment_change
- investment_active_months_12m
- investment_option_count_asof
- direct_investment_flag

Do not assume every investment row represents a behavioural change.

Only use value/change measures if the business meaning of the value column is confirmed.

Mark uncertain features:

REVIEW REQUIRED

9. Insurance Features

Use:

edgeSource.AccountInsuranceCurrent

Generate only point-in-time-safe features.

Check whether the source supports historical reconstruction through:

- effective-from dates
- effective-to dates
- historical rows
- other approved point-in-time logic

Do not use current-state insurance values for historical AsOfDates unless the source supports it.

Do not treat insurance claim proceeds as ordinary contribution activity.

10. Third Party Authority

Use:

edgeSource.thirdPartyAuthority

Where supported, generate an active-as-of indicator using logic similar to:

dateAuthorityRequested <= @AsOfDate
AND (
    terminationDate IS NULL
    OR terminationDate > @AsOfDate
)

Only use this if the actual DDL/source semantics support it.

11. Derived Trend / Change Features

Generate a small number of useful standalone derived feature queries such as:

- recent vs prior 90-day contribution
- contribution decline
- contribution inactivity
- months of declining contribution
- recent vs prior net flow
- persistent negative-flow months
- increasing outflow
- recent partial rollover escalation
- engagement inactivity
- repeat helpline activity
- months without contributions
- financial-stress pattern

Any combined rule must be labelled:

CANDIDATE DERIVED FEATURE - BUSINESS/MODEL VALIDATION REQUIRED

Do not invent arbitrary business thresholds.

If a threshold is necessary for illustration, clearly state it is proposed only.

12. Campaign Features

Campaign engagement is currently deferred for the tactical scope unless explicitly reintroduced.

Do not automatically include campaign engagement features in the current confirmed feature list.

MEMBER_EXIT and other outcome-like campaign events must never be used as predictors.

If campaign logic is shown for reference, clearly label it as deferred/review only.

13. Customer Experience / Qualtrics

CSAT, NPS and VoC are future/candidate sources only unless explicitly confirmed.

Do not create active model features from Qualtrics unless business/source confirmation exists.

If shown, mark:

REVIEW REQUIRED

or

PENDING SOURCE/BUSINESS CONFIRMATION

Noise reduction

For every standalone query, explicitly check whether the following should be excluded or separately classified:

- internal transfers
- adjustments
- insurance claims
- fees
- tax
- administrative records
- system-generated records
- duplicate rows
- reversal rows
- target/outcome events
- future events
- post-AsOfDate events
- workflow noise
- unrelated flow types

Reuse exact business mappings and filters where available.

Do not invent exclusions.

Missing-value behaviour

Do not apply generic missing-value treatment in these business-review queries.

Document the business meaning instead.

Examples:

- no contribution rows can mean zero contribution activity
- no rollover rows can mean zero rollover activity
- recency can remain NULL if no prior event exists
- website fields must remain NULL in UAT because the source itself is not populated

Do not convert UAT-wide website missingness to zero.

Final business-review summary

At the end of behavioural_features_business_review.sql, create a summary result set/table containing:

- feature_name
- feature_group
- business_meaning
- source_table
- source_columns
- mapping_or_filter_used
- included_types
- excluded_types
- feature_window
- point_in_time_status
- leakage_risk
- recommendation
- business_question

Use only:

- INCLUDE
- REVIEW REQUIRED
- EXCLUDE
- INCLUDE PENDING PROD VALIDATION

Mandatory validation before finishing

Review the complete generated SQL and confirm:

1. exitDate is not used where the approved field should be exitDateRecorded.
2. exitDateRecorded is not used as a predictive feature.
3. Every predictive event query uses only data on or before @AsOfDate.
4. Future/outcome events are excluded from model inputs.
5. Internal transfers are correctly excluded where required.
6. Death-exclusion logic is preserved where eligibility is applied.
7. No source columns were invented.
8. No lookup/mapping values were invented.
9. Business flow mappings match the reference SQL.
10. Website UAT limitation is documented.
11. Each query is standalone and independently runnable.
12. No query depends on a variable, temp table, CTE or setup from another query.
13. 36-month training history and 12-month feature window remain separate concepts.
14. Every proposed feature has a simple business meaning.
15. Leakage-prone features are visibly marked for review.

Do not do the following

Do not:

- build the final consolidated ML feature dataset
- join all features into a modelling table
- start model training
- perform final feature selection
- apply full missing-value treatment
- create Databricks/PySpark implementation
- overwrite existing SQL files
- modify behaviorial.sql

The sole purpose of this task is:

Create one business/team-review SQL file containing independently runnable standalone feature queries, with correct mappings, filters, point-in-time rules, leakage notes and business-friendly descriptions.

Stop after creating and validating:

behavioural_features_business_review.sql
