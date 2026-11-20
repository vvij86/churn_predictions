
Member Retention Analytics - ML Development Instructions

These instructions apply to all Machine Learning development for the Member Retention Analytics project in this repository.

Copilot must read and follow these instructions before generating or modifying any ML feature-engineering code.

---

1. General Development Rules

- This repository is shared with Data Engineering and Power BI development.
- Do not modify unrelated Data Engineering or Power BI files.
- All ML Python files must start with:

"ml_mscs_mrt_"

Examples:

- "ml_mscs_mrt_base_population.py"

- "ml_mscs_mrt_contribution_features.py"

- "ml_mscs_mrt_rollover_features.py"

- "ml_mscs_mrt_investment_features.py"

- "ml_mscs_mrt_insurance_features.py"

- Do not create any subfolders under the existing "notebook" folder.

- Keep all ML Python files directly under the existing "notebook" folder.

- Use PySpark / Databricks Spark DataFrames for the main feature-engineering pipeline.

- Do not use Pandas for large-scale feature engineering unless explicitly required for a small local operation.

- Do not create mock or sample source data unless explicitly requested.

- Prefer reusable functions over large monolithic scripts.

- Feature modules must be independently testable but reusable by downstream modules.

- Do not execute a feature pipeline automatically merely because the module was imported.

- Pipeline execution should be triggered explicitly through a run/main function.

---

2. Databricks Source

Source catalog:

"mer_wealth_dev"

Source schema:

"mer_wealth_landing_edge"

Use only the ML-related Databricks landing tables following the naming convention:

"mscs_mrt_*"

Examples include:

- "mscs_mrt_account_summary"
- "mscs_mrt_account_money_inflow"
- "mscs_mrt_account_rollover_payment"
- "mscs_mrt_account_investments"
- "mscs_mrt_account_insurance_current"
- "mscs_mrt_account_engagement_web"
- "mscs_mrt_account_engagement_helpline"
- "mscs_mrt_account_engagement_workflow"
- "mscs_mrt_campaign_events"
- "mscs_mrt_campaign_event_details"
- "mscs_mrt_customer_mapping"
- "mscs_mrt_customer_summary"
- "mscs_mrt_third_party_authority"

Do not use similarly named legacy/non-MRT tables unless explicitly requested.

Always inspect the actual Databricks source schema before implementing logic.

Do not assume that SQL Server and Databricks:

- table names
- column names
- data types
- Boolean representations
- date representations

are identical.

Do not invent source fields.

If a required SQL Server field does not exist in the Databricks source:

- log the issue
- add a clear TODO/comment
- state the missing mapping
- do not fabricate or approximate the value

---

3. Mandatory Behavioural SQL Reference Files

The following existing standalone SQL files contain previously developed/reviewed behavioural feature logic and MUST be used as business-logic references when implementing the corresponding Databricks feature logic.

1. "behavioural_features_business_review.sql"

2. "AccountEngagementWeb_Reviewed_Features.sql"

These files are reference implementations from the earlier SQL Server development.

When implementing features in Databricks:

- review the relevant logic in these SQL files first
- preserve the reviewed feature definitions
- preserve reviewed calculations
- preserve reviewed feature windows
- preserve reviewed exclusions
- preserve reviewed business rules
- preserve feature names where practical
- do not blindly copy SQL Server table names
- do not blindly copy SQL Server column names
- do not blindly translate SQL syntax without validating the Databricks source
- map the reviewed SQL logic to the appropriate "mscs_mrt_*" Databricks tables
- inspect the actual Databricks schema before referencing fields
- do not introduce new business rules unless explicitly requested

If the Python implementation differs from the reference SQL because of a genuine Databricks source difference, document the reason clearly.

---

4. Reference SQL Purpose

"behavioural_features_business_review.sql"

Use this as the primary reference for reviewed behavioural feature logic including, where applicable:

- base-population eligibility rules
- contribution behaviour
- contribution change / inflow behaviour
- partial rollover / withdrawal behaviour
- investment behaviour
- insurance behaviour
- campaign / event behaviour
- helpline behaviour
- third-party authority behaviour
- other reviewed behavioural feature blocks contained in the file

"AccountEngagementWeb_Reviewed_Features.sql"

Use this specifically as the reference for reviewed AccountEngagementWeb / digital behavioural feature logic.

Do not use outcome or future information such as "ExitDate" from web request parameters as predictive features.

Generic website activity must not be introduced merely because the source table contains it.

Only implement reviewed digital-intent features.

---

5. Mandatory Modelling Grain

The mandatory ML feature grain is:

"one row per account_id per as_of_date"

Every feature module must preserve this grain.

The account is the modelling entity.

Lower-grain records such as:

- transactions
- contributions
- rollovers
- campaign events
- web events
- helpline interactions
- investment positions
- insurance records

must be aggregated appropriately before becoming final feature output.

Never allow feature joins to multiply account-level rows.

Every feature module must validate:

"account_id + as_of_date"

for uniqueness.

---

6. CRITICAL As-Of-Date / Snapshot Rule

This rule is mandatory and overrides any inferred source-date behaviour.

Modelling "as_of_date"

"as_of_date" is an explicit, controlled modelling snapshot date.

It MUST NOT be derived directly from:

- "reportingDate"
- "exitDate"
- "exitDateRecorded"
- "fundJoinDate"
- transaction dates
- event dates
- the current system date

The initial development snapshot is:

"2024-03-31"

unless another controlled snapshot date is explicitly supplied.

The reviewed standalone SQL uses the equivalent concept:

"@AsOfDate"

The PySpark implementation must preserve that same business meaning.

Example:

If the controlled modelling snapshot is:

"2024-03-31"

then all eligible accounts in that snapshot should have:

"as_of_date = 2024-03-31"

The source "reportingDate" must NOT automatically become "as_of_date".

---

7. Role of Important Account Dates

The following fields serve different purposes and must not be confused.

"fundJoinDate"

"fundJoinDate" represents when the account joined the fund.

Use it for:

- account eligibility
- tenure calculation
- point-in-time membership existence checks

Typical rule:

"fundJoinDate <= as_of_date"

Example:

"fundJoinDate = 2018-06-10"

"as_of_date = 2024-03-31"

The account existed at the modelling snapshot and may be included subject to other eligibility rules.

"fundJoinDate" is NOT the modelling snapshot date.

"reportingDate"

"reportingDate" is source metadata / source reporting information.

It must NOT automatically become the ML modelling "as_of_date".

This is especially important because in the source data "reportingDate" may align with "exitDate" for many records.

Using "reportingDate" as the modelling snapshot could incorrectly anchor account observations around exit events.

"reportingDate" may only be used when explicitly required for deterministic source-record selection or source-data interpretation.

It must never redefine the controlled modelling snapshot.

"exitDate" / "exitDateRecorded"

These fields represent account-exit information.

They may be used for:

- eligibility as of the snapshot
- target construction
- explicit exclusion logic
- outcome definition

They must NOT define the feature snapshot date.

For an active account at snapshot:

"exitDateRecorded IS NULL OR exitDateRecorded > as_of_date"

Feature logic must not use future exit information as a predictor.

"dateOfDeath" / death indicators

Death-related records must follow the reviewed exclusion logic.

An account/member deceased on or before the modelling snapshot must not be treated as an eligible active modelling record where the reviewed business rules exclude deceased members.

---

8. Historical Snapshot Strategy

The pipeline must support multiple historical modelling snapshots.

However, snapshots must be generated intentionally using controlled dates.

Do NOT create historical snapshots simply by using every available source "reportingDate".

Example controlled snapshots may eventually include:

- "2024-03-31"
- "2024-06-30"
- "2024-09-30"
- "2024-12-31"
- later agreed monthly or quarterly snapshot dates

The exact snapshot schedule must be driven by modelling/business requirements.

Each controlled snapshot must independently answer:

«What information was genuinely available for this account as of this date?»

The feature pipeline must therefore be reusable for any supplied "as_of_date".

Do not hard-code logic that only works for one snapshot.

---

9. Historical and Point-in-Time Rules

Historical source availability begins from:

"2023-04-01"

All predictive feature calculations must be point-in-time safe.

Features may use only information available on or before:

"as_of_date"

No information after "as_of_date" may contribute to predictive features.

All feature windows must be calculated relative to the controlled "as_of_date".

Prevent outcome leakage.

Use deterministic point-in-time logic when multiple source records exist.

Do not use "dropDuplicates()" merely to hide duplicate records without understanding why duplicates occurred.

When several source records exist for an account, use the reviewed business rule and appropriate source dates to select or aggregate them deterministically.

---

10. Feature Windows

Where required by the reviewed feature logic, use:

- trailing 12-month feature window
- recent 90-day feature window
- prior 90-day feature window
- earlier/baseline windows where specifically defined

All windows must be calculated relative to the controlled:

"as_of_date"

Do not calculate windows from:

- current system date
- execution date
- "reportingDate"

unless explicitly required by the reviewed source logic.

For example, if:

"as_of_date = 2024-03-31"

then a trailing 12-month feature should only use relevant events occurring within the reviewed lookback period ending on or before "2024-03-31".

---

11. Base Population

The ML feature pipeline must be anchored to a common reusable account-level base population.

Primary source:

"mer_wealth_dev.mer_wealth_landing_edge.mscs_mrt_account_summary"

The base population must maintain:

"one account_id + one controlled as_of_date = one row"

The base population must be driven by the supplied controlled "as_of_date".

Do not populate "as_of_date" using the account source's "reportingDate".

For the initial development snapshot:

"as_of_date = 2024-03-31"

unless another value is explicitly passed.

Use reviewed eligibility logic including, where applicable:

- "fundJoinDate <= as_of_date"
- approved database/fund scope
- account active as of the snapshot
- exit date after the snapshot or null
- deceased exclusion
- other reviewed account eligibility rules

The base population should expose required identifiers/fields used downstream, such as where available:

- "account_id"
- "member_id"
- "customer_id"
- "fund_id"
- "fund_join_date"
- "as_of_date"

Do not include future outcome data as modelling features.

Behavioural features should subsequently join to this common account spine.

---

12. Feature Module Output Standard

Each individual feature module should produce:

- "account_id"
- "as_of_date"
- feature columns belonging to that module

The result from every module must contain no duplicate:

"account_id + as_of_date"

Accounts in the base population should not disappear simply because no source behaviour exists.

Where appropriate:

- counts may default to 0
- flags may default to 0
- recency values may remain NULL when no event exists
- amounts should follow the reviewed business meaning

Do not arbitrarily replace meaningful NULLs with zero.

Intermediate feature DataFrames do not need to be persisted unless explicitly required.

---

13. Feature Dataset Persistence

Do not persist every individual feature block as a Databricks table.

During feature development, modules should normally return Spark DataFrames.

After all approved feature blocks are:

- implemented
- assembled
- validated
- checked for leakage
- checked for grain integrity

persist one consolidated feature dataset in the DEV environment.

The consolidated feature dataset will become the reusable source for downstream modelling-input preparation.

The persisted dataset must maintain:

"one row per account_id per as_of_date"

Do not persist an invalid or partially multiplied feature dataset.

---

14. Feature Review Status

The Business SME feature review may still be in progress.

Therefore:

- do not assume every currently implemented feature is finally approved
- keep feature logic modular
- make it easy to add/remove features after Business SME confirmation
- clearly distinguish active, pending-review and de-scoped features where relevant
- do not reintroduce previously de-scoped duplicate features without explicit instruction

When new business-review comments arrive:

- review the affected feature block
- update only the impacted feature logic
- preserve unaffected modules
- rerun relevant validations
- document material changes

---

15. Known Reviewed Feature Decisions

Contribution Behaviour

Contribution behaviour should be sourced from the reviewed AccountMoneyInflow logic.

Do not recreate duplicate contribution-event counters from Campaign/Event sources.

Previously de-scoped duplicate features include:

- "contribution_event_count_12m"
- "recent_contribution_event_count_90d"

Do not reintroduce these unless explicitly requested.

Investment Behaviour

Reviewed active investment features include:

- "investment_option_count_asof"
- "total_investment_value_asof"
- "direct_investment_flag"

Insurance Behaviour

Reviewed active insurance features include:

- "has_death_cover_asof"
- "has_tpd_cover_asof"
- "has_ip_cover_asof"
- "insurance_cover_type_count_asof"

De-scoped final insurance amount features include:

- "death_cover_amount_asof"
- "tpd_cover_amount_asof"
- "ip_cover_amount_asof"

Amounts may be used internally when required to derive valid cover flags, but must not be output as final modelling features unless business review changes.

Website Engagement

Use only reviewed AccountEngagementWeb features from:

"AccountEngagementWeb_Reviewed_Features.sql"

Do not introduce generic website activity features unless explicitly reviewed.

Do not use "ExitDate" or other outcome information embedded in request parameters.

---

16. Leakage Protection

Never use future/outcome information as a predictive feature.

Examples include:

- future exit events
- exit date after "as_of_date"
- account closure occurring in the outcome period
- completed churn events
- future full-rollover events
- future Super-to-Pension events
- outcome-period information embedded inside web request parameters
- any source activity occurring after "as_of_date"

All predictive features must represent information genuinely available as of the controlled scoring/snapshot date.

Feature/event records must satisfy:

"event_date <= as_of_date"

where event dates are relevant.

Post-"as_of_date" leakage must be validated explicitly.

---

17. Boolean Data-Type Handling

Databricks source types must be respected.

Do not assume that fields represented as "0/1" in SQL Server are integers in Databricks.

If Databricks exposes a field as BOOLEAN:

do not write:

"boolean_column == 1"

or:

"boolean_column == 0"

Use Boolean-safe expressions instead.

For example:

- true condition
- false condition
- "coalesce(boolean_column, false)"

Apply this especially to flags such as:

- internal transfer flags
- direct investment flags
- insurance flags
- other Databricks Boolean columns

Always inspect the Databricks schema first.

---

18. Spark Session and Module Reuse

Feature modules must work reliably in Databricks ML cluster execution and when imported by other ML modules.

Do not rely exclusively on a module-global "spark" variable.

Prefer:

- passing the active SparkSession explicitly into reusable functions
- or obtaining the SparkSession using an approved reusable runtime pattern

Importing one feature module from another must not accidentally run the imported module's entire pipeline.

Avoid code like this at module import time:

"feature_df = run_pipeline()"

unless the execution context explicitly requires it.

Prefer an explicit callable function such as:

"run_feature_pipeline(spark, as_of_date)"

and invoke it deliberately.

When necessary, use:

"if __name__ == "__main__":"

for direct execution behaviour.

Keep modules compatible with:

- Databricks ML shared cluster
- VS Code Databricks extension
- future Databricks Workflow execution

Do not hard-code user-specific Databricks workspace paths.

---

19. Inter-Module Imports

ML modules under the "notebook" folder may reuse functions from other ML modules.

Prefer normal Python module imports where supported.

Example:

"from ml_mscs_mrt_base_population import run_base_population_pipeline"

Do not use fragile absolute workspace paths tied to a specific developer account.

Do not create manual file-loading logic unless necessary.

All shared modules should be designed so that:

- direct execution works
- imported execution works
- ML-cluster execution works
- workflow execution can be added later

---

20. Logging and Exception Handling

Use Python "logging" for pipeline execution/status messages.

Use:

- "logger.info()" for normal progress
- "logger.warning()" for non-fatal data-quality concerns
- "logger.error()" where useful for explicit critical messages
- "logger.exception()" inside exception handlers to preserve stack traces

Re-raise critical exceptions so Databricks jobs fail correctly.

Never silently swallow exceptions.

Critical failures include, where appropriate:

- missing required source columns
- invalid modelling grain
- duplicate "account_id + as_of_date"
- null required keys
- invalid feature values
- source mapping failures
- future leakage
- unexpected row multiplication

Log major processing stages such as:

- source load
- schema inspection
- mapping
- point-in-time filtering
- feature calculations
- aggregation
- validation
- successful completion

Do not use MLflow autologging for feature-engineering/base-population modules.

MLflow autologging should be introduced later for:

- model training
- model evaluation
- experiment tracking

where appropriate.

---

21. Validation Requirements

Every feature module must include appropriate validation.

At minimum validate/log where relevant:

- total row count
- base population row count
- output row count
- distinct account count
- distinct "account_id + as_of_date"
- duplicate "account_id + as_of_date"
- null account IDs
- null "as_of_date"
- date ranges
- unexpected negative values
- percentage/rate boundaries
- feature min/max values where useful
- unexpected row multiplication
- post-"as_of_date" leakage
- invalid Boolean/flag values
- source mapping issues
- source rows that cannot map to an account where relevant

Critical grain or leakage failures must not be silently ignored.

For a valid feature module:

- duplicate "account_id + as_of_date" count should be 0
- null mandatory key count should be 0
- future leakage count should be 0
- output row count must not exceed the base population because of join multiplication

Feature-specific validations should also be implemented.

---

22. Performance Standards

Use Spark-native transformations wherever practical.

Prefer:

- "select"
- "filter"
- "withColumn"
- "groupBy"
- "agg"
- Spark window functions
- left joins from the base population
- Spark SQL functions

Avoid:

- unnecessary ".collect()"
- converting large datasets to Pandas
- driver-side loops over large datasets
- unnecessary full-table caching
- repeated full scans where avoidable
- Python UDFs when Spark-native functions can perform the same logic

Use ".collect()" only for small validation summaries where appropriate.

Do not collect large Spark datasets to the driver.

---

23. Join Standards

The base population should normally drive feature joins.

Use left joins when behavioural activity is optional.

Before joining lower-grain sources:

- understand the source grain
- aggregate or deterministically select appropriate records
- validate uniqueness of the join key where necessary

Never allow:

one account-level row

to become:

multiple account-level rows

because of an uncontrolled join.

After important joins, validate row counts and grain.

---

24. Naming Standards

Use snake_case for ML output column names.

Examples:

- "account_id"
- "as_of_date"
- "fund_join_date"
- "contribution_count_12m"
- "partial_rollover_amount_12m"
- "investment_option_count_asof"
- "has_death_cover_asof"

Use descriptive function names.

Examples:

- "load_source()"
- "validate_source()"
- "build_features()"
- "validate_features()"
- "run_feature_pipeline()"

Keep source catalog/schema/table names configurable where appropriate.

Use concise comments and docstrings explaining business meaning rather than obvious syntax.

---

25. Controlled Snapshot Parameterisation

Feature modules must accept a controlled snapshot date.

Preferred conceptual interface:

"run_feature_pipeline(spark, as_of_date)"

The supplied "as_of_date" must be used consistently across:

- base population
- contribution features
- rollover features
- investment features
- insurance features
- campaign features
- helpline features
- website features
- all future feature modules

For the initial development run:

"as_of_date = "2024-03-31""

Do not separately derive an "as_of_date" inside individual feature modules.

All modules participating in the same modelling snapshot must use the same controlled snapshot date.

---

26. Future Multiple Snapshot Processing

The feature code must be designed so multiple historical snapshots can later be generated by repeatedly executing the same pipeline with different controlled "as_of_date" values.

Conceptually:

Snapshot 1:

"as_of_date = 2024-03-31"

Snapshot 2:

"as_of_date = 2024-06-30"

Snapshot 3:

"as_of_date = 2024-09-30"

etc.

Do not derive snapshot dates implicitly from source records.

Do not assume the historical snapshot schedule without explicit requirement.

The eventual multi-snapshot feature dataset will contain:

"account_id + as_of_date"

as its modelling key.

---

27. Current Development Sequence

Current feature-development sequence should follow the reviewed business logic approximately as:

1. base population
2. contribution behaviour
3. partial rollover / withdrawal behaviour
4. investment behaviour
5. insurance behaviour
6. campaign / event behaviour
7. helpline behaviour
8. website engagement
9. other reviewed behavioural feature blocks
10. consolidated feature assembly
11. final feature validation
12. modelling-input preparation
13. temporal train / validation / test split
14. model training and evaluation
15. MLflow / model registry / scoring pipeline

Do not jump directly to modelling before the consolidated feature dataset is ready and validated.

---

28. Final Development Principle

Before generating or modifying any ML feature code:

1. Read this repository instruction file.
2. Review the relevant standalone behavioural SQL reference.
3. Inspect the corresponding "mscs_mrt_*" Databricks source schema.
4. Confirm the controlled "as_of_date".
5. Confirm the reviewed business logic.
6. Confirm source field mappings and data types.
7. Implement feature logic at "account_id + as_of_date" grain.
8. Use only information available on or before "as_of_date".
9. Validate grain, ranges, nulls and leakage.
10. Only then integrate the feature into the consolidated feature dataset.

When there is a conflict between an inferred technical interpretation and the reviewed business logic, do not guess.

Preserve the reviewed business intent and add a TODO / request clarification when required.

Most importantly:

Never derive the modelling "as_of_date" from "reportingDate".

The modelling "as_of_date" is a controlled snapshot parameter equivalent to the reviewed SQL Server "@AsOfDate".

"fundJoinDate", "reportingDate", "exitDateRecorded", event dates and transaction dates have their own specific business purposes and must not replace the modelling snapshot date.
