Optimize the existing Member Retention behavioural feature pipeline for performance and future multi-snapshot execution.

Follow ".github/copilot-instructions.md" strictly.

IMPORTANT:
Do NOT rewrite the pipeline from scratch.
Do NOT change any reviewed business logic, feature formulas, exclusions, source mappings, feature names, leakage rules, or final modelling grain.

The current single-snapshot consolidated pipeline works correctly for:

as_of_date = "2024-03-31"

but currently takes approximately 1 hour 20 minutes.

The objective of this task is:

PERFORMANCE OPTIMIZATION + CENTRAL CONFIGURATION + FUTURE MULTI-SNAPSHOT FOUNDATION.

Do NOT introduce module-level parallel execution in this task.

Existing modules include:

- notebook/ml_mscs_mrt_base_population.py
- notebook/ml_mscs_mrt_contribution_features.py
- notebook/ml_mscs_mrt_rollover_features.py
- notebook/ml_mscs_mrt_investment_features.py
- notebook/ml_mscs_mrt_insurance_features.py
- notebook/ml_mscs_mrt_helpline_features.py
- notebook/ml_mscs_mrt_campaign_features.py
- notebook/ml_mscs_mrt_web_engagement_features.py
- notebook/ml_mscs_mrt_third_party_authority_features.py
- notebook/ml_mscs_mrt_consolidated_features.py

Reviewed SQL references remain:

- behavioural_features_business_review.sql
- AccountEngagementWeb_Reviewed_Features.sql

1. Build Base Population Once

The consolidated pipeline must create the account-level base population exactly ONCE for each controlled snapshot.

Example:

base_population_df = run_base_population_pipeline(
spark,
as_of_date=configured_as_of_date
)

Do not allow individual feature modules to independently rerun the base-population pipeline when called from the consolidated pipeline.

Refactor feature pipeline entry points so they can optionally accept an already-created:

base_population_df

Conceptually:

run_contribution_feature_pipeline(
spark,
as_of_date,
base_population_df=base_population_df
)

Apply the same design to all feature modules.

When "base_population_df" is supplied:

- use it directly
- do not rebuild the account spine
- do not reread AccountSummary merely to recreate eligibility/base population

Preserve standalone execution capability for individual module development/testing.

Final grain must remain:

one row per account_id per as_of_date

2. Central Global Configuration

Create one central configuration module:

notebook/ml_mscs_mrt_config.py

Move genuine pipeline-global settings there.

At minimum include:

DEFAULT_AS_OF_DATE = "2024-03-31"

HISTORICAL_SOURCE_START_DATE = "2023-04-01"

FEATURE_WINDOW_MONTHS = 12

RECENT_WINDOW_DAYS = 90

PRIOR_WINDOW_DAYS = 90

SNAPSHOT_FREQUENCY = "monthly"

Supported future snapshot frequencies:

- monthly
- quarterly
- yearly

Also centralize source catalog/schema values if they are currently duplicated across modules and are genuinely global.

Do NOT move feature-specific business rules into global configuration.

3. Snapshot Frequency Foundation

Prepare reusable logic for future historical snapshot generation.

Do NOT generate multiple snapshots yet.

Create a deterministic snapshot-date generator supporting:

generate_snapshot_dates(
start_date,
end_date,
frequency
)

Supported frequency values:

- monthly
- quarterly
- yearly

Snapshot dates must be controlled modelling dates.

Do NOT derive snapshots from:

- reportingDate
- fundJoinDate
- exitDate
- transaction dates
- event dates
- system/current date

For the current regression test continue using:

2024-03-31

4. No Module-Level Parallel Execution

Do NOT run feature modules concurrently in this task.

Do NOT use:

- Python threading
- multiprocessing
- concurrent.futures
- parallel notebook execution
- multiple simultaneous Spark jobs initiated by this pipeline

Keep feature-module orchestration sequential for now.

Reason:
first remove unnecessary repeated reads/actions and establish a correct baseline.

Spark may continue to use its normal distributed execution internally.

Do not disable Spark's native parallelism.

5. Reduce Repeated Spark Work

Inspect the consolidated pipeline and all feature modules for unnecessary repeated Spark work.

Reduce where safe:

- repeated base-population reads
- repeated AccountSummary reads only for eligibility/base population
- repeated ".count()" calls
- repeated ".distinct().count()" calls when already available
- repeated schema inspections
- repeated source table loads
- repeated actions that recalculate identical lineage
- repeated display/show actions during normal pipeline execution

Do NOT remove critical validations.

If multiple validations can reuse already-calculated metrics, calculate them once and reuse them.

6. Cache/Persist Only Reusable DataFrames

Evaluate whether:

base_population_df

should be cached/persisted because every module reuses it.

If beneficial:

persist once before feature-module execution

and:

unpersist after the consolidated snapshot finishes.

Do NOT cache every feature DataFrame.

Only cache/persist where actual reuse justifies it.

Do not convert large Spark datasets to Pandas.
Do not collect large datasets to the driver.

7. Reuse Common Source Reads Where Safe

Inspect source usage across modules.

If multiple modules read exactly the same source table using compatible initial filters, consider introducing reusable source-loading helpers.

Examples may include common account/investment source reads.

However:

DO NOT combine reviewed feature logic.

DO NOT weaken feature-specific point-in-time filters.

DO NOT change business logic just for speed.

Correctness has higher priority than runtime.

8. Consolidated Pipeline Flow

Update:

notebook/ml_mscs_mrt_consolidated_features.py

so execution becomes conceptually:

1. Load global configuration.
2. Resolve controlled as_of_date.
3. Build base population once.
4. Persist base population if beneficial.
5. Execute feature modules sequentially.
6. Pass the same base_population_df and as_of_date to each module.
7. Join each result on:

account_id
as_of_date

8. Validate grain after joins.
9. Run final consolidated validation.
10. Log/display a small sample.
11. Unpersist reusable cached DataFrames.

Do NOT regenerate the base population between modules.

9. Preserve Existing Feature Logic Exactly

Do not alter formulas or definitions for:

- contribution behaviour
- inflow/change behaviour
- rollover behaviour
- investment behaviour
- insurance behaviour
- helpline behaviour
- campaign/event behaviour
- AccountEngagementWeb behaviour
- third-party authority behaviour

Reviewed SQL logic remains authoritative.

Do not reintroduce de-scoped features.

Web engagement source-unavailable behavior must continue to preserve NULL semantics.

10. Regression Validation

Run the optimized pipeline for:

as_of_date = "2024-03-31"

Validate at minimum:

- base population row count
- consolidated row count
- distinct account_id + as_of_date
- duplicate account_id + as_of_date = 0
- null account_id = 0
- null as_of_date = 0
- distinct as_of_date count = 1
- actual as_of_date = 2024-03-31
- future leakage count = 0
- no unexpected row multiplication
- no de-scoped features in final output
- web unavailable features remain NULL
- final feature names remain unchanged

The previous successful base population count was:

785885

Treat this as a regression reference only.

If the underlying Databricks source changed, report the new count rather than forcing 785885.

11. Runtime Instrumentation

Add concise timing logs around:

- base population
- contribution
- rollover
- investment
- insurance
- helpline
- campaign
- web engagement
- third-party authority
- joins
- final validation
- total consolidated runtime

Log duration in seconds and minutes.

This is mandatory so we can compare against the previous approximately:

1 hour 20 minutes.

12. Validation Performance

Review validations themselves for expensive repeated Spark actions.

Where possible:

- aggregate multiple validation metrics in one Spark action
- reuse calculated counts
- avoid triggering the same lineage repeatedly

Do NOT weaken:

- grain checks
- leakage checks
- null-key checks
- snapshot checks

13. Persistence

Do NOT save the final consolidated dataset to a permanent Databricks table in this task.

First complete optimization and regression validation.

Permanent DEV-table persistence will be the next step after the optimized pipeline is proven correct.

14. Expected Report

After implementation and execution, provide:

1. Files changed
2. Global config values introduced
3. Base-population reuse approach
4. Any shared-source reuse introduced
5. DataFrames persisted/cached and why
6. Repeated Spark actions removed/reduced
7. Confirmation that module execution remains sequential
8. Confirmation that Spark-native distributed execution remains enabled
9. Snapshot-frequency configuration design
10. Regression validation results
11. Runtime for each module
12. Total optimized runtime
13. Previous runtime comparison
14. Percentage/runtime improvement if measurable
15. Remaining performance bottlenecks
16. Recommendation before enabling multiple historical snapshots

Do NOT implement:

- target generation
- model training
- MLflow
- permanent feature-table persistence
- multi-snapshot execution
- module-level parallel execution

in this task.

This task is strictly:

OPTIMIZE THE EXISTING CORRECT SINGLE-SNAPSHOT PIPELINE WITHOUT CHANGING BUSINESS LOGIC.
