Read member_retention_ml_copilot_instructions.md, behavioural_features_business_review.sql, MemberRetention_01-AccountBase_v006.sql, and MemberRetention_03-MemberRetentionMetrics_v005.sql.

Do not restart from scratch. Continue from the current behavioural_features_business_review.sql and update only the relevant standalone feature sections.

Business specifically discussed the following three areas as potentially useful for ML. Review the exact existing logic in MemberRetention_01-AccountBase_v006.sql and add/refine standalone behavioural feature queries where appropriate.

1. Rollover Destination Features

Review edgeSource.accountRolloverPayment and the business SQL logic around:

- rolloverDestinationName
- rolloverDestinationType

Assess whether these fields can provide useful behavioural churn-risk features.

Possible features to consider:

- distinct rollover destination count in the last 12 months
- most recent rollover destination type
- external rollover destination indicator
- repeated external rollover destination activity
- rollover destination type frequency

Do not use raw rolloverDestinationName directly if it creates high cardinality/noise.

Prefer grouped and business-friendly features.

Keep these behaviours separate:

- partial rollover
- external rollover
- rollover in
- internal transfer

Internal transfers must not be treated as churn-risk external rollover activity.

Any feature that is too close to full account exit/churn must be marked:

LEAKAGE REVIEW REQUIRED

Use only source columns and mappings supported by the DDL/business SQL.

2. Inflow Signals / Contribution Change Patterns

Locate and review the section in MemberRetention_01-AccountBase_v006.sql corresponding to:

12.1 Inflow signals (SG / SalSac / MV / Roll-in)

Review the existing logic for fields such as:

- EmployerSG_baseline_amount
- EmployerSG_recent_amount
- SalSac_baseline_amount
- SalSac_recent_amount
- MemVol_baseline_amount
- MemVol_recent_amount
- rollin_amount_12m
- SalSac_previous_fy_amount
- SalSac_current_fy_amount
- MemVol_previous_fy_amount
- MemVol_current_fy_amount

Trace the exact mappings and filters used by the business SQL.

Use MemberRetention_03-MemberRetentionMetrics_v005.sql where required to confirm contribution/flow mappings.

Create useful standalone feature queries that represent behavioural changes, not just raw totals.

Possible features to consider:

- Employer SG recent amount
- Employer SG baseline amount
- Employer SG recent-vs-baseline change
- Salary Sacrifice recent amount
- Salary Sacrifice baseline amount
- Salary Sacrifice recent-vs-baseline change
- Member Voluntary recent amount
- Member Voluntary baseline amount
- Member Voluntary recent-vs-baseline change
- contribution drop signal
- contribution spike signal
- contribution inactivity / cessation signal
- Salary Sacrifice current FY vs previous FY change
- Member Voluntary current FY vs previous FY change
- rollover-in amount in the last 12 months

Keep these contribution types separate:

- Employer SG
- Salary Sacrifice
- Member Voluntary
- Rollover In

Do not mix in:

- internal transfers
- insurance claim proceeds
- adjustments
- unrelated inflows

Do not invent spike/drop thresholds.

If the business SQL does not already define the threshold, mark:

BUSINESS CONFIRMATION REQUIRED

Prefer useful change/trend signals over creating too many raw features.

3. Low Balance and Advice Engagement

Locate and review the relevant business SQL section around:

12.4 Web login and advice engagement events

Specifically trace the logic for:

- low_balance_flag
- advice_helpline_engagement_12m_flag

Identify the original physical source tables and source columns used to create these fields.

If the required logic can be reproduced using the approved ML source tables, add standalone queries for:

- low balance indicator
- advice helpline engagement in the last 12 months

For advice_helpline_engagement_12m_flag, use only activity available on or before @AsOfDate.

If the exact business logic requires a source outside the approved ML table scope, do not invent an alternative.

Mark it clearly as:

REVIEW REQUIRED - ADDITIONAL SOURCE DEPENDENCY

Also check whether the advice-engagement logic overlaps with the existing helpline features. If so, keep only the feature that adds distinct business information and document the relationship.

Standalone Query Requirements

Update only:

behavioural_features_business_review.sql

Each added query must remain independently runnable.

Each standalone query must contain its own required parameters, including:

DECLARE @AsOfDate DATE = '2024-03-31';

and its own feature-window parameters where required.

Do not depend on variables, CTEs or temp tables created by a previous standalone query.

Maintain all current approved controls:

- approved FundScope/databaseCode filtering
- fundJoinDate <= @AsOfDate
- use exitDateRecorded, not exitDate
- exclude accounts already exited as of AsOfDate
- death exclusion
- internal-transfer handling
- point-in-time safety
- no future events
- no target leakage
- default 12-month feature window
- 36-month overall training history is separate from the feature window

Before each new feature/query block use the existing documentation format:

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

Use only these recommendation values:

- INCLUDE
- REVIEW REQUIRED
- EXCLUDE
- INCLUDE PENDING PROD VALIDATION

Noise Reduction

For these new features:

- avoid raw high-cardinality fields
- prefer grouped/interpretable signals
- avoid duplicate features
- exclude system/admin noise
- exclude internal transfers where relevant
- exclude post-AsOfDate events
- exclude outcome/target events
- do not use exit-related information as a predictive feature
- do not invent business mappings or thresholds

If logic is uncertain, mark it for business review instead of guessing.

Final Validation

Before finishing, confirm:

- rollover destination features were reviewed
- inflow signal / contribution-change features were reviewed
- low-balance and advice-engagement features were reviewed
- all source columns come from the DDL/reference SQL
- no unsupported table or column was invented
- no future information is used
- no target leakage is introduced
- FundScope filtering is still present in executable SQL
- unrelated existing feature queries were not changed
- the final source-usage summary is updated if any new approved source is used

Do not build the final consolidated feature dataset.

Do not start model training.

Stop after updating and validating behavioural_features_business_review.sql.
