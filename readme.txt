Create a new Python file directly under the existing "notebook" folder named:

"ml_mscs_mrt_investment_features.py"

Follow ALL rules from:

".github/copilot-instructions.md"

Do not create any subfolder under "notebook".

Purpose

Build the reviewed Investment Behaviour / Position features for Member Retention Analytics using Databricks / PySpark.

Final grain MUST remain:

"one row per account_id per as_of_date"

Reuse the account-level base population from:

"ml_mscs_mrt_base_population.py"

Do not independently rebuild the base-population logic.

Reference SQL

Use:

"behavioural_features_business_review.sql"

as the primary business-logic reference for Investment Behaviour.

Review the Investment Behaviour / Position section before implementing.

Do not blindly copy SQL Server syntax, table names or column names.

Map the reviewed logic to Databricks "mscs_mrt_*" tables.

Databricks Source

Catalog:

"mer_wealth_dev"

Schema:

"mer_wealth_landing_edge"

Primary source:

"mer_wealth_dev.mer_wealth_landing_edge.mscs_mrt_account_investments"

Only use "mscs_mrt_*" source tables.

Before implementing:

- inspect/log the actual source schema
- identify account ID
- identify investment option / investment identifier
- identify investment value / balance field
- identify source date / effective date / update date required for point-in-time selection
- identify any field required to derive direct investment status

Do not invent unavailable fields.

If a reviewed feature cannot be mapped safely:

- log the issue
- add a clear TODO/comment
- raise an exception if the feature cannot be calculated correctly

Base Population

Reuse:

"base_population_df"

from:

"ml_mscs_mrt_base_population.py"

All calculations must be relative to:

"account_id"
"as_of_date"

Do not calculate investment position using current system date.

The implementation must remain compatible with future multiple AsOfDate snapshots.

Reviewed Investment Features

Implement the reviewed features:

- "current_account_fum_amount"
- "investment_option_count_asof"
- "direct_investment_flag"

Do not create additional investment features unless they are explicitly present in the reviewed SQL/reference logic.

Current FUM Logic

"current_account_fum_amount" must use the SAME business definition already used in:

"ml_mscs_mrt_rollover_features.py"

Do not introduce a different FUM calculation.

Reuse/refactor the existing FUM logic where practical.

Requirements:

- use only investment records available on or before "as_of_date"
- select the latest valid investment position per investment option/account where required
- aggregate the latest valid option-level values to account level
- do not use records after "as_of_date"
- do not allow multiple investment rows to multiply the final account-level grain

If the rollover feature file already contains a reusable FUM helper function, reuse it rather than duplicating business logic.

If refactoring is required, move/reuse the logic carefully without changing the already validated rollover results.

Investment Option Count

Calculate:

"investment_option_count_asof"

as the number of valid investment options held by the account as of "as_of_date", according to the reviewed SQL logic.

Use the point-in-time selected investment position, not all historical investment records.

Direct Investment Flag

Calculate:

"direct_investment_flag"

using the reviewed source field/business definition from "behavioural_features_business_review.sql".

Do not infer a new rule.

If the required Databricks field is not available, add a TODO and clearly identify the missing mapping.

Output

Create final DataFrame:

"investment_features_df"

It must contain:

- "account_id"
- "as_of_date"
- "current_account_fum_amount"
- "investment_option_count_asof"
- "direct_investment_flag"

Final grain:

"one account_id + one as_of_date = one row"

Accounts with no valid investment position should remain present from the base population.

Handle NULL versus zero carefully.

Do not blindly convert unavailable FUM to zero unless supported by business meaning.

Logging and Exception Handling

Follow the same logging pattern used in:

- "ml_mscs_mrt_base_population.py"
- "ml_mscs_mrt_contribution_features.py"
- "ml_mscs_mrt_rollover_features.py"

Use:

- "logger.info()" for normal execution
- "logger.warning()" for non-fatal data-quality observations
- "logger.exception()" for failures
- re-raise critical exceptions

Log major stages:

- source load
- schema validation
- source field mapping
- point-in-time investment selection
- current FUM calculation
- investment option count calculation
- direct investment flag calculation
- final feature aggregation
- validation
- successful completion

Do not add MLflow autologging.

Spark Session Handling

Follow the reusable-module pattern already implemented.

Pass the active SparkSession explicitly.

Do not rely on a module-global Databricks "spark" object when the file is imported.

Importing the module must not automatically execute the pipeline.

Validation

Validate and log:

- base population row count
- output row count
- distinct "account_id + as_of_date"
- duplicate "account_id + as_of_date"
- null account_id
- null as_of_date
- negative "investment_option_count_asof"
- unexpected negative FUM values
- future investment records used
- row multiplication
- distribution/count of "direct_investment_flag"
- count of NULL FUM values
- count of zero FUM values
- count of negative FUM values

Critical checks:

- duplicate grain count = 0
- null key counts = 0
- future investment leakage count = 0
- output row count must not exceed base population due to joins

Negative FUM values should be logged for review; do not silently alter them unless the reviewed business logic explicitly requires it.

Modularity

Prefer helper functions such as:

- "load_investment_source()"
- "validate_investment_source()"
- "build_point_in_time_investment_position()"
- "build_current_fum()"
- "build_investment_features()"
- "validate_investment_features()"
- "run_investment_feature_pipeline()"

Persistence

Do NOT save this individual feature DataFrame as a Databricks table yet.

Final output:

"investment_features_df"

The consolidated feature dataset will be persisted later after all feature blocks are assembled and validated.

Final Check

Before finalizing:

1. Read ".github/copilot-instructions.md".
2. Review Investment Behaviour logic in "behavioural_features_business_review.sql".
3. Inspect the actual "mscs_mrt_account_investments" schema.
4. Reuse the same FUM definition already validated in "ml_mscs_mrt_rollover_features.py".
5. Confirm every referenced source column exists.
6. Ensure all investment records used are on or before "as_of_date".
7. Keep the final grain at "account_id + as_of_date".
8. Do not modify contribution logic.
9. Do not alter validated rollover business logic.
10. Do not modify unrelated Data Engineering / Power BI files.
