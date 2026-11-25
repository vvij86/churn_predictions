We are continuing the Member Retention Analytics ML feature engineering development in Databricks.

The account profile feature module has been implemented and successfully executed for the snapshot 2024-03-31, producing 785,885 records with zero duplicate keys. Historical attribute limitations remain documented.

Now implement the missing workflow behaviour feature module.

1. Repository instructions

Read and strictly follow all applicable repository instruction files, including copilot-instructions.md.

Review the existing configuration, base population, account profile features, other feature modules and behavioural_features_business_review.sql.

2. Implementation scope

Create two new files following the existing project structure and coding conventions:

- ml_mscs_mrt_workflow_features.py
- workflow_features_validation.sql

Implement only the workflow behaviour features specified in the reviewed business SQL.

Reuse the approved source tables, columns, event classifications, filters and feature definitions.

Do not invent additional features, source columns or business rules.

If any required source mapping is unavailable or ambiguous, report it explicitly.

3. Mandatory historical rules

- Never use reportingDate for historical filtering, snapshot selection or source ordering.
- Use fundJoinDate <= as_of_date for account joining eligibility.
- Reuse the existing historical base population logic without modification.
- Maintain exactly one row per account_id per as_of_date.
- Aggregate workflow events at account level before joining with the base population.
- Preserve all eligible base population records.

4. Point-in-time correctness

- Use verified workflow event dates to restrict feature calculations to information available on or before as_of_date.
- Never use future events or outcome information.
- Exclude exit-completion and other outcome-revealing events that could cause target leakage.
- Do not use current workflow status to reconstruct historical status unless historical validity is established.
- Reuse existing configuration constants for feature windows.
- Historical source start date is 2023-04-01.
- Feature lookback window is 12 months, wherever applicable.
- Recent and prior windows are 90 days each, wherever applicable.
- Support accounts with shorter tenure.

5. Missing data handling

Distinguish between:

- No workflow activity during a confirmed observable period.
- Insufficient historical coverage.
- Unavailable source data.

Use zero only when source coverage is confirmed and no qualifying activity exists.

Preserve NULL where historical information is unavailable.

AccountEngagementWeb still contains no data. Do not modify its existing NULL handling.

CSAT, NPS and VOC remain unavailable.

6. Business constraints

- Respect all existing business-approved feature exclusions.
- ATO-related churn clarification is pending business confirmation.
- Do not introduce ATO, ST000 or migration-related exclusions.
- Keep feature engineering independent of target labels and temporal split assignments.

7. Validation

Create a read-only SQL validation script covering:

- Base and output population counts.
- Distinct account snapshot keys.
- Duplicate records.
- Missing and extra accounts compared with base population.
- NULL key checks.
- Feature-level NULL distribution.
- Invalid or negative feature values.
- Future event violations.
- Outcome-related event leakage.
- Historical coverage limitations.
- Source-to-feature sample reconciliation.

Provide a consolidated validation summary with expected results and PASS, FAIL or WARNING criteria.

Do not claim point-in-time correctness where historical validity cannot be established.

8. Manual Databricks execution

Provide exact Python notebook code to execute the new module for:

as_of_date = 2024-03-31

Provide code to create a temporary validation view and instructions to run the validation SQL within the same Spark session.

No permanent table creation is required at this stage.

9. Strict restrictions

Create only the two requested files.

Do not modify existing configuration, base population, historical snapshots, ground truth, target labels, temporal splitting, account profile or consolidated feature modules.

Do not execute Python files, SQL queries, notebooks, terminal commands or Databricks jobs.

Do not create, overwrite or delete Databricks tables.

10. Expected summary

Provide:

- Files created.
- Number of features implemented.
- Feature names and descriptions.
- Source table and column mappings.
- Feature derivation logic.
- Point-in-time safeguards.
- Missing data handling.
- Historical limitations.
- Expected output schema.
- Manual execution instructions.
- Expected validation results.

Perform a final static review against repository instructions and reviewed business SQL.
