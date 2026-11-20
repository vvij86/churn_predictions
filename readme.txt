Create a new consolidated behavioural feature dataset module:

notebook/ml_mscs_mrt_consolidated_features.py

Follow `.github/copilot-instructions.md` strictly.

DO NOT modify the existing feature modules unless absolutely required for import/reuse.

PURPOSE

Combine the completed reviewed behavioural feature modules into one consolidated account-level feature dataset for downstream modelling.

CONTROLLED SNAPSHOT

Use:

as_of_date = "2024-03-31"

Reuse the common base population from:

notebook/ml_mscs_mrt_base_population.py

The consolidated dataset must remain at:

one row per account_id per as_of_date

FEATURE MODULES TO REUSE

- notebook/ml_mscs_mrt_contribution_features.py
- notebook/ml_mscs_mrt_rollover_features.py
- notebook/ml_mscs_mrt_investment_features.py
- notebook/ml_mscs_mrt_insurance_features.py
- notebook/ml_mscs_mrt_helpline_features.py
- notebook/ml_mscs_mrt_campaign_features.py
- notebook/ml_mscs_mrt_web_engagement_features.py
- notebook/ml_mscs_mrt_third_party_authority_features.py

Do not reimplement feature business logic inside this consolidated module.

Instead:

1. Run/reuse the common base population with the controlled as_of_date.
2. Run each feature pipeline using the same SparkSession and same controlled as_of_date.
3. Join each feature DataFrame back to the base population using:

   account_id
   as_of_date

4. Use LEFT joins from the base population so every eligible base-population account is retained.
5. Never allow joins to multiply account-level rows.
6. Do not join on member_id, customer_id, fund_id, reportingDate, or fundJoinDate.
7. Do not derive a new as_of_date anywhere.

EXPECTED INPUT DATAFRAMES

Reuse the existing final DataFrames produced by the modules:

- contribution_features_df
- rollover_features_df
- investment_features_df
- insurance_features_df
- helpline_features_df
- campaign_features_df
- web_engagement_features_df
- third_party_authority_features_df

BASE CONTEXT COLUMNS

Retain the base-population identifiers/context needed for downstream modelling and Power BI, including at minimum:

- account_id
- member_id
- customer_id
- fund_id
- fund_join_date
- as_of_date

Do not accidentally remove these while joining features.

WEB ENGAGEMENT NULL RULE

The UAT AccountEngagementWeb source is unavailable for the current snapshot window.

Preserve the existing NULL semantics from `web_engagement_features_df`.

Do NOT replace unavailable web feature NULLs with zero in the consolidated dataset.

OTHER FEATURE NULL HANDLING

Do not blanket-fill all NULLs with 0.

Preserve each feature module's intended semantics.

Only use zero where the individual reviewed feature module already defines zero as the valid "no activity / no event" value.

DE-SCOPED FEATURES

Do not reintroduce any previously de-scoped features.

Examples include:

- contribution_event_count_12m
- recent_contribution_event_count_90d
- employer_sg_current_amount_12m
- salary_sacrifice_current_amount_12m
- member_voluntary_current_amount_12m
- death_cover_amount_asof
- tpd_cover_amount_asof
- ip_cover_amount_asof
- de-scoped generic web activity features
- de-scoped workflow features

Do not include intermediate helper columns unless they are part of the reviewed final feature output.

FINAL DATAFRAME

Create:

consolidated_features_df

Do not persist it as a table yet unless explicitly instructed.

VALIDATION

After every join, validate:

- row count does not increase above base population
- distinct account_id + as_of_date count remains equal to base population
- duplicate account_id + as_of_date count = 0

Final validation must log:

- base population row count
- consolidated output row count
- distinct account_id count
- distinct account_id + as_of_date count
- duplicate account_id + as_of_date count
- null account_id count
- null as_of_date count
- distinct as_of_date count
- distinct as_of_date values
- minimum as_of_date
- maximum as_of_date
- confirmation all rows use 2024-03-31
- total final column count
- feature count by module
- unexpected duplicate column names
- post-snapshot leakage status
- web unavailable/NULL feature counts
- row-count comparison after each feature-module join

HARD FAIL CONDITIONS

Raise an exception if:

- consolidated row count exceeds base population row count
- duplicate account_id + as_of_date exists
- more than one as_of_date exists for this run
- as_of_date differs from 2024-03-31
- account_id or as_of_date is null
- any feature join changes the modelling grain
- duplicate feature column names are introduced unexpectedly

OUTPUT

Display a small sample of `consolidated_features_df`.

After implementation provide a concise summary containing:

1. Base row count.
2. Final consolidated row count.
3. Number of final feature columns.
4. Feature modules successfully joined.
5. Any columns intentionally excluded.
6. Any feature groups containing NULLs because source is unavailable.
7. Duplicate/grain validation result.
8. Confirmation all rows use as_of_date = 2024-03-31.

Do not create training/validation splits yet.

Do not train any ML model yet.

This task is only to build and validate the consolidated behavioural feature dataset.
