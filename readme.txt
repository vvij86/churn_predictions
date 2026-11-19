Create a new Python file directly under the existing "notebook" folder named:

"ml_mscs_mrt_rollover_features.py"

Follow ALL rules from:

".github/copilot-instructions.md"

Do not create any subfolder under "notebook".

Purpose

Build the reviewed Partial Rollover / Withdrawal behavioural features for Member Retention Analytics using Databricks / PySpark.

Final grain MUST remain:

"one row per account_id per as_of_date"

Reuse the account-level spine from:

"ml_mscs_mrt_base_population.py"

Do not independently rebuild base-population logic.

Reference SQL

Use:

"behavioural_features_business_review.sql"

as the primary business-logic reference for Partial Rollover / Withdrawal behaviour.

Review the existing reviewed SQL logic before implementation.

Do not blindly copy SQL Server syntax, table names or column names.

Map the reviewed logic to the Databricks "mscs_mrt_*" tables.

Do not use:

"AccountEngagementWeb_Reviewed_Features.sql"

for rollover logic.

Databricks Sources

Catalog:

"mer_wealth_dev"

Schema:

"mer_wealth_landing_edge"

Primary rollover source:

"mer_wealth_dev.mer_wealth_landing_edge.mscs_mrt_account_rollover_payment"

FUM/investment source where required:

"mer_wealth_dev.mer_wealth_landing_edge.mscs_mrt_account_investments"

Only use "mscs_mrt_*" tables.

Before implementing logic:

- inspect/log the actual schemas
- validate required columns
- identify account ID
- identify rollover/payment event date
- identify amount field
- identify internal-transfer flag
- identify rollover/withdrawal type fields required by reviewed SQL
- identify investment-value fields required for current FUM

Do not invent unavailable fields.

If a required field cannot be mapped safely:

- add a clear TODO/comment
- log the missing mapping
- raise an explicit exception where the feature cannot be calculated correctly

Base Population

Reuse:

"base_population_df"

from:

"ml_mscs_mrt_base_population.py"

All calculations MUST be relative to each row's:

"account_id"
"as_of_date"

Do not use the current system date.

Write the implementation so it remains compatible with future multiple historical AsOfDate snapshots.

Reviewed Rollover Features

Implement these reviewed features:

- "partial_rollover_count_12m"
- "partial_rollover_amount_12m"
- "days_since_last_partial_rollover"
- "recent_partial_rollover_count_90d"
- "recent_partial_rollover_amount_90d"
- "current_account_fum_amount"
- "partial_rollover_pct_12m"
- "recent_partial_rollover_pct_90d"

Partial Rollover Business Rules

Follow the reviewed SQL definition for identifying partial rollover / partial withdrawal activity.

IMPORTANT:

- Internal transfers must be excluded.
- Do not treat internal transfers as behavioural external withdrawals.
- Do not treat a full rollover/account closure churn event as a partial rollover feature.
- Preserve the reviewed business logic from "behavioural_features_business_review.sql".

If the Databricks internal-transfer field is BOOLEAN, use Boolean-safe logic.

Do not compare Boolean fields with integer values such as "1" or "0".

Feature Windows

Trailing 12 months

Use qualifying partial rollover events occurring within the trailing 12 months up to and including "as_of_date".

Recent 90 days

Use qualifying partial rollover events occurring within the most recent 90 days up to and including "as_of_date".

No event after "as_of_date" may enter any feature.

Recency

Calculate:

"days_since_last_partial_rollover"

using the latest qualifying partial rollover date on or before "as_of_date".

If the account has never had a qualifying partial rollover in the applicable history, preserve NULL unless the reviewed SQL specifies another treatment.

Current Account FUM

Derive:

"current_account_fum_amount"

from:

"mscs_mrt_account_investments"

using point-in-time-safe logic.

Use the latest valid investment position available on or before each "as_of_date".

If there are multiple investment options for an account, aggregate the appropriate latest investment values to account level according to the reviewed SQL/reference logic.

Do not use investment records after "as_of_date".

Do not duplicate account rows.

Rollover Percentage Logic

Use the reviewed denominator formula:

"partial_rollover_pct_12m = partial_rollover_amount_12m / (current_account_fum_amount + partial_rollover_amount_12m)"

and:

"recent_partial_rollover_pct_90d = recent_partial_rollover_amount_90d / (current_account_fum_amount + recent_partial_rollover_amount_90d)"

Only calculate percentage values where the denominator is valid/positive according to the reviewed logic.

Do NOT use:

"partial_rollover_amount / current_fum"

as the denominator.

That older formulation produced values above 100% and must not be reintroduced.

Handle zero, NULL and invalid denominators explicitly.

Do not return NaN or infinity.

Output

Create final DataFrame:

"rollover_features_df"

It must contain:

- "account_id"
- "as_of_date"
- "partial_rollover_count_12m"
- "partial_rollover_amount_12m"
- "days_since_last_partial_rollover"
- "recent_partial_rollover_count_90d"
- "recent_partial_rollover_amount_90d"
- "current_account_fum_amount"
- "partial_rollover_pct_12m"
- "recent_partial_rollover_pct_90d"

Final grain:

"one account_id + one as_of_date = one row"

Accounts with no rollover activity must remain present because the base population is the driving dataset.

Logging and Exception Handling

Follow the same logging pattern used in:

"ml_mscs_mrt_base_population.py"
and
"ml_mscs_mrt_contribution_features.py"

Use:

- "logger.info()" for normal progress
- "logger.warning()" for non-fatal data-quality observations
- "logger.exception()" inside exception handlers
- re-raise critical exceptions

Log major stages:

- loading rollover source
- loading investment/FUM source
- schema validation
- field mapping
- partial rollover filtering
- internal-transfer exclusion
- 12-month calculations
- recent 90-day calculations
- current FUM derivation
- percentage calculations
- final aggregation
- validation
- successful completion

Do NOT add MLflow autologging.

Spark Session Handling

Follow the reusable-module pattern already corrected in the previous files.

Do not depend on a module-global Databricks "spark" object when imported.

Pass the active SparkSession explicitly to reusable pipeline functions.

Importing this module must not automatically execute the pipeline.

Direct Databricks job execution may run the pipeline under an appropriate execution guard.

Validation

At minimum validate and log:

- base population row count
- output row count
- distinct "account_id + as_of_date"
- duplicate "account_id + as_of_date"
- null "account_id"
- null "as_of_date"
- negative rollover counts
- unexpected negative rollover amounts
- internal-transfer records included in qualifying rollover features
- future rollover leakage count
- future investment/FUM leakage count
- NaN/infinite percentage values
- "partial_rollover_pct_12m < 0"
- "partial_rollover_pct_12m > 1"
- "recent_partial_rollover_pct_90d < 0"
- "recent_partial_rollover_pct_90d > 1"

Critical requirements:

- duplicate grain count = 0
- null key counts = 0
- future leakage counts = 0
- internal-transfer leakage count = 0
- percentage values must not exceed 1 or fall below 0
- row count must not increase because of join multiplication

Raise explicit exceptions for critical validation failures.

Modularity

Prefer helper functions such as:

- "load_rollover_source()"
- "load_investment_source()"
- "validate_source_columns()"
- "build_current_fum()"
- "build_rollover_features()"
- "validate_rollover_features()"
- "run_rollover_feature_pipeline()"

Persistence

Do NOT save this individual DataFrame as a Databricks table yet.

The output should remain:

"rollover_features_df"

The consolidated feature table will be persisted later after all approved feature blocks are assembled.

Final Check

Before finalizing:

1. Read ".github/copilot-instructions.md".
2. Review Partial Rollover logic in "behavioural_features_business_review.sql".
3. Inspect the actual schemas of "mscs_mrt_account_rollover_payment" and "mscs_mrt_account_investments".
4. Confirm every referenced source column exists.
5. Preserve reviewed internal-transfer exclusions.
6. Preserve point-in-time safety.
7. Use the approved rollover percentage denominator formula.
8. Keep final grain at "account_id + as_of_date".
9. Do not modify contribution feature logic.
10. Do not modify unrelated Data Engineering / Power BI files.
