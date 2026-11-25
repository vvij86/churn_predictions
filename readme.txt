We are continuing the Member Retention Analytics ML feature engineering development in Databricks.

1. Mandatory repository instructions

Before making any changes:

- Read and strictly follow copilot-instructions.md and all other applicable repository instructions.md files.
- Review the existing configuration, historical base population, historical snapshot orchestration, consolidated feature logic and individual feature engineering modules.
- Review behavioural_features_business_review.sql and approved feature definitions.
- Preserve previously established business rules, architectural decisions and coding conventions.
- Do not override repository instructions.

2. Current development status

- Historical snapshot generation completed.
- Ground-truth generation completed with 32,616,602 records across 40 monthly snapshots.
- Ground-truth sanity checks completed against existing business rules.
- Temporal splitting implementation and dry run completed.
- Account profile features implemented and initially validated for 2024-03-31.
- Workflow behaviour features are de-scoped. The recently generated workflow Python and validation SQL files have been deleted. Do not recreate or integrate them.
- ATO-related churn clarification is pending business confirmation.
- AccountEngagementWeb still contains no data.

3. Objective

Review and improve historical source coverage and NULL handling across the existing active feature engineering modules.

Do not unnecessarily rewrite existing feature calculations or introduce additional business features.

4. Mandatory historical population rules

- Never use AccountSummary.reportingDate for historical filtering, snapshot selection, source row selection or ordering.
- reportingDate and exitDate are identical in many MercerEdge records.
- Use fundJoinDate <= as_of_date for account joining eligibility.
- Reuse the existing validated historical base population logic.
- Maintain exactly one row per account_id per as_of_date.
- Preserve all eligible historical account snapshot records.
- Do not introduce additional population exclusions or minimum tenure requirements.

5. Historical coverage handling

Existing configuration:

- Historical source start date: 2023-04-01.
- Feature lookback window: 12 months.
- Recent window: 90 days.
- Prior window: 90 days.

Review how each existing feature module handles historical windows when the full requested history is unavailable.

For example:

- Snapshot: 2023-09-30.
- Requested lookback: 12 months.
- Potentially available source history: approximately six months.

Implement consistent handling of:

- Fully available historical windows.
- Partially available historical windows.
- Completely unavailable historical windows.
- Accounts with shorter tenure.
- Source-specific historical availability.

Do not assume every source table has complete data from 2023-04-01.

Reuse existing configuration parameters wherever possible.

Distinguish the effective observable feature window from the originally requested feature window.

Do not extrapolate or artificially inflate observed activity to compensate for missing historical coverage.

6. NULL and zero handling

Apply the following principles consistently:

- Zero represents confirmed absence of qualifying activity within an observable period.
- NULL represents unavailable, insufficient or historically unverifiable information where the feature cannot be reliably calculated.
- Do not blindly use fillna(0), COALESCE or equivalent defaulting logic across all features.
- Do not interpret missing historical records as proof of no account activity.
- Preserve observed activity where partially available history supports a valid calculation, while documenting the coverage limitation.
- For ratios, trends and recent-versus-prior comparisons, ensure the underlying observation windows are sufficiently available and comparable.
- Handle zero denominators safely.
- Preserve existing approved feature-specific NULL handling.

Identify each feature requiring complete historical coverage versus features that can be calculated reliably using partial history.

7. Source-specific restrictions

AccountEngagementWeb:

- The source currently contains no data.
- Preserve all existing web engagement feature columns as NULL wherever source data is unavailable.
- Do not populate these features with artificial zeros.
- Ensure empty source data does not cause pipeline failures or loss of base population records.

Insurance:

- Do not assume current insurance status represents historical insurance status.
- Preserve NULL where historical validity cannot be established.
- Document unresolved insurance point-in-time limitations for the next implementation phase.
- Do not redesign the insurance module as part of this task.

Other restrictions:

- CSAT, NPS and VOC data remain unavailable.
- Workflow behaviour features are de-scoped.
- PensionerData-related features remain excluded.
- Respect existing business-approved feature exclusions.

8. Point-in-time correctness

- Restrict transactional and behavioural features to information available on or before as_of_date.
- Use verified source-specific event dates.
- Do not use future events, future account attributes or outcome information.
- Do not assume that fundJoinDate establishes historical validity for mutable attributes.
- Preserve NULL where historical attribute validity cannot be established.
- Keep feature engineering independent of target labels and temporal split assignments.
- Do not introduce ATO-related, ST000-related or migration-related target exclusions.

9. Implementation approach

First identify the exact files requiring changes.

Review the existing active modules covering:

- Contribution behaviour.
- Partial rollover and withdrawal behaviour.
- Investment behaviour.
- Helpline engagement.
- Campaign engagement.
- Web engagement.
- Third-party authority.
- Account profile features.
- Other currently approved active feature modules.

Modify only modules where historical coverage or NULL handling corrections are genuinely required.

Reuse shared utilities wherever possible to avoid duplicating historical coverage logic.

Preserve existing feature names, output schemas and approved calculation logic wherever possible.

If additional technical coverage metadata is required, keep it separate from the approved ML predictor list.

Avoid introducing unnecessary configuration constants or duplicate helper functions.

10. Validation

Create a consolidated read-only validation SQL file following existing repository naming conventions, preferably:

feature_historical_coverage_validation.sql

Include validation for:

- Full and partial historical coverage.
- Requested versus observable feature windows.
- Source-specific coverage limitations.
- Zero versus NULL handling.
- Accounts with shorter tenure.
- Feature-level NULL and zero distributions.
- Invalid ratios and division-by-zero conditions.
- Future event violations.
- AccountEngagementWeb NULL handling.
- Duplicate account_id and as_of_date combinations.
- Population reconciliation against the existing base population.

Provide a consolidated validation summary with PASS, FAIL, WARNING or NOT VALIDATED criteria.

Do not report a check as PASS without actual execution evidence.

11. Controlled manual execution

Provide notebook code and validation instructions for the following representative snapshots:

- 2023-04-30: Early historical snapshot.
- 2023-09-30: Partial historical coverage.
- 2024-03-31: Potentially complete 12-month historical coverage.

Recommend executing one snapshot at a time initially.

Use temporary validation views where appropriate.

Do not require permanent table creation for initial validation.

12. Performance requirements

- Use PySpark and Spark SQL consistent with existing architecture.
- Avoid collecting large datasets into driver memory.
- Avoid unnecessary Pandas conversions.
- Avoid repeated expensive source scans.
- Preserve scalability for approximately 32.6 million historical account snapshot records.
- Do not execute all 40 snapshots during this development step.

13. Strict restrictions

- Do not modify repository instruction files.
- Do not modify historical base population eligibility logic.
- Do not modify historical snapshot generation.
- Do not modify target label generation or ground-truth logic.
- Do not modify temporal splitting.
- Do not integrate the account profile module into consolidated features yet.
- Do not recreate workflow feature files.
- Do not execute Python scripts, SQL queries, notebooks or terminal commands.
- Do not launch background processes or Databricks jobs.
- Do not create, overwrite or delete Databricks tables.
- Do not proceed with EDA or model training.

14. Expected implementation summary

Provide a consolidated summary containing:

- Files reviewed.
- Files modified or created.
- Existing modules requiring no changes.
- Feature names affected.
- Previous NULL and zero handling.
- Corrected NULL and zero handling.
- Historical coverage logic.
- Source-specific limitations.
- Any output schema changes.
- Outstanding insurance historical validity limitations.
- Manual notebook execution code.
- Recommended validation sequence.

Perform a final static review against all repository instruction files and approved business feature definitions before completing the task.

Implement only the required historical coverage and NULL handling corrections. I will manually review and execute the generated code in Databricks.
