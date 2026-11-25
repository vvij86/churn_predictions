Read and strictly follow ".github/copilot-instructions.md" and "AGENTS.md".

We have completed manual Databricks historical feature coverage validation for the following three snapshots:

- 2023-04-30
- 2023-09-30
- 2024-03-31

All validation checks passed except "chk_future_event_violations", which failed consistently across all three snapshots. Source coverage confirmation returned the expected WARNING because historical source completeness is assumed.

Investigate the root cause of "chk_future_event_violations" in "feature_historical_coverage_validation.sql".

Specifically:

1. Identify the exact CTEs, conditions, source tables and date columns contributing to this failure.
2. Determine whether the validation incorrectly counts future events from raw source tables rather than events actually consumed by the feature engineering pipelines.
3. Review the corresponding Python feature modules and verify their point-in-time filtering against "as_of_date".
4. Distinguish actual data leakage from a false-positive SQL validation failure.
5. Provide lightweight, read-only diagnostic Databricks SQL queries to identify the failing feature category and violation counts.
6. Provide exact file and line references for any confirmed issue.
7. Review whether the overall validation status correctly propagates the source coverage confirmation WARNING.

Strict restrictions:

- Maintain one row per account_id and as_of_date.
- Continue using fundJoinDate for account eligibility as per existing approved rules.
- Do not use reportingDate for as-of-date filtering.
- Preserve newly joined account eligibility.
- Historical source start date remains 2023-04-01.
- AccountEngagementWeb remains empty; preserve NULL features.
- Do not reintroduce de-scoped workflow features.
- Do not modify base population, target labels, temporal split or historical snapshot orchestration.
- Do not change any files.
- Do not execute any code, SQL, terminal commands or Databricks jobs.

Provide root cause analysis, diagnostic SQL and recommended corrections only.
