Create the next reviewed behavioural feature module for Member Retention Analytics:

notebook/ml_mscs_mrt_helpline_features.py

Follow `.github/copilot-instructions.md` strictly.

IMPORTANT:
Do not invent or redesign the business logic.

Before writing code:

1. Read `.github/copilot-instructions.md`.
2. Review the Helpline Behaviour section in:
   `behavioural_features_business_review.sql`
3. Treat the reviewed standalone SQL as the primary source of truth for:
   - feature definitions
   - source fields
   - filters
   - exclusions
   - date logic
   - aggregation logic
4. Inspect the actual Databricks schema before implementing.

Databricks source should use the corresponding MRT landing table, expected to be:

mer_wealth_dev.mer_wealth_landing_edge.mscs_mrt_account_engagement_helpline

Do not assume SQL Server and Databricks column names/types are identical.
Inspect the actual Databricks schema and map the reviewed SQL logic appropriately.

BASE POPULATION

Reuse the common corrected base population from:

notebook/ml_mscs_mrt_base_population.py

Do not rebuild AccountSummary eligibility logic inside this module.

Call the shared base population using the same controlled modelling snapshot:

as_of_date = "2024-03-31"

Conceptually:

base_population_df =
    run_base_population_pipeline(
        spark,
        as_of_date="2024-03-31"
    )

The helpline pipeline should conceptually expose:

run_helpline_feature_pipeline(
    spark,
    as_of_date="2024-03-31"
)

MANDATORY SNAPSHOT RULE

The final modelling snapshot must come only from the explicitly supplied controlled `as_of_date`.

Do NOT derive `as_of_date` from:

- reportingDate
- fundJoinDate
- helpline interaction dates
- system/current date
- any other source date

For this development run every final row must have:

as_of_date = 2024-03-31

FEATURE LOGIC

Implement only the reviewed/active Helpline Behaviour features from:

`behavioural_features_business_review.sql`

Preserve the standalone SQL logic as closely as possible.

Where the reviewed SQL uses:

- trailing 12-month windows
- recent 90-day windows
- recency calculations
- call/contact counts
- interaction/category filters
- exclusions

preserve those definitions exactly unless Databricks schema/type differences require a technical adaptation.

All feature windows must be calculated relative to the controlled `as_of_date`.

No source helpline interaction after `as_of_date` may contribute to predictive features.

The final feature DataFrame must be:

helpline_features_df

Final grain:

one row per account_id per as_of_date

Accounts with no qualifying helpline activity must still remain in the output through the shared base population, with appropriate zero/NULL values consistent with the reviewed SQL logic.

Do not persist this individual feature DataFrame as a table yet.

VALIDATION

Add logging and validation consistent with the existing contribution/rollover/investment/insurance modules.

At minimum log and validate:

- base population row count
- output row count
- distinct account_id + as_of_date count
- distinct as_of_date count
- duplicate account_id + as_of_date count
- null account_id count
- null as_of_date count
- distinct as_of_date values
- future helpline leakage count
- negative count/rate values where applicable
- any feature-specific invalid ranges

Hard requirements:

- output row count must equal base population row count
- duplicate account_id + as_of_date = 0
- null account_id = 0
- null as_of_date = 0
- distinct as_of_date count = 1
- as_of_date must equal 2024-03-31
- future helpline leakage count = 0

Use Python logging and re-raise critical exceptions.

Do not modify:

- base population business logic
- contribution features
- rollover features
- investment features
- insurance features
- unrelated Data Engineering / Power BI files

Do not persist any table.

After implementation, provide:

1. Databricks source table used
2. Actual source-field mappings
3. Helpline features implemented
4. Any reviewed SQL fields that could not be mapped
5. Validation checks added
6. Confirmation that final grain remains one row per account_id per as_of_date
