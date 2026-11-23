Review and fix:

"notebook/ml_mscs_mrt_consolidated_features.py"

Current problem:

The pipeline is failing immediately in "_run_datasource_preflight_check()" because it explicitly executes:

"Class.forName("com.mongodb.spark.sql.DefaultSource", ...)"

and receives:

"NoClassDefFoundError: scala/Serializable"

This Mongo connector check is unrelated to the Member Retention ML pipeline and unrelated to writing our output as a Unity Catalog Delta table.

Yesterday we successfully verified from the SAME ML cluster that:

- current user/group is available
- "USE CATALOG mer_wealth_dev" succeeds
- "USE SCHEMA mer_wealth_mra_mlops" succeeds
- group "mer_wealth_mscs_ds_dev" has "ALL PRIVILEGES" on schema "mer_wealth_dev.mer_wealth_mra_mlops"
- schema/table listing succeeds

Therefore do NOT require MongoDB Spark connector availability as a prerequisite for Delta persistence.

Required fix

Remove or disable the Mongo-specific classpath check from the persistence preflight.

Specifically, do NOT call:

"Class.forName("com.mongodb.spark.sql.DefaultSource")"

and do NOT scan/load unrelated datasource providers merely to determine whether we can write a Delta table.

The pipeline only needs to persist to:

"mer_wealth_dev.mer_wealth_mra_mlops.member_retention_features"

using Delta / Unity Catalog.

Replace preflight with Delta-specific checks only

Before running the expensive feature pipeline, perform only lightweight checks such as:

1. Verify catalog exists/access:
   "mer_wealth_dev"

2. Verify schema exists/access:
   "mer_wealth_mra_mlops"

3. Verify current principal can access that catalog/schema.

4. Log the intended target table:
   "mer_wealth_dev.mer_wealth_mra_mlops.member_retention_features"

Do NOT create/load/test Mongo classes.

Do NOT add any other external connector dependency.

Do NOT make a dummy write if that would unnecessarily create/remove tables.

The real validated Delta write at the end of the pipeline should be the authoritative persistence test.

Actual persistence

Keep:

"persist_output=True"

for the current development main execution.

After the existing consolidated validation passes, write the validated snapshot to:

"mer_wealth_dev.mer_wealth_mra_mlops.member_retention_features"

using Spark/Delta only.

Maintain existing idempotent snapshot handling:

- grain = "account_id + as_of_date"
- rerunning "2024-03-31" must not duplicate rows
- existing other snapshots must not be deleted

Do not change:

- behavioural feature logic
- feature columns
- source mappings
- date-window logic
- base-population logic
- snapshot logic
- validation rules
- execution order unless required for persistence only

Error handling

If the ACTUAL Delta write itself fails, log the exact Delta-write exception separately.

Do not translate an unrelated Mongo connector problem into a Delta persistence failure.

For example clearly log:

"Delta persistence failed during actual table write"

with the real underlying exception.

Target module

Review:

"notebook/ml_mscs_mrt_target_labels.py"

and remove the same Mongo-specific preflight there if it exists.

Target persistence should depend only on Spark/Delta/Unity Catalog and write to:

"mer_wealth_dev.mer_wealth_mra_mlops.member_retention_ground_truth"

Do not alter target/churn business logic.

After changes report

Tell me:

1. where the Mongo-specific preflight was introduced
2. whether it has now been completely removed from consolidated and target persistence paths
3. what lightweight Delta/Unity Catalog preflight remains
4. confirmation that "persist_output=True"
5. confirmation of the exact features table
6. confirmation of the exact ground-truth table
7. confirmation that no feature or churn business logic changed
8. whether the code compiles successfully

Do NOT recommend changing/removing cluster libraries unless the actual Delta write subsequently fails because of the connector conflict.
