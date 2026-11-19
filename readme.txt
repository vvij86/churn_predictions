Create a new Python file directly under the existing "notebook" folder named:

"ml_mscs_mrt_base_population.py"

Follow ALL development rules from:

".github/copilot-instructions.md"

Important context:

This is the first file in the Member Retention Analytics ML feature-build pipeline.

Use Databricks / PySpark.

Do not create any subfolder under "notebook".

Source

Use:

Catalog:
"mer_wealth_dev"

Schema:
"mer_wealth_landing_edge"

Primary source table:

"mer_wealth_dev.mer_wealth_landing_edge.mscs_mrt_account_summary"

Only use "mscs_mrt_*" source tables.

Do not use similarly named legacy/non-MRT tables.

Behavioural SQL References

The workspace contains two important SQL reference files:

1. "behavioural_features_business_review.sql"
2. "AccountEngagementWeb_Reviewed_Features.sql"

For this base-population file, review "behavioural_features_business_review.sql" for any relevant account population / eligibility / point-in-time assumptions.

Do not copy SQL Server table or column names blindly.

The SQL files are business-logic references only.

Always validate the actual Databricks "mscs_mrt_account_summary" schema first.

"AccountEngagementWeb_Reviewed_Features.sql" will mainly be used later when building web-engagement features and should not be implemented in this base-population file.

Purpose

Build the reusable account-level base population / account spine that will be used by all subsequent feature modules.

Final grain MUST be:

"one row per account_id per as_of_date"

Final DataFrame name:

"base_population_df"

Do NOT create behavioural features in this file.

Do NOT create model training logic.

Do NOT create churn probability or drivers.

Do NOT persist a Databricks feature table yet.

Required Configuration

Create configurable constants near the top:

"SOURCE_CATALOG = "mer_wealth_dev""

"SOURCE_SCHEMA = "mer_wealth_landing_edge""

"ACCOUNT_SUMMARY_TABLE = "mscs_mrt_account_summary""

"HISTORICAL_START_DATE = "2023-04-01""

Define "AS_OF_DATE" as a configurable parameter rather than repeating a hard-coded value throughout the code.

Build the fully qualified source table name from the configuration.

Schema Validation

Load the source using "spark.table()".

Before implementing transformations:

- print/display the schema
- inspect the actual column names
- identify available equivalents for:
  - account ID
  - member/reference ID
  - customer ID
  - fund ID
  - reporting/snapshot date
  - exit date
  - exit type
  - date of death
  - other fields genuinely required for the account spine

Do not invent columns.

If a required mapping cannot be established from the actual Databricks table:

- add a clear TODO
- identify what needs clarification
- do not fabricate a replacement

Base Population Logic

Create a reusable account-level population using only information available on or before "as_of_date".

Historical source availability begins from:

"2023-04-01"

Where supported by the actual source and agreed logic:

- exclude deceased records
- maintain point-in-time correctness
- prevent future/outcome leakage
- preserve valid historical account records

Do not use outcome-period information as feature/input data.

If multiple source records can exist for the same account and AsOfDate, use deterministic point-in-time logic to select the correct record.

Do not simply call "dropDuplicates()" without explaining the duplicate source condition and selection logic.

Output Columns

Where available, standardize identifiers to snake_case and include:

"account_id"

"member_id"

"customer_id"

"fund_id"

"as_of_date"

Only include additional base fields if they are genuinely required for downstream feature logic or eligibility.

Do not add behavioural feature columns.

Modularity

Prefer functions such as:

"load_account_summary()"

"build_base_population()"

"validate_base_population()"

Keep the implementation production-readable and reusable.

Validation

At the end, validate:

- total row count
- distinct account_id count
- distinct account_id + as_of_date count
- duplicate account_id + as_of_date count
- null account_id count
- null as_of_date count
- minimum as_of_date
- maximum as_of_date

Critical requirements:

- duplicate "account_id + as_of_date" count must be 0
- null "account_id" count must be 0
- null "as_of_date" count must be 0

Use clear assertions or validation failures for critical conditions.

Display a small development sample of "base_population_df".

Important

Do not implement contribution, rollover, FUM, investment, insurance, campaign, web, helpline or other behavioural features yet.

This file is only the reusable account-level spine.

Do not modify unrelated files in the shared repository.

Before finalizing the code, confirm that every referenced source column actually exists in:

"mer_wealth_dev.mer_wealth_landing_edge.mscs_mrt_account_summary"
