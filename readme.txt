Change the ML pipeline architecture to reduce memory pressure by using persisted Delta tables between the consolidated-feature stage and target-label stage.

Follow ".github/copilot-instructions.md" strictly.

Important:

- Do NOT change any reviewed behavioural feature business logic.
- Do NOT change churn definition.
- Do NOT change target definition.
- Do NOT change account_id + as_of_date grain.
- Do NOT introduce parallel execution.
- Do NOT add aggressive repartitioning/broadcasting unless clearly justified.

Current cluster is only:

- 16 GB
- 4 cores

We have repeatedly hit Spark/JVM out-of-memory issues while target generation tries to operate over the full consolidated feature lineage.

Required architecture change

Stage 1 — Consolidated behavioural features

Update:

"notebook/ml_mscs_mrt_consolidated_features.py"

After all existing consolidated validations PASS, optionally persist the validated consolidated feature snapshot as a Delta table.

Use:

Catalog:
"mer_wealth_dev"

Schema:
"mer_wealth_mra_mlops"

Table:

"mer_wealth_dev.mer_wealth_mra_mlops.member_retention_features"

The table must have:

"account_id + as_of_date"

as the unique logical grain.

For the current run:

"as_of_date = 2024-03-31"

Persistence must occur ONLY after the existing consolidated validation status is PASS.

Use an idempotent snapshot write strategy:

- rerunning the same as_of_date must not create duplicate records
- existing other snapshot dates must not be overwritten

Prefer controlled replace/overwrite of ONLY the current "as_of_date" partition or a Delta MERGE approach.

Do NOT blindly append.

After successful persistence:

- unpersist any cached DataFrames
- release large intermediate DataFrames where practical
- do not keep the entire consolidated feature lineage in memory for target generation

Stage 2 — Target labels

Update:

"notebook/ml_mscs_mrt_target_labels.py"

Do NOT rebuild "ml_mscs_mrt_consolidated_features.py" inside this target module.

Instead read the already validated persisted feature snapshot from:

"mer_wealth_dev.mer_wealth_mra_mlops.member_retention_features"

and filter immediately to the required controlled:

"as_of_date"

Only select columns actually required for the target join and final output.

Generate "target_churn" using the existing reviewed churn definition.

For churn source tables:

- filter by the required outcome date window BEFORE expensive joins
- select only required columns
- aggregate churn events to "account_id + as_of_date" before joining back to the wide feature table wherever possible

Avoid joining raw many-row event tables directly to the 89-column consolidated feature DataFrame.

Preferred flow:

1. Read persisted feature snapshot.
2. Create a narrow account spine containing only:
   - account_id
   - as_of_date
   - only eligibility/reference columns actually needed for target generation.
3. Generate a small/narrow target DataFrame at:
   "account_id + as_of_date"
4. Validate target DataFrame.
5. Join the final single-row target back to the persisted consolidated feature dataset only once at the end.

This is important to prevent row explosion and expensive wide-table shuffles.

Memory/caching requirements

Avoid MEMORY_ONLY caching.

Do not cache the full consolidated wide DataFrame in target generation.

Do not cache large raw event tables.

Prefer rereading the persisted Delta snapshot over keeping a very long Spark lineage in memory.

If temporary persistence is genuinely needed, explain why before using it and prefer disk-friendly persistence.

Do NOT use:

- toPandas()
- large collect()
- large display()
- Python iteration over Spark rows

Only collect single-row aggregate validation metrics.

For sample output use:

"df.limit(10).show(truncate=False)"

Target output persistence

After target validation PASS, persist the final ground-truth dataset to:

"mer_wealth_dev.mer_wealth_mra_mlops.member_retention_ground_truth"

Again use an idempotent snapshot strategy.

Do not overwrite other historical "as_of_date" snapshots.

Validation

Preserve the existing:

"FINAL CONSOLIDATED VALIDATION SUMMARY"

and:

"GROUND TRUTH DATASET VALIDATION SUMMARY"

Required target checks remain:

- final row count equals feature snapshot row count
- duplicate account_id + as_of_date = 0
- null account_id = 0
- null as_of_date = 0
- target_churn only 0/1
- null target = 0 for eligible rows
- churn count
- retained count
- churn percentage
- internal-transfer leakage = 0
- outcome-window leakage = 0
- deceased eligibility rules preserved

Current single-snapshot objective

First make only:

"2024-03-31"

work successfully.

Do NOT create the multi-snapshot loop yet.

After implementing, tell me:

1. which latest memory-oriented changes were replaced
2. exact consolidated Delta table name
3. exact ground-truth Delta table name
4. whether target generation now reads the persisted feature table instead of rebuilding consolidated features
5. whether any large DataFrame caching remains
6. how same-snapshot reruns avoid duplicates
7. whether behavioural feature logic changed
8. whether churn logic changed
9. whether the target join is now performed on a narrow account/target DataFrame before joining to the wide feature table
