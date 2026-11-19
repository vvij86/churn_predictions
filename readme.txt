Create a new Python file directly under the existing "notebook" folder named:

"ml_mscs_mrt_contribution_features.py"

Follow ALL rules from:

".github/copilot-instructions.md"

Do not create any subfolder under "notebook".

Purpose

Build the reviewed Contribution Behaviour features for Member Retention Analytics using Databricks / PySpark.

The final grain MUST remain:

"one row per account_id per as_of_date"

The implementation must work against the reusable account-level base population created by:

"ml_mscs_mrt_base_population.py"

Do not rebuild the base population logic independently.

Reference SQL

Use this SQL file as the primary business-logic reference:

"behavioural_features_business_review.sql"

Review the Contribution Behaviour and related contribution-change logic in that file before implementing.

Do not blindly copy SQL Server syntax, table names or column names.

Map the reviewed logic to the Databricks "mscs_mrt_*" source tables.

The following SQL file exists but is NOT relevant to contribution features:

"AccountEngagementWeb_Reviewed_Features.sql"

Do not use web-engagement logic in this file.

Databricks Source

Catalog:

"mer_wealth_dev"

Schema:

"mer_wealth_landing_edge"

Primary contribution source table:

"mer_wealth_dev.mer_wealth_landing_edge.mscs_mrt_account_money_inflow"

Only use "mscs_mrt_*" source tables.

Do not use similarly named legacy/non-MRT tables.

Before implementing calculations:

- load the source with "spark.table()"
- inspect/log the actual schema
- validate the required columns
- map SQL Server reference fields to actual Databricks columns
- do not invent missing fields

If a required source field is unavailable:

- add a clear TODO/comment
- log the missing mapping
- raise an appropriate exception if the feature cannot be calculated safely

Base Population Input

Reuse the account spine produced by:

"ml_mscs_mrt_base_population.py"

The feature logic must be calculated relative to each row's:

"account_id"
"as_of_date"

Do not calculate features relative to the current system date.

IMPORTANT:
Although the current development run may use a single configured AsOfDate, write the feature logic so that it remains compatible with future multiple historical snapshots.

Therefore all date filtering must be relative to each "as_of_date", not globally hard-coded to "2024-03-31".

Feature Windows

Use point-in-time-safe windows relative to "as_of_date".

Required windows:

Trailing 12 months

Use contribution events occurring within the trailing 12 months up to and including "as_of_date".

Recent 90 days

Use contribution events in the most recent 90 days up to "as_of_date".

Prior 90 days

Use the 90-day period immediately before the recent 90-day window where required for contribution change calculations.

No event after "as_of_date" may enter any feature.

Reviewed Contribution Features

Implement the following reviewed contribution features where supported by the Databricks source schema:

- "contribution_count_12m"
- "contribution_amount_12m"
- "contribution_active_months_12m"
- "days_since_last_contribution"
- "recent_contribution_amount_90d"
- "prior_contribution_amount_90d"
- "recent_contribution_count_90d"
- "prior_contribution_count_90d"
- "contribution_change_pct_90d"
- "contribution_ceased_90d_flag"
- "employer_sg_amount_12m"
- "employer_sg_amount_90d"
- "salary_sacrifice_amount_12m"
- "salary_sacrifice_amount_90d"
- "member_voluntary_amount_12m"
- "member_voluntary_amount_90d"

Also implement the reviewed contribution-type change/cessation features where the reference SQL and Databricks source support them:

- "employer_sg_change_pct_12m"
- "employer_sg_cessation_flag"
- "salary_sacrifice_change_pct_12m"
- "salary_sacrifice_cessation_flag"
- "member_voluntary_change_pct_12m"
- "member_voluntary_cessation_flag"

Do NOT recreate these previously de-scoped duplicate features:

- "employer_sg_current_amount_12m"
- "salary_sacrifice_current_amount_12m"
- "member_voluntary_current_amount_12m"

Also do NOT create Campaign/Event contribution counters in this file.

The following were previously identified as duplicate contribution signals and must not be reintroduced:

- "contribution_event_count_12m"
- "recent_contribution_event_count_90d"

Point-in-Time Requirements

For every contribution record used:

"event/contribution date <= as_of_date"

Apply the appropriate lower boundary for each feature window.

No future contribution information may be used.

No outcome-period data may be used.

Output

Create a DataFrame named:

"contribution_features_df"

It must contain:

- "account_id"
- "as_of_date"
- reviewed contribution feature columns

Final grain MUST be:

"one account_id + one as_of_date = one row"

Do not include unnecessary raw transaction-level columns in the final output.

Join Strategy

Use the base population as the driving dataset.

Aggregate contribution records to:

"account_id + as_of_date"

before producing the final contribution feature DataFrame.

Do not allow transaction-level joins to multiply account-level rows.

Where an account has no contribution activity, preserve the account from the base population.

Handle zero versus NULL carefully:

- use zero for a genuine absence of contribution activity where business meaning supports zero
- preserve NULL where the source itself is unavailable/unknown
- do not blindly fill every NULL with zero

Change Percentage Logic

Use the reviewed SQL logic for percentage-change calculations.

Handle divide-by-zero explicitly.

Do not return infinity or NaN.

If the prior-period amount is zero, follow the reviewed business logic from "behavioural_features_business_review.sql".

Do not invent an alternative percentage definition.

Cessation Logic

Use the reviewed SQL definition for contribution cessation.

Do not infer a new definition.

Ensure the cessation flag is calculated only from information available on or before "as_of_date".

Logging and Exceptions

Follow the logging rules already established in "ml_mscs_mrt_base_population.py".

Use:

- "logger.info()" for normal pipeline stages
- "logger.warning()" for non-fatal data-quality observations
- "logger.exception()" inside exception handlers
- re-raise critical exceptions

Add INFO logging for:

- source load
- schema validation
- source column mapping
- base population load/use
- 12-month feature calculations
- recent/prior 90-day calculations
- contribution-type feature calculations
- feature aggregation
- validation
- successful completion

Do not add MLflow autologging to this feature-engineering file.

Validation

Add validations for:

- total output row count
- distinct "account_id + as_of_date"
- duplicate "account_id + as_of_date"
- null "account_id"
- null "as_of_date"
- contribution count values below zero
- contribution amount values where unexpected negatives occur
- NaN/infinite change percentages
- future contribution records entering feature calculations
- output row count versus base population row count

Critical requirements:

- duplicate "account_id + as_of_date" must be 0
- null key counts must be 0
- future contribution leakage count must be 0
- output must not contain more rows than the base population due to join multiplication

Log all validation metrics.

Raise explicit exceptions for critical failures.

Modularity

Prefer helper functions such as:

- "load_contribution_source()"
- "validate_contribution_source()"
- "build_contribution_features()"
- "validate_contribution_features()"

Keep the code readable and production-oriented.

Persistence

Do NOT save this individual feature DataFrame as a Databricks table yet.

Return/create:

"contribution_features_df"

The final consolidated feature dataset will be persisted later after all feature blocks are assembled and validated.

Important Final Check

Before finalizing the code:

1. Read ".github/copilot-instructions.md".
2. Review the Contribution Behaviour logic in "behavioural_features_business_review.sql".
3. Inspect "mscs_mrt_account_money_inflow" schema.
4. Confirm every referenced source column exists.
5. Preserve the reviewed business definitions.
6. Ensure all calculations are relative to "as_of_date".
7. Ensure final grain remains "account_id + as_of_date".
8. Do not alter "ml_mscs_mrt_base_population.py" unless absolutely required.
