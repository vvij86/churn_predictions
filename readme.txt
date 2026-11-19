Member Retention Analytics - ML Development Instructions

1. General Development Rules

- This repository is shared with Data Engineering / Power BI development.
- Do not modify unrelated Data Engineering or Power BI files.
- All ML Python files must start with:

"ml_mscs_mrt_"

- Do not create any subfolders under the existing "notebook" folder.
- Keep all ML Python files directly under the "notebook" folder.
- Use PySpark / Databricks Spark DataFrames for the main feature engineering pipeline.
- Do not use Pandas for large-scale feature engineering unless explicitly required for a small local operation.
- Do not create mock or sample source data unless explicitly requested.

2. Databricks Source

Source catalog:

"mer_wealth_dev"

Source schema:

"mer_wealth_landing_edge"

Use only the ML-related Databricks landing tables that follow the naming convention:

"mscs_mrt_*"

Examples include:

- "mscs_mrt_account_summary"
- "mscs_mrt_account_money_inflow"
- "mscs_mrt_account_rollover_payment"
- "mscs_mrt_account_investments"
- "mscs_mrt_account_insurance_current"
- "mscs_mrt_account_engagement_web"
- "mscs_mrt_account_engagement_helpline"
- "mscs_mrt_campaign_events"
- "mscs_mrt_campaign_event_details"
- "mscs_mrt_customer_mapping"
- "mscs_mrt_customer_summary"

Do not use similarly named legacy/non-MRT tables unless explicitly requested.

Always inspect the actual Databricks source schema before implementing logic.

Do not assume that SQL Server and Databricks column names are identical.

3. Mandatory Behavioural SQL Reference Files

The following existing standalone SQL files contain previously developed/reviewed behavioural feature logic and MUST be used as business-logic references when implementing corresponding Databricks feature logic:

1. "behavioural_features_business_review.sql"

2. "AccountEngagementWeb_Reviewed_Features.sql"

These files are reference implementations from the earlier SQL Server development.

When implementing features in Databricks:

- Review the relevant logic in these SQL files first.
- Preserve the existing reviewed feature definitions, calculations, date windows, exclusions and business rules where applicable.
- Do not blindly copy SQL Server table names.
- Do not blindly copy SQL Server column names.
- Do not blindly convert SQL syntax without validating the Databricks source.
- Map the existing logic to the appropriate "mscs_mrt_*" Databricks tables.
- Validate the actual Databricks schemas before referencing columns.
- If a required SQL Server field is not available in Databricks, do not invent or approximate it.
- Add a clear TODO/comment identifying the missing mapping or clarification required.
- Do not introduce new business rules unless explicitly requested.

Reference SQL Purpose

"behavioural_features_business_review.sql"

Use this as the primary reference for reviewed behavioural feature logic including, where applicable:

- contribution behaviour
- inflow/change behaviour
- partial rollover behaviour
- investment behaviour
- insurance behaviour
- campaign/event behaviour
- helpline behaviour
- other behavioural feature blocks contained in the file

"AccountEngagementWeb_Reviewed_Features.sql"

Use this specifically as the reference for reviewed AccountEngagementWeb / digital behavioural feature logic.

Do not use outcome or future information such as ExitDate from web request parameters as predictive features.

4. Modelling Grain

The mandatory ML feature grain is:

"one row per account_id per as_of_date"

Every feature module must preserve this grain.

Lower-grain records such as:

- transactions
- contributions
- rollovers
- campaign events
- web events
- helpline interactions
- investment positions

must be aggregated appropriately before joining to the account-level dataset.

Never allow feature joins to multiply the account-level rows.

5. Historical and Point-in-Time Rules

Historical source availability starts from:

"2023-04-01"

All feature calculations must be point-in-time safe.

Features may use only information available on or before:

"as_of_date"

No information after "as_of_date" may be used in predictive features.

Prevent outcome leakage.

Use deterministic point-in-time logic when multiple source records exist.

Do not use "dropDuplicates()" merely to hide duplicate records without understanding why duplicates occurred.

6. Feature Windows

Where required by the reviewed feature logic, use:

- trailing 12-month feature window
- recent 90-day feature window
- prior 90-day window where required

All windows must be calculated relative to "as_of_date".

Do not use current system date as a replacement for "as_of_date".

7. Feature Module Output Standard

Each individual feature module should produce:

- "account_id"
- "as_of_date"
- feature columns belonging to that module

The result from every feature module must contain no duplicate:

"account_id + as_of_date"

Intermediate feature DataFrames do not need to be persisted unless specifically required.

8. Feature Dataset Persistence

Do not persist every individual feature block.

After all approved feature blocks are assembled and validated, persist one consolidated feature dataset in the DEV environment.

The consolidated feature dataset will become the reusable source for downstream modelling-input preparation.

The persisted dataset must maintain:

"one row per account_id per as_of_date"

9. Validation Requirements

Every feature module should include appropriate validation.

At minimum validate:

- total row count
- distinct account count
- duplicate "account_id + as_of_date"
- null account IDs
- null AsOfDates
- date ranges
- unexpected negative values
- percentage/rate boundaries
- feature min/max values where useful
- unexpected row multiplication
- post-AsOfDate leakage

Critical grain or leakage failures must not be silently ignored.

10. Coding Standards

- Use snake_case for ML output column names.
- Use descriptive variable names.
- Keep source catalog/schema/table names configurable where appropriate.
- Prefer reusable helper functions.
- Add concise docstrings and comments.
- Avoid large monolithic transformation blocks when logical functionality can be separated.
- Do not unnecessarily cache large DataFrames.
- Do not collect large Spark datasets to the driver.
- Do not convert large Spark datasets to Pandas.
- Use Spark-native transformations wherever practical.

11. Base Population

The ML feature pipeline must be anchored to a common reusable account-level base population.

The primary source for the initial base population is:

"mer_wealth_dev.mer_wealth_landing_edge.mscs_mrt_account_summary"

The base population must maintain:

"one account_id + one as_of_date = one row"

Behavioural features should subsequently join to this common spine.

12. Feature Review Status

The Business SME feature review may still be in progress.

Therefore:

- do not assume every currently implemented feature is finally approved
- keep feature logic modular
- make it easy to add/remove features after Business SME confirmation
- clearly distinguish active, pending-review and de-scoped features where relevant
- do not reintroduce previously de-scoped duplicate features without explicit instruction

13. Leakage Protection

Never use future/outcome information as an input feature.

Examples include:

- future exit events
- exit date after AsOfDate
- account closure occurring in the outcome period
- completed churn events
- future full rollover events
- future Super-to-Pension events
- outcome-period information embedded inside web request parameters

All predictive features must represent information genuinely available as of the scoring date.

14. Final Development Principle

Before generating or modifying ML feature code:

1. Read these repository instructions.
2. Review the relevant behavioural SQL reference file.
3. Inspect the corresponding "mscs_mrt_*" Databricks table schema.
4. Map the reviewed SQL business logic to the Databricks source.
5. Implement the feature at account_id + as_of_date grain.
6. Validate grain, ranges and leakage.
7. Only then integrate the feature into the consolidated feature dataset.
