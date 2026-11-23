Fix the Unity Catalog preflight in:

"notebook/ml_mscs_mrt_consolidated_features.py"

Current error:

"[UC_INVALID_NAMESPACE] Nested or empty namespaces are not supported in Unity Catalog"

The failing code is effectively doing:

"USE SCHEMA mer_wealth_dev.mer_wealth_mra_mlops"

This is incorrect after setting the catalog.

Change the preflight to use:

spark.sql("USE CATALOG mer_wealth_dev")
spark.sql("USE SCHEMA mer_wealth_mra_mlops")

Do NOT use:

"USE SCHEMA mer_wealth_dev.mer_wealth_mra_mlops"

For fully-qualified table references, continue using:

"mer_wealth_dev.mer_wealth_mra_mlops.member_retention_features"

Also review "ml_mscs_mrt_target_labels.py" for the same incorrect "USE SCHEMA catalog.schema" pattern and fix it there too.

Do not change:

- feature logic
- churn logic
- target logic
- validation logic
- snapshot logic
- persistence table names
- grain

Keep "persist_output=True".

After the change confirm:

1. "USE CATALOG mer_wealth_dev"
2. "USE SCHEMA mer_wealth_mra_mlops"
3. exact features table remains "mer_wealth_dev.mer_wealth_mra_mlops.member_retention_features"
4. exact ground-truth table remains "mer_wealth_dev.mer_wealth_mra_mlops.member_retention_ground_truth"
5. no business logic changed
