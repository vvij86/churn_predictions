Follow all repository ML instructions in ".github/copilot-instructions.md" and "AGENTS.md".

Implement strict point-in-time leakage validation for the existing Member Retention Analytics feature engineering modules.

The previous historical coverage validation for all three representative snapshots returned NOT VALIDATED because structured runtime leakage evidence was unavailable to the validation SQL.

Requirements

1. Review and reuse existing runtime leakage counters wherever they correctly validate the actual feature-consumed DataFrames.

2. Correct incomplete or logically redundant leakage checks. Validate the actual records consumed by feature calculations before aggregation, rather than separately filtering raw source records to artificially produce zero violations.

3. Cover all applicable feature modules:
   
   - Contribution
   - Rollover
   - Investment
   - Helpline
   - Campaign
   - Web engagement
   - Third-party authority
   - Insurance
   - Account profile, where applicable

4. Create a reusable mechanism to expose runtime leakage evidence through a session-level temporary view containing:
   
   - as_of_date
   - module_name
   - leakage_count
   - evidence_scope
   - evidence_status
   - evidence_note

5. Update "feature_historical_coverage_validation.sql" to consume this evidence:
   
   - FAIL when actual leakage is detected.
   - PASS when all applicable checks have valid runtime evidence and zero violations.
   - NOT VALIDATED when required evidence is missing or insufficient.
   - Explicitly distinguish unavailable sources and non-applicable checks.
   - Keep raw future source presence as an informational diagnostic, not actual leakage.
   - Preserve existing source coverage warnings.

6. Where practical, provide a small independent test that verifies feature outputs remain unchanged when future-dated events are introduced into test inputs.

Mandatory restrictions

- Maintain account-level grain: one row per account_id + as_of_date.
- Continue using fundJoinDate for account eligibility.
- Do not use reportingDate for as-of-date filtering.
- Historical source start date remains 2023-04-01.
- Newly joined accounts remain eligible.
- AccountEngagementWeb is still empty; preserve all web feature values as NULL.
- Do not use current-state insurance attributes when historical validity cannot be established.
- Do not reintroduce de-scoped workflow features.
- Do not modify approved business feature calculations or predictor schemas.
- Do not modify base population, target labels, temporal split, consolidated feature integration or historical snapshot orchestration.
- Avoid expensive repeated source scans and unnecessary count operations.
- Do not create persistent tables.
- Do not execute notebooks, scripts, SQL or Databricks jobs.

Expected deliverables

- Minimal required Python changes.
- Updated historical coverage validation SQL.
- Complete copy-paste-ready Databricks notebook execution code.
- Validation instructions for 2023-04-30, 2023-09-30 and 2024-03-31.
- Summary of modified files and remaining limitations.

Do not artificially force any validation status to PASS.
