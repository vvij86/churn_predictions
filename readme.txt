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
- identify source/effective/update date required for point-in-time selection
- identify the actual source field required to determine direct investment exposure

Do not invent unavailable fields.

If a reviewed feature cannot be mapped safely:

- log the issue
- add a clear TODO/comment
- raise an exception where the feature cannot be calculated correctly

Base Population

Reuse:

"base_population_df"

from:

"ml_mscs_mrt_base_population.py"

All calculations must be relative to:

"account_id"
"as_of_date"

Do not calculate investment position using the current system date.

The implementation must remain compatible with future multiple historical AsOfDate snapshots.

Reviewed Investment Features

Implement ONLY the reviewed Investment Behaviour / Position features below:

1. "investment_option_count_asof"

Description:
Number of distinct investment options held by the account as at the "as_of_date".

2. "total_investment_value_asof"

Description:
Total latest investment value across all valid investment options as at the "as_of_date".

3. "direct_investment_flag"

Description:
Flag indicating whether the account has any direct-investment exposure as at the "as_of_date".

Do not introduce additional Investment Behaviour features unless explicitly requested.

Point-in-Time Investment Selection

All investment features must be point-in-time safe.

For each "account_id + as_of_date":

- use only investment records available on or before "as_of_date"
- identify the latest valid position for each investment option as at that date
- exclude future investment records
- aggregate the selected option-level positions back to account level
- do not allow historical investment rows to inflate the final feature values

Do not use the current/latest overall investment record if it occurred after the relevant "as_of_date".

investment_option_count_asof

Calculate:

"investment_option_count_asof"

as the number of distinct valid investment options held by the account at the point-in-time snapshot.

Use only the latest valid position per investment option as at "as_of_date".

Follow the reviewed SQL logic from:

"behavioural_features_business_review.sql"

Do not count historical duplicate positions as separate options.

total_investment_value_asof

Calculate:

"total_investment_value_asof"

as the total latest investment value across all valid investment options held by the account as at "as_of_date".

IMPORTANT:

The underlying business definition must remain consistent with the FUM/current investment-value logic already implemented in:

"ml_mscs_mrt_rollover_features.py"

The rollover feature pipeline may internally refer to this value as current account FUM for percentage calculations.

Do NOT introduce a different investment/FUM calculation in this file.

Reuse or refactor the already validated point-in-time investment-value logic where practical.

The final reviewed Investment Behaviour feature name MUST be:

"total_investment_value_asof"

Do NOT rename this output to:

"current_account_fum_amount"

inside "investment_features_df".

If shared helper logic is required, reuse it without changing the validated rollover percentage results.

direct_investment_flag

Calculate:

"direct_investment_flag"

using the reviewed business definition/source mapping in:

"behavioural_features_business_review.sql"

The output should represent whether the account has any direct-investment exposure at "as_of_date".

Use an integer/Boolean-safe representation consistent with project standards, for example:

- "1" = Yes
- "0" = No

Do not infer a new direct-investment rule if the required source field/mapping is unavailable.

If mapping cannot be confirmed:

- add a TODO
- log the issue
- do not fabricate a value

Output

Create final DataFrame:

"investment_features_df"

It must contain exactly these keys/features:

- "account_id"
- "as_of_date"
- "investment_option_count_asof"
- "total_investment_value_asof"
- "direct_investment_flag"

Final grain:

"one account_id + one as_of_date = one row"

Accounts with no valid investment position must still remain present from the base population.

Handle NULL versus zero carefully.

Do not blindly replace unknown/unavailable investment values with zero unless the business meaning supports zero.

Logging and Exception Handling

Follow the same logging pattern already used in:

- "ml_mscs_mrt_base_population.py"
- "ml_mscs_mrt_contribution_features.py"
- "ml_mscs_mrt_rollover_features.py"

Use:

- "logger.info()" for normal execution
- "logger.warning()" for non-fatal data-quality observations
- "logger.exception()" inside exception handlers
- re-raise critical exceptions

Log major stages:

- loading base population
- loading investment source
- source schema validation
- source field mapping
- point-in-time investment selection
- investment option count calculation
- total investment value calculation
- direct investment flag calculation
- final aggregation
- validation
- successful completion

Do NOT add MLflow autologging.

Spark Session Handling

Use the same reusable-module pattern already implemented in the previous ML files.

Pass the active SparkSession explicitly.

Do not depend on a module-global Databricks "spark" object when imported.

Importing this module must not automatically execute the pipeline.

Direct Databricks job execution may run the pipeline using the same execution pattern already established in the previous files.

Validation

Validate and log:

- base population row count
- output row count
- distinct "account_id + as_of_date" count
- duplicate "account_id + as_of_date" count
- null "account_id"
- null "as_of_date"
- negative "investment_option_count_asof"
- count of NULL "total_investment_value_asof"
- count of zero "total_investment_value_asof"
- count of negative "total_investment_value_asof"
- future investment leakage count
- distribution of "direct_investment_flag"
- invalid values in "direct_investment_flag"
- unexpected row multiplication

Critical checks:

- duplicate grain count = 0
- null key counts = 0
- future investment leakage count = 0
- output row count must not exceed the base population because of join multiplication
- "investment_option_count_asof" must not be negative
- "direct_investment_flag" must contain only valid expected values

Negative investment/FUM values should be logged for review and not silently modified unless the reviewed business logic explicitly requires it.

Modularity

Prefer reusable helper functions such as:

- "load_investment_source()"
- "validate_investment_source()"
- "build_point_in_time_investment_position()"
- "build_investment_features()"
- "validate_investment_features()"
- "run_investment_feature_pipeline()"

If reusable FUM logic already exists in:

"ml_mscs_mrt_rollover_features.py"

reuse/refactor it where practical instead of maintaining two different definitions.

Do not create circular imports.

Persistence

Do NOT save this individual feature DataFrame as a Databricks table yet.

Final output must be:

"investment_features_df"

The consolidated feature dataset will be persisted later after all reviewed feature blocks are assembled and validated.

Final Check

Before finalizing:

1. Read ".github/copilot-instructions.md".
2. Review the Investment Behaviour / Position section in "behavioural_features_business_review.sql".
3. Inspect the actual schema of "mscs_mrt_account_investments".
4. Implement only these reviewed features:
   - "investment_option_count_asof"
   - "total_investment_value_asof"
   - "direct_investment_flag"
5. Ensure "total_investment_value_asof" uses the same underlying point-in-time FUM logic already validated for rollover features.
6. Confirm every referenced source column exists.
7. Ensure all investment records used are on or before "as_of_date".
8. Keep final grain at "account_id + as_of_date".
9. Do not modify contribution logic.
10. Do not change validated rollover business logic.
11. Do not modify unrelated Data Engineering / Power BI files.
