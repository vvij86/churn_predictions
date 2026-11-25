Read and strictly follow ".github/copilot-instructions.md" and "AGENTS.md".

Create a single reusable Python validation runner under the existing notebook folder:

"ml_mscs_mrt_feature_validation.py"

Do not generate any Jupyter notebook (.ipynb).

Objective:

Automate the existing historical coverage and runtime leakage validation process using the already implemented Python feature modules and validation SQL.

Implementation requirements:

1. Inspect the actual function signatures, imports, return types and dependencies of existing modules before writing code.
2. Reuse existing implementations. Do not duplicate or redesign feature engineering logic.
3. Provide a single entry-point function named "run_feature_validation(spark, as_of_date)".
4. Generate the base population once and reuse it across all eight existing feature pipelines.
5. Initialize and capture actual runtime leakage evidence using the existing runtime leakage evidence module.
6. Register all temporary feature views, required source views and "tmp_runtime_leakage_evidence".
7. Load and execute the existing "feature_historical_coverage_validation.sql" using a reliable path relative to the repository structure.
8. Return the final validation result as a Spark DataFrame.
9. Log module-wise execution progress, elapsed time and meaningful error messages identifying the failing module.
10. Avoid redundant count operations and repeated source scans where possible.
11. Use existing Databricks-compatible import conventions and support Serverless compute.
12. Perform static checks for import correctness, function arguments, SQL dependencies and temporary view names before completing implementation.

Mandatory business rules:

- Maintain one row per account_id per as_of_date.
- Reuse existing base population eligibility rules.
- Use fundJoinDate for account eligibility.
- Never use reportingDate for as-of-date filtering.
- Historical source start date: 2023-04-01.
- Newly joined accounts must remain eligible.
- AccountEngagementWeb is empty; preserve NULL values.
- Respect existing insurance historical limitations.
- Do not reintroduce de-scoped workflow features.
- Never fabricate leakage evidence or artificially force validation to PASS.
- Preserve NOT VALIDATED when sufficient evidence is unavailable.

Strict restrictions:

- Create only the requested Python file.
- Do not modify existing Python modules or SQL files.
- Do not modify base population, target labels, historical snapshots or temporal split logic.
- Do not create, overwrite or delete permanent Databricks tables.
- Do not execute Databricks jobs, notebooks or SQL.
- Do not introduce unnecessary dependencies or additional helper files.

Finally, provide only a concise implementation summary and the minimal Databricks notebook code required to invoke the validation runner.

If any existing dependency prevents implementation, report the exact blocker instead of making assumptions or modifying unrelated files.
