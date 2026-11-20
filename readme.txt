Create a new Python file directly under the existing "notebook" folder named:

"ml_mscs_mrt_insurance_features.py"

Follow ALL rules from:

".github/copilot-instructions.md"

Do not create any subfolder under "notebook".

Purpose

Build the reviewed Insurance Behaviour / Cover Position features for Member Retention Analytics using Databricks / PySpark.

Final grain MUST remain:

"one row per account_id per as_of_date"

Reuse the account-level base population from:

"ml_mscs_mrt_base_population.py"

Do not independently rebuild the base-population logic.

Reference SQL

Use:

"behavioural_features_business_review.sql"

as the primary business-logic reference for Insurance Behaviour / Cover Position.

Review the insurance section before implementing.

Do not blindly copy SQL Server syntax or source names.

Map the reviewed logic to the Databricks "mscs_mrt_*" source tables.

Databricks Source

Catalog:

"mer_wealth_dev"

Schema:

"mer_wealth_landing_edge"

Primary insurance source:

"mer_wealth_dev.mer_wealth_landing_edge.mscs_mrt_account_insurance_current"

Only use "mscs_mrt_*" source tables.

Before implementing:

- inspect/log the actual source schema
- identify account ID
- identify Death cover fields
- identify TPD cover fields
- identify Income Protection cover fields
- identify effective/snapshot dates if present
- identify cover type fields required for the reviewed logic

Do not invent unavailable fields.

If a reviewed source mapping cannot be confirmed:

- log the issue
- add a clear TODO/comment
- do not fabricate feature values

Base Population

Reuse:

"base_population_df"

from:

"ml_mscs_mrt_base_population.py"

All calculations must remain relative to:

"account_id"
"as_of_date"

The implementation must remain compatible with future multiple historical AsOfDate snapshots.

Reviewed Insurance Features

Implement ONLY these reviewed features:

- "has_death_cover_asof"
- "has_tpd_cover_asof"
- "has_ip_cover_asof"
- "insurance_cover_type_count_asof"

These are the reviewed KEEP features.

Do NOT include the following de-scoped insurance amount features in the final output:

- "death_cover_amount_asof"
- "tpd_cover_amount_asof"
- "ip_cover_amount_asof"

The amount fields may be used internally if required to derive the corresponding cover flags, but they must not appear as final modelling features.

Cover Flag Logic

Follow the reviewed SQL/business logic.

The final flags should represent whether valid cover exists as at "as_of_date".

Expected output:

- "1" = cover exists
- "0" = no cover

Use Boolean-safe logic where source fields are Boolean.

Do not compare Boolean fields with integer values.

If amount fields are used internally to infer cover presence, preserve the reviewed business definition.

Do not create a new interpretation.

Insurance Cover Type Count

Calculate:

"insurance_cover_type_count_asof"

as the number of reviewed cover types present as at the snapshot.

The count should be based on:

- Death
- TPD
- Income Protection

Example:

Death = 1
TPD = 1
IP = 0

Then:

"insurance_cover_type_count_asof = 2"

Do not count historical insurance records multiple times.

Point-in-Time Rules

Where the insurance source contains historical/effective dates:

- use only records valid on or before "as_of_date"
- exclude future insurance records
- select the appropriate latest/valid record for the account as at that snapshot

If "mscs_mrt_account_insurance_current" contains only a current-state record and does not support historical reconstruction, log this limitation clearly.

Do not fabricate historical insurance states.

Output

Create:

"insurance_features_df"

Final columns should be:

- "account_id"
- "as_of_date"
- "has_death_cover_asof"
- "has_tpd_cover_asof"
- "has_ip_cover_asof"
- "insurance_cover_type_count_asof"

Final grain:

"one account_id + one as_of_date = one row"

Accounts with no insurance cover must still remain in the output because the base population is the driving dataset.

Logging and Exception Handling

Follow the same logging pattern used in:

- "ml_mscs_mrt_base_population.py"
- "ml_mscs_mrt_contribution_features.py"
- "ml_mscs_mrt_rollover_features.py"
- "ml_mscs_mrt_investment_features.py"

Use:

- "logger.info()" for normal execution
- "logger.warning()" for non-critical data issues
- "logger.exception()" inside exception handlers
- re-raise critical exceptions

Log:

- base population load
- insurance source load
- schema validation
- source field mapping
- Death cover calculation
- TPD cover calculation
- IP cover calculation
- cover type count calculation
- final aggregation
- validation
- successful completion

Do not add MLflow autologging.

Spark Session Handling

Use the reusable Spark-session pattern already implemented in the other ML files.

Pass the active SparkSession explicitly.

Do not rely on a module-global "spark" variable when imported.

Importing this module must not automatically execute the pipeline.

Keep it compatible with the Databricks ML shared cluster and the existing VS Code / Databricks workflow.

Validation

Validate and log:

- base population row count
- output row count
- distinct "account_id + as_of_date"
- duplicate "account_id + as_of_date"
- null "account_id"
- null "as_of_date"
- invalid "has_death_cover_asof" values
- invalid "has_tpd_cover_asof" values
- invalid "has_ip_cover_asof" values
- invalid "insurance_cover_type_count_asof"
- cover type count > 3
- cover type count < 0
- future insurance leakage count, where historical dates are available
- distribution/count of each insurance flag

Critical requirements:

- duplicate grain count = 0
- null key counts = 0
- cover flags contain only 0 or 1
- cover type count must be between 0 and 3
- output row count must not increase because of join multiplication
- future leakage count must be 0 where the source supports historical dating

Modularity

Prefer helper functions such as:

- "load_insurance_source()"
- "validate_insurance_source()"
- "build_insurance_features()"
- "validate_insurance_features()"
- "run_insurance_feature_pipeline()"

Persistence

Do NOT save this individual DataFrame as a Databricks table yet.

Final output:

"insurance_features_df"

The consolidated feature dataset will be persisted later after all reviewed feature blocks are assembled and validated.

Final Check

Before finalizing:

1. Read ".github/copilot-instructions.md".
2. Review the Insurance Behaviour / Cover Position section in "behavioural_features_business_review.sql".
3. Inspect the actual schema of "mscs_mrt_account_insurance_current".
4. Implement only:
   - "has_death_cover_asof"
   - "has_tpd_cover_asof"
   - "has_ip_cover_asof"
   - "insurance_cover_type_count_asof"
5. Do not output:
   - "death_cover_amount_asof"
   - "tpd_cover_amount_asof"
   - "ip_cover_amount_asof"
6. Preserve final grain at "account_id + as_of_date".
7. Preserve point-in-time/no-leakage rules where supported.
8. Do not alter existing contribution, rollover, investment or base-population business logic.
9. Do not modify unrelated Data Engineering or Power BI files.
