Review:

"notebook/ml_mscs_mrt_target_labels.py"

The Databricks run failed with:

"Py4JJavaError"
"JVM_OUT_OF_MEMORY"
"java.lang.OutOfMemoryError: Java heap space"
during "collectToPythonFile".

Current cluster:

- 16 GB
- 4 cores

Fix the implementation for Spark/Databricks memory efficiency.

Requirements:

- Do NOT change churn business rules.
- Do NOT change target definition.
- Do NOT change account_id + as_of_date grain.
- Do NOT change behavioural feature logic.

Identify any use of:

- collect()
- toPandas()
- collectToPython()
- large display()
- large show()
- Python-side iteration over Spark rows
- conversion of large Spark DataFrames to local Python objects

Remove or replace them with Spark-native aggregations.

Validation metrics such as:

- row count
- churn count
- retained count
- duplicate count
- null target count
- invalid target count
- leakage counts
- churn percentage

should be calculated using Spark aggregations and return only a single small metrics row to the driver.

Where possible, calculate multiple validation metrics in ONE "agg()" action rather than separate full DataFrame scans.

Do not collect account-level records to Python.

Only display a very small sample using "limit(10)" if needed.

Also review whether unnecessary caching/persisting of large DataFrames is causing driver/executor memory pressure. Persist only DataFrames that are genuinely reused and unpersist them promptly.

Keep the final "GROUND TRUTH DATASET VALIDATION SUMMARY".

After fixing, tell me:

1. exact cause of the OOM
2. which collect/toPandas/display operations were removed or changed
3. whether validation Spark actions were reduced
4. whether any business logic changed
5. whether the existing 16 GB / 4-core cluster should be sufficient after the fix
