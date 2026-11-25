Read and strictly follow ".github/copilot-instructions.md" and "AGENTS.md".

We have completed historical coverage validation for the following snapshots:

- 2023-04-30
- 2023-09-30
- 2024-03-31

All other reported structural validation checks passed. Source coverage confirmation remains WARNING, and strict future event leakage remains NOT VALIDATED because runtime feature-consumption evidence is unavailable to the validation SQL.

Perform a read-only review of all existing active ML feature engineering modules.

1. Identify existing runtime point-in-time leakage validation counters in each feature module.
2. Confirm whether these counters validate the actual records consumed during feature computation.
3. Check whether existing runtime counters can be reused without modifying feature modules.
4. Identify any feature modules where runtime leakage evidence is missing or incomplete.
5. Recommend the simplest approach to expose runtime leakage validation results to "feature_historical_coverage_validation.sql".
6. Do not artificially mark leakage validation as PASS by independently filtering raw source records.

Mandatory constraints:

- Maintain one row per account_id + as_of_date.
- Preserve existing fundJoinDate-based eligibility rules.
- Do not use reportingDate for as-of-date filtering.
- Historical source start date remains 2023-04-01.
- Newly joined accounts remain eligible.
- AccountEngagementWeb is still empty. Preserve NULL outputs.
- Workflow features remain de-scoped.
- Do not modify base population, target labels, temporal split or historical snapshot orchestration.
- Do not modify any files, execute code or write to Databricks tables.

Provide a module-wise review table containing existing leakage counters, validation evidence, gaps, file and line references, and recommended minimal changes.
