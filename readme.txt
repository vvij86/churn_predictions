We have completed target label generation and successfully reconciled the SQL Server and Databricks churn counts for the 2024-03-31 snapshot.

Completed validation results:

- Account full exits: 18,738
- Full rollover to external fund: 33
- Total churn accounts: 18,771
- Databricks churn count: 18,771
- Count difference: 0

Objective:

Perform the final multi-snapshot ground-truth sanity checks before proceeding with temporal splitting.

Review the existing files:

- "ml_mscs_mrt_target_labels.py"
- "mult_snap_sanity_check.sql"

Understand the existing implementation, business rules, eligibility criteria, outcome window and target label generation logic.

Databricks ground-truth table:

"mer_wealth_dev.mer_wealth_mra_mlops.member_retention_ground_truth"

Modelling grain:

The modelling grain must remain at account level, with exactly one row per accountID per as_of_date.

Required validations:

1. Overall dataset summary:
   
   - Total record count.
   - Number of snapshots.
   - Earliest and latest snapshot dates.

2. Snapshot-level distribution:
   
   - Total accounts.
   - Churn accounts.
   - Retained accounts.
   - Churn percentage.
   - Ineligible or incomplete-outcome accounts, if applicable.

3. Check for duplicate records at accountID and as_of_date level.

4. Check for NULL account IDs, NULL snapshot dates and invalid target_churn values.

5. Validate outcome window start dates, end dates and duration against the existing configuration.

6. Ensure qualifying churn event dates fall within their respective outcome windows.

7. Validate churn source distribution across all snapshots:
   
   - ACCOUNT_FULL_EXIT.
   - FULL_ROLLOVER_OUT.
   - Check for overlapping churn events and duplicate account counts.

8. Validate business rule exclusions:
   
   - Internal transfers.
   - Death-related exclusions.
   - Partial withdrawals and partial rollovers must not independently qualify as churn.
   - Eligible database codes.

9. Validate historical account eligibility as of each snapshot date.

10. Identify unusual churn rate spikes or drops across monthly snapshots. Report them as warnings requiring investigation rather than automatically treating them as errors.

11. Validate outcome window completeness, particularly for the latest snapshots, to ensure accounts with incomplete outcome windows are not incorrectly labelled as retained.

12. Check for potential point-in-time violations and temporal data leakage wherever relevant source timestamps are available. Clearly distinguish checks that must be performed later during feature engineering.

13. Reconfirm the 2024-03-31 snapshot churn count of 18,771 and perform account-level reconciliation where the required data is available.

Implementation requirements:

- Reuse existing sanity-check queries wherever possible.
- Update the existing "mult_snap_sanity_check.sql" file instead of creating redundant SQL files.
- Use Databricks-compatible SQL syntax.
- Use actual table names and column names from the existing implementation.
- Do not assume or invent unavailable columns.
- Preserve the existing approved business rules.
- Keep each validation query separate, clearly numbered and commented.
- Ensure each validation query can be executed independently.
- Avoid unnecessary repeated scans of large historical datasets wherever possible.
- Provide a consolidated validation summary query with the following columns:
  - check_id
  - check_name
  - expected_result
  - actual_result
  - validation_status
  - remarks
- Use PASS, FAIL, WARNING or NOT VALIDATED as validation statuses.
- Do not mark a check as PASS unless it is supported by actual execution results.
- Clearly distinguish mandatory validation failures from informational warnings.

Strict execution restrictions:

- Do not execute any Python files.
- Do not execute any SQL scripts.
- Do not execute notebooks.
- Do not execute terminal commands.
- Do not launch any background execution or processes.
- Do not trigger Databricks jobs or workflows.
- Do not start or restart Databricks compute.
- Do not create, overwrite, update, truncate or delete any Databricks tables.
- Do not modify "ml_mscs_mrt_target_labels.py".
- Do not modify any other Python files or existing production logic.
- Do not proceed with temporal splitting, feature engineering or model training.

Only review the existing implementation and update "mult_snap_sanity_check.sql" with the required read-only validation queries.

After completing the changes, provide a short summary of:

- Existing validations retained.
- New validations added.
- Any limitations or unavailable columns.
- Recommended SQL execution order.

I will manually review and execute the generated SQL queries in Databricks and share the validation results.

The objective is to confirm that the historical ground-truth dataset is ready for the next ML development phase without modifying the existing data or business logic.
