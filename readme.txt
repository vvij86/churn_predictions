Read member_retention_ml_copilot_instructions.md and continue from the existing behavioural_features_business_review.sql.

Do not restart from scratch.

Update only the existing standalone query for edgeSource.accountEngagementWorkflow.

Do not modify any other feature query.

Business feedback is that the workflow table contains a lot of operational/system noise, so the query should not simply count every workflow row. The requirement is to reduce noise and retain only workflow activity that is potentially meaningful for churn prediction.

First inspect the available workflow fields and distinct values, especially:

- jobCode
- jobDescription
- jobSourceDescription
- jobSourceID
- jobCompletedFlag
- jobStartDate
- jobDueDate
- jobCompletionDate

Use the existing DDL, EDA files and business reference SQL to understand the fields.

Before changing the feature logic, profile the workflow categories and identify which records look like:

- member-driven/member-service activity
- genuine account servicing activity
- unresolved/open member requests
- follow-up activity
- administrative processing
- reconciliation activity
- batch/system-generated processing
- reporting/technical jobs
- other operational noise

From the sample data, examples such as:

- Web Link - Address/Name Change Confirmation
- Reconciliation - Cashflow Exceptions

should not automatically be treated equally. Review their source/job type and decide whether they represent useful member behaviour or operational noise.

Do not invent business exclusions. Where the meaning is uncertain, classify it as:

REVIEW REQUIRED

Required output

Replace the current broad workflow aggregation with a cleaner standalone query that focuses on meaningful workflow activity.

Prefer features such as:

- meaningful_workflow_count_12m
- completed_meaningful_workflow_count_12m
- open_meaningful_workflow_count_asof
- days_since_last_meaningful_workflow
- recent_meaningful_workflow_count_90d
- repeat_meaningful_workflow_flag

If useful, also create separate counts for a small number of clearly interpretable workflow groups, such as:

- member service / account change
- advice/support
- unresolved/open cases
- other useful member-facing workflows

Do not create dozens of job-code dummy features at this stage.

Noise reduction rules

Exclude or flag for exclusion workflow records that are clearly:

- reconciliation-only
- technical/system processing
- reporting jobs
- batch processing
- purely administrative back-office jobs
- duplicate/repeated technical records
- events with no clear member behavioural meaning

However, only hard-code exclusions when supported by the observed jobDescription, jobSourceDescription, DDL/EDA or business reference logic.

For anything ambiguous, document it as:

BUSINESS CONFIRMATION REQUIRED

Preserve existing controls

Keep all existing approved logic unchanged:

- standalone independently runnable query
- own @AsOfDate
- own @FeatureStartDate
- own @Recent90Start
- FundScope through accountSummary.databaseCode
- fundJoinDate <= @AsOfDate
- exitDateRecorded, not exitDate
- death exclusion
- no post-AsOfDate workflow activity
- 12-month feature window
- no target leakage

Add a workflow profiling section before the final query

Add a small review query that outputs:

- jobCode
- jobDescription
- jobSourceDescription
- jobCompletedFlag
- row count
- distinct account count
- proposed classification: INCLUDE, EXCLUDE, or REVIEW REQUIRED
- reason

This profiling output is for business review only.

Then update the actual workflow feature query to use only the categories marked INCLUDE.

If there are no categories that can be safely hard-coded as INCLUDE from existing evidence, do not guess. Keep the feature query in REVIEW REQUIRED status and clearly show the proposed categories for business confirmation.

Update only the workflow section in:

behavioural_features_business_review.sql

Do not change helpline, website, contribution, money-flow, rollover, investment, insurance, campaign or other feature queries.

Stop after updating and validating the workflow section.
