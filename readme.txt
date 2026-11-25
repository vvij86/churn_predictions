Read and strictly follow ".github/copilot-instructions.md" and "AGENTS.md".

Based on the completed read-only root cause analysis, correct "feature_historical_coverage_validation.sql".

Implement the following targeted corrections:

1. Separate raw future source event presence from actual feature leakage.
2. Rename the existing raw future event check to "raw_future_source_presence" and treat it as informational diagnostics only. Future events existing in raw historical sources are expected and must not cause validation failure.
3. Retain a strict future-event leakage validation using actual feature-consumed records or existing runtime validation evidence from the Python modules.
4. Do not merely replicate as_of_date filtering in SQL and claim that leakage validation passed. If actual consumption evidence is unavailable, return NOT VALIDATED and explain the additional evidence required.
5. Propagate "chk_source_coverage_confirmation = WARNING" into the overall validation status.
6. Ensure genuine leakage violations still result in FAIL.
7. Preserve all existing population reconciliation, duplicate key, historical coverage, contribution NULL handling, ratio guardrails and web NULL handling checks.

Mandatory restrictions:

- Maintain account-level grain: one row per account_id and as_of_date.
- Use fundJoinDate for account eligibility according to existing approved rules.
- Never use reportingDate for as-of-date filtering.
- Historical source start date remains 2023-04-01.
- Newly joined accounts remain eligible without minimum tenure restrictions.
- AccountEngagementWeb is still empty. Preserve NULL behaviour.
- Do not reintroduce workflow features.
- Do not modify existing Python feature modules, base population, target labels, temporal split, consolidated features or historical snapshot orchestration.
- Modify only "feature_historical_coverage_validation.sql".
- If Python changes are necessary to expose actual leakage validation evidence, report them separately without implementing them.
- Do not execute any code, SQL, terminal commands, notebooks or Databricks jobs.
- Do not create or overwrite persistent tables.

Provide a summary of changes, expected validation results and exact manual Databricks execution steps.
