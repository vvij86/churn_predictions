Create the next reviewed behavioural feature module for Member Retention Analytics:

notebook/ml_mscs_mrt_campaign_features.py

Follow `.github/copilot-instructions.md` strictly.

Before writing code, review the existing standalone reviewed SQL:

- behavioural_features_business_review.sql

Use the Campaign / Event Behaviour section of that SQL as the PRIMARY business-logic reference.

Also inspect the actual Databricks source schemas before implementing anything.

Use only the corresponding `mscs_mrt_*` Databricks landing tables under:

catalog:
mer_wealth_dev

schema:
mer_wealth_landing_edge

Possible relevant sources include the reviewed mappings for:
- campaign events
- campaign event details
- campaign/account mappings

Do NOT invent column mappings.
If any SQL Server field does not have a confirmed Databricks equivalent, clearly flag it instead of guessing.

IMPORTANT:
Previously de-scoped duplicate contribution-event features must NOT be reintroduced:

- contribution_event_count_12m
- recent_contribution_event_count_90d

These were removed because contribution behaviour is already sourced from AccountMoneyInflow.

Retain only the currently reviewed/approved Campaign/Event behavioural features from the standalone SQL.

For roll-in related campaign/event features, preserve the reviewed logic where applicable, including:

- rollin_event_count_12m
- recent_rollin_event_count_90d

Do not add new business features unless they already exist in the reviewed standalone SQL.

BASE POPULATION

Reuse the common controlled-snapshot base population from:

notebook/ml_mscs_mrt_base_population.py

Do NOT rebuild eligibility/database-code/deceased/active-account filtering inside this module.

The module must call:

run_base_population_pipeline(
    spark,
    as_of_date="2024-03-31"
)

For the current development run:

as_of_date = "2024-03-31"

The final grain must remain:

one row per account_id per as_of_date

Do NOT derive as_of_date from:

- reportingDate
- fundJoinDate
- campaign dates
- event dates
- exit dates
- system/current date

FEATURE WINDOWS

All feature windows must be calculated relative to the controlled as_of_date.

Where required by the reviewed SQL:

- trailing 12-month window
- recent 90-day window

No campaign/event record after as_of_date may contribute to a predictive feature.

Use Spark/PySpark DataFrame operations.

Preserve point-in-time safety and prevent outcome leakage.

Do NOT use outcome-related events such as:

- member exit
- account closure
- completed full rollover-out
- other events that directly reveal churn after/because of exit

OUTPUT

Create final DataFrame:

campaign_features_df

It must contain:

- account_id
- as_of_date
- only the reviewed Campaign/Event feature columns

Do not persist this individual DataFrame as a table yet.

VALIDATION

Add validation consistent with the existing contribution, rollover, investment, insurance and helpline modules.

At minimum log and validate:

- base population row count
- output row count
- distinct account_id + as_of_date count
- distinct as_of_date count
- duplicate account_id + as_of_date count = 0
- null account_id count = 0
- null as_of_date count = 0
- future campaign/event leakage count = 0
- exactly one snapshot date
- snapshot date exactly equals 2024-03-31
- negative count/value checks where relevant
- invalid binary flag checks where relevant

If raw source contains post-2024-03-31 events, they may be logged as an INFORMATIONAL source-presence metric, but validation should fail only if such future records actually enter feature calculations.

LOGGING

Follow the same logging and exception-handling pattern used in the existing ML feature modules.

Log major stages:

- loading base population
- loading source tables
- schema inspection
- source mapping
- point-in-time filtering
- feature calculation
- aggregation to account grain
- validation
- successful completion

Do not modify:

- existing completed feature modules
- Data Engineering files
- Power BI files
- business SQL reference files

After implementation, provide:

1. Exact reviewed Campaign/Event features implemented.
2. Databricks source table/column mapping used.
3. Features intentionally excluded/de-scoped.
4. Any unresolved source mapping.
5. Validation results.
6. Confirmation that final grain is one row per account_id per as_of_date.
7. Confirmation that all rows use as_of_date = 2024-03-31.
