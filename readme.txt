Create the next reviewed behavioural feature module:

notebook/ml_mscs_mrt_third_party_authority_features.py

Follow `.github/copilot-instructions.md` strictly.

PRIMARY BUSINESS-LOGIC REFERENCE:

behavioural_features_business_review.sql

Before writing code:

1. Read the complete Third Party Authority section in the reviewed SQL.
2. Inspect the actual Databricks `mscs_mrt_*` source schema used for this logic.
3. Preserve the reviewed SQL business rules exactly.
4. Do not invent source mappings or new features.

Reuse the common base population from:

notebook/ml_mscs_mrt_base_population.py

using:

run_base_population_pipeline(
    spark,
    as_of_date="2024-03-31"
)

Controlled snapshot:

as_of_date = "2024-03-31"

Do NOT derive as_of_date from:
- reportingDate
- fundJoinDate
- authority start/end dates
- transaction dates
- system date

All authority information used for predictive features must represent information available on or before:

2024-03-31

Implement only the reviewed Third Party Authority features present in:

behavioural_features_business_review.sql

Do NOT add new feature definitions.

Final grain must remain:

one row per account_id per as_of_date

Create final DataFrame:

third_party_authority_features_df

It must contain:
- account_id
- as_of_date
- reviewed Third Party Authority feature columns

Do not persist this feature DataFrame as a table yet.

VALIDATION

Add validation consistent with the existing completed modules:

- base population row count
- output row count
- distinct account_id + as_of_date
- duplicate count = 0
- null account_id = 0
- null as_of_date = 0
- distinct as_of_date count = 1
- snapshot exactly = 2024-03-31
- future leakage count = 0
- invalid flag/count values = 0 where applicable

If the source contains records after as_of_date, log them separately as informational source presence, but fail only if future records actually enter feature calculations.

Preserve NULL semantics where source information is genuinely unavailable.

Use Spark/PySpark DataFrame transformations.

Do not modify:
- completed feature modules
- Data Engineering files
- Power BI files
- reviewed SQL reference files

After implementation report:

1. Exact reviewed Third Party Authority features implemented.
2. Databricks source table and column mappings used.
3. Any unavailable source mappings.
4. Any de-scoped features intentionally excluded.
5. Validation metrics.
6. Confirmation of one row per account_id per as_of_date.
7. Confirmation all rows use as_of_date = 2024-03-31.
