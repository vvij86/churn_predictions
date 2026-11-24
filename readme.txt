We have executed "mult_snap_sanity_check.sql" in Databricks and obtained the following results:

Dataset summary:

- Total records: 32,616,602
- Total snapshots: 40
- First snapshot: 2023-04-30
- Last snapshot: 2026-07-31
- Total churn records: 355,441
- Total retained records: 32,261,161
- Duplicate records: 0
- NULL account IDs: 0
- NULL snapshot dates: 0
- NULL or invalid target labels: 0
- Configured outcome horizon: 90 days
- Maximum available event date: 2026-10-16
- Incomplete outcome window records: 833,849
- March 2024 churn count: 18,771 (successfully reconciled with SQL Server).

Objective:

Complete the remaining ground-truth validations and investigate incomplete outcome windows before proceeding with temporal splitting.

Review the existing "mult_snap_sanity_check.sql" and "ml_mscs_mrt_target_labels.py" files.

Focus only on the following checks:

1. Check 06 – Churn event window

- Identify churn events outside their respective outcome windows.
- Return the actual violation count.

2. Check 07 – Churn source distribution

- Provide account-level counts for ACCOUNT_FULL_EXIT and FULL_ROLLOVER_OUT.
- Identify overlapping churn events.
- Confirm that overlapping events do not cause duplicate target records.

3. Check 08a–08d – Business rule exclusions

- Validate internal transfer exclusions.
- Validate death-related exclusions.
- Ensure partial withdrawals and partial rollovers do not independently qualify as churn.
- Validate eligible database codes.

4. Check 09 – Historical account eligibility

- Confirm that accounts were eligible as of their respective snapshot dates.
- Return the actual violation count.

5. Check 11 – Outcome window completeness

- Identify all snapshots with incomplete outcome windows.
- Display as_of_date, outcome_end_date, source coverage date, missing outcome days, total records, churn records and retained records.
- Validate data coverage separately for AccountSummary and AccountRolloverPayment.
- Do not assume that the maximum observed event date guarantees complete source data coverage.
- Identify the latest fully observable snapshot based on confirmed source coverage.
- Calculate the number of complete snapshots and records available for future temporal splitting.
- Recommend excluding incomplete snapshots from supervised training, validation and testing without deleting them from the existing ground-truth table.

6. Check 12a – Target-level temporal validation

- Validate target-level point-in-time rules.
- Identify any violations.
- Defer feature-level data leakage checks to the feature engineering phase.

Implementation requirements:

- Update the existing "mult_snap_sanity_check.sql" file.
- Retain previously completed validation queries.
- Use actual table and column names from the existing implementation.
- Maintain account-level grain: one row per accountID per as_of_date.
- Use read-only Databricks-compatible SQL.
- Provide a consolidated summary containing actual violation counts rather than references such as "See Check 08 output".
- Return PASS, FAIL, WARNING or NOT VALIDATED for each check.
- Do not mark unavailable or unverified checks as PASS.
- Do not change existing business rules.

Strict restrictions:

- Do not execute any SQL, Python, notebooks or terminal commands.
- Do not run any background processes.
- Do not trigger Databricks jobs or compute.
- Do not modify any Python files, including "ml_mscs_mrt_target_labels.py".
- Do not create, overwrite, update or delete any Databricks tables.
- Do not implement temporal splitting or feature engineering yet.

Only update the existing sanity-check SQL file.

I will manually execute the SQL in Databricks and review the results before proceeding to the next phase.
