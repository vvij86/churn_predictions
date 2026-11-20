Create the reviewed AccountEngagementWeb / Digital Behaviour feature module:

notebook/ml_mscs_mrt_web_engagement_features.py

Follow `.github/copilot-instructions.md` strictly.

PRIMARY BUSINESS-LOGIC REFERENCE:

AccountEngagementWeb_Reviewed_Features.sql

Before implementing anything:

1. Read the complete reviewed SQL file.
2. Inspect the actual Databricks source schema.
3. Confirm whether the corresponding `mscs_mrt_account_engagement_web` source contains data in the current DEV/UAT environment.

Use:

catalog:
mer_wealth_dev

schema:
mer_wealth_landing_edge

Do NOT invent mappings.

IMPORTANT ENVIRONMENT RULE:

The AccountEngagementWeb source is known to be unavailable/empty in UAT.

If the Databricks source is empty:

- do NOT manufacture sample records
- do NOT convert unavailable web behaviour into genuine zero activity
- preserve NULL/unavailable semantics for the reviewed web feature columns
- log clearly that AccountEngagementWeb data is unavailable for this snapshot/environment
- still produce the full base-population grain so this module can later work when production data becomes available

Reuse the common base population from:

notebook/ml_mscs_mrt_base_population.py

using:

run_base_population_pipeline(
    spark,
    as_of_date="2024-03-31"
)

Controlled snapshot:

as_of_date = "2024-03-31"

Never derive as_of_date from source dates.

Final grain:

one row per account_id per as_of_date

IMPLEMENT ONLY THE REVIEWED DIGITAL FEATURES FROM:

AccountEngagementWeb_Reviewed_Features.sql

Expected reviewed feature concepts include, where supported by the SQL:

Retirement planning:
- retirement_planning_activity_count_12m
- recent_retirement_planning_activity_count_90d
- days_since_last_retirement_planning_activity

Leaving-service intent, where retained in reviewed SQL:
- leaving_service_quote_count_12m
- recent_leaving_service_quote_count_90d
- days_since_last_leaving_service_quote

Transfer intent, where retained:
- transfer_intent_activity_count_12m
- recent_transfer_intent_activity_count_90d

Investment-switch digital intent, where retained:
- investment_switch_activity_count_12m
- recent_investment_switch_activity_count_90d

Do NOT reintroduce the previously de-scoped broad generic website activity features unless the reviewed SQL explicitly retains them.

Examples that were de-scoped include generic WebQuoteSummary activity such as:

- web_activity_count_12m
- web_active_days_12m
- days_since_last_web_activity
- recent_web_activity_count_90d

LEAKAGE:

Never use ExitDate or other outcome/future information present inside RequestParameters.

Do not use:
- ExitDate
- future account closure information
- future rollover-out information
- any outcome information after as_of_date

All actual web events used in features must satisfy:

event_date <= as_of_date

FEATURE WINDOWS:

Use reviewed SQL definitions relative to controlled as_of_date:

- trailing 12 months
- recent 90 days
- recency calculations where applicable

OUTPUT:

Create:

web_engagement_features_df

containing:

- account_id
- as_of_date
- reviewed digital behaviour feature columns

If source data is unavailable in this environment, output should still contain all 785885 base-population accounts, but web feature values must follow the reviewed unavailable-data NULL handling rather than pretending each member had zero web activity.

Do NOT persist this individual DataFrame yet.

VALIDATION:

Log and validate:

- base population row count
- output row count
- distinct account_id + as_of_date
- duplicate count = 0
- null account_id = 0
- null as_of_date = 0
- distinct as_of_date count = 1
- snapshot exactly 2024-03-31
- future web-feature leakage = 0
- source row count
- whether source is available or empty
- null/unavailable feature counts when source is empty

If source contains future web records, log raw future-source presence separately, but fail only if a future record enters feature calculations.

Do not modify any existing completed feature module.

After implementation report:

1. Source availability status.
2. Exact reviewed features implemented.
3. Source field mappings used.
4. Features intentionally de-scoped.
5. Any unresolved mappings.
6. Validation metrics.
7. Confirmation of one-row-per-account snapshot grain.
8. Confirmation that unavailable UAT website features remain NULL rather than being incorrectly represented as zero.
