Follow all repository instructions in ".github/copilot-instructions.md" and "AGENTS.md".

Address only the two identified historical coverage review findings.

1. Historical coverage utility

- Correct "ml_mscs_mrt_historical_coverage.py" so that the earliest observed source event date is not treated as proof of continuous historical coverage.
- Retain the configured historical source start date of 2023-04-01.
- Distinguish confirmed coverage, assumed coverage, partial coverage and unavailable coverage.
- Use reliable source coverage metadata if available. Otherwise, explicitly document the coverage assumption without claiming verified completeness.
- Do not infer source unavailability merely because a particular month has no transactions.
- Preserve the distinction between NULL and zero.

2. Investment feature module

- Correct "ml_mscs_mrt_investment_features.py" so that source-level coverage assessment is independent of eligible-account and point-in-time population filtering.
- Preserve existing point-in-time investment feature calculations.
- Do not use future investment observations as historical predictors.

3. Validation SQL

- Update "feature_historical_coverage_validation.sql" to align with the corrected coverage semantics.

Mandatory restrictions

- Maintain account-level grain: one row per account_id + as_of_date.
- Continue using fundJoinDate for account eligibility with existing approved base population rules.
- Do not use reportingDate for as-of-date filtering.
- Do not introduce minimum account tenure restrictions.
- Preserve existing approved feature names and business calculations.
- AccountEngagementWeb remains empty; preserve all web feature values as NULL.
- Do not reintroduce de-scoped workflow features.
- Do not modify base population, target labels, temporal split or historical snapshot orchestration.
- Modify other feature modules only if strictly necessary for compatibility with the shared coverage utility.
- Do not execute any scripts, SQL, notebooks, jobs or permanent table writes.

Provide a summary of modified files, corrected logic, remaining assumptions and manual Databricks validation steps for 2023-04-30, 2023-09-30 and 2024-03-31.
