Create the next stage of the Member Retention ML training-data pipeline: a controlled multi-snapshot historical runner.

Follow ".github/copilot-instructions.md" strictly.

The single-snapshot pipeline is already validated successfully for:

"as_of_date = 2024-03-31"

Current validated outputs:

Feature table:
"mer_wealth_dev.mer_wealth_mra_mlops.member_retention_features"

Ground-truth table:
"mer_wealth_dev.mer_wealth_mra_mlops.member_retention_ground_truth"

Current grain:

"one row per account_id + as_of_date"

The current single snapshot has passed:

- duplicate count = 0
- null key counts = 0
- future feature leakage = 0
- target leakage = 0
- internal transfer leakage = 0
- deceased eligibility violations = 0
- target validation = PASS

Do NOT change any existing feature or churn business logic.

Objective

Create a new orchestration module, for example:

"notebook/ml_mscs_mrt_historical_snapshots.py"

Its only responsibility is to orchestrate the already validated feature and target pipelines over multiple controlled monthly snapshot dates.

Do NOT copy/reimplement feature engineering or target logic in this file.

Reuse:

- "ml_mscs_mrt_consolidated_features.py"
- "ml_mscs_mrt_target_labels.py"
- "ml_mscs_mrt_config.py"

Snapshot generation

Use the existing central snapshot-date generation/config.

Do NOT derive snapshot dates from:

- reportingDate
- fundJoinDate
- exitDate
- transaction/event dates
- system/current date

Snapshot dates must be explicitly/config-driven.

For the first test, run ONLY these three monthly snapshots:

- "2024-03-31"
- "2024-04-30"
- "2024-05-31"

Make this date range configurable so we can later extend it without changing business logic.

Do NOT launch the complete historical range yet.

Processing order

Process snapshots sequentially for now.

Do NOT introduce Python threads, multiprocessing, concurrent futures, parallel notebooks, or simultaneous snapshot execution.

For each snapshot:

1. Log snapshot start time.
2. Run consolidated feature generation for that controlled "as_of_date".
3. Validate feature dataset.
4. Persist only if feature validation PASS.
5. Run target generation using the persisted feature snapshot.
6. Validate ground-truth dataset.
7. Persist only if target validation PASS.
8. Log snapshot completion status and runtime.
9. Continue to the next snapshot only according to explicit failure-handling rules.

Persistence

Continue using:

"mer_wealth_dev.mer_wealth_mra_mlops.member_retention_features"

and:

"mer_wealth_dev.mer_wealth_mra_mlops.member_retention_ground_truth"

Both tables must contain multiple "as_of_date" snapshots.

Do NOT create separate physical tables for each month.

Maintain idempotent behavior:

- rerunning an existing snapshot must not duplicate "account_id + as_of_date"
- rerunning one snapshot must not delete other snapshots
- use the existing MERGE / snapshot-safe persistence logic

Performance

We are currently temporarily running on Databricks Serverless while the shared ML cluster library issue is being fixed.

The single consolidated snapshot completed successfully on Serverless in about 5 minutes.

Do not unnecessarily rebuild the same snapshot more than once.

The target pipeline must read the already persisted feature snapshot rather than rerunning feature engineering.

Avoid unnecessary:

- collect()
- toPandas()
- display of large DataFrames
- repeated counts
- cache/persist of large DataFrames
- orderBy/sort operations

Keep Spark processing distributed.

Failure handling

For each snapshot, capture:

- feature status
- target status
- feature runtime
- target runtime
- failure stage
- concise exception message

If feature validation fails for a snapshot:

- do NOT persist that snapshot
- do NOT run target generation for it
- mark snapshot FAILED

If target validation fails:

- feature snapshot may remain persisted if it had already passed
- do NOT persist invalid ground truth
- mark target stage FAILED

Do not silently skip errors.

For the initial 3-snapshot test, stop the overall run on the first critical failure so we can investigate before continuing.

Final historical-run summary

At the end print a concise table/summary such as:

Snapshot | Feature Status | Feature Rows | Target Status | Churn Rows | Churn % | Runtime

Also print:

- requested snapshot count
- successful snapshot count
- failed snapshot count
- total runtime
- overall PASS/FAIL

Validation after all 3 snapshots

Verify in both Delta tables:

- all requested "as_of_date" values exist
- no duplicate "account_id + as_of_date"
- row counts by snapshot
- target distribution by snapshot
- no snapshot was accidentally overwritten
- historical table contains more than one distinct "as_of_date"

Do not create train/validation/test splits yet.

Do not start model training yet.

After implementation report

Tell me:

1. new file created
2. exact three snapshot dates configured
3. whether snapshots run sequentially
4. how feature pipeline receives each controlled "as_of_date"
5. how target pipeline receives the same "as_of_date"
6. confirmation that existing business logic was not duplicated or changed
7. confirmation that persistence remains idempotent
8. expected tables updated
9. failure-handling behavior
10. command/file I should run to execute the 3-snapshot test
