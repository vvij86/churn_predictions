Fix the current execution issue between:

"ml_mscs_mrt_base_population.py"

and

"ml_mscs_mrt_contribution_features.py"

Current error:

"RuntimeError: This module must be executed in a Databricks notebook/runtime with an active Spark session."

The error occurs when "ml_mscs_mrt_contribution_features.py" imports:

"run_base_population_pipeline"

from:

"ml_mscs_mrt_base_population.py"

Do NOT change any existing business logic, filtering rules, feature calculations, source mappings, validation rules or output grain.

This change is ONLY to correct Spark-session handling and Python module reuse.

Required Refactoring

1. Do not rely on the Databricks notebook global "spark" variable inside reusable imported modules.

2. Pass the active SparkSession explicitly into reusable pipeline functions.

For example, refactor functions as appropriate to accept:

"spark"

or:

"spark_session"

as a parameter.

Examples:

"load_account_summary(spark_session)"

"run_base_population_pipeline(spark_session, as_of_date=AS_OF_DATE)"

"load_contribution_source(spark_session)"

"run_contribution_feature_pipeline(spark_session)"

3. Update all internal calls accordingly.

4. In "ml_mscs_mrt_contribution_features.py", call the imported base-population pipeline using the currently active Databricks Spark session.

Conceptually:

"base_population_df = run_base_population_pipeline(spark_session=spark)"

5. Remove the current pattern that sets:

"spark = None"

when the module is imported if it causes the reusable module to lose access to the caller's Spark session.

6. "ml_mscs_mrt_base_population.py" must remain reusable as a Python module.

Importing:

"run_base_population_pipeline"

must NOT automatically execute the entire base-population pipeline.

7. Move direct execution of the base-population pipeline behind:

if __name__ == "__main__":
    ...

or an equivalent Databricks-safe execution guard.

The important requirement is:

Importing "ml_mscs_mrt_base_population.py" must define its functions without automatically running the pipeline.

8. Apply the same execution pattern to:

"ml_mscs_mrt_contribution_features.py"

so that functions can be reused later by feature-assembly code without automatically executing during import.

9. When either file is executed directly as a Databricks job, it should still run its respective pipeline successfully.

10. Preserve all existing logging and exception handling.

11. Preserve:

Base population final DataFrame:
"base_population_df"

Contribution feature final DataFrame:
"contribution_features_df"

12. Preserve final grain:

"one row per account_id per as_of_date"

13. Do not change:

- "mer_wealth_dev"
- "mer_wealth_landing_edge"
- "mscs_mrt_account_summary"
- "mscs_mrt_account_money_inflow"
- AsOfDate logic
- historical start date
- eligibility rules
- contribution business rules
- contribution windows
- feature definitions
- validation rules

14. After refactoring, verify that:

- "ml_mscs_mrt_base_population.py" can run independently as a Databricks job
- "ml_mscs_mrt_contribution_features.py" can reuse the base population successfully
- importing the base-population module does not execute it automatically
- the active Spark session is correctly available to both modules
- existing base-population validation results remain unchanged

Do not introduce SparkSession.builder configuration or local Spark configuration that could conflict with Databricks serverless/job compute. Reuse the active Databricks Spark session supplied by the caller.
