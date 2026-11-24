We have successfully completed historical snapshot generation, target label generation and ground-truth sanity checks for the Member Retention Analytics ML project.

Completed validation summary:

- Total records: 32,616,602
- Total monthly snapshots: 40
- First snapshot: 2023-04-30
- Last snapshot: 2026-07-31
- Total churn records: 355,441
- Total retained records: 32,261,161
- Duplicate account snapshot records: 0
- Invalid or NULL target labels: 0
- Historical eligibility violations: 0
- Target-level temporal violations: 0
- Partial-only positive violations: 0
- March 2024 churn reconciliation: 18,771
- Account-level reconciliation mismatches: 0
- Sanity-check results: 11 PASS, 2 WARNING, 0 FAIL.

Known limitations:

- Reported source coverage date: 2026-10-16.
- Incomplete outcome window records: 833,849.
- The July 2026 snapshot has an incomplete 90-day outcome window.
- Source completeness must be confirmed independently of the maximum observed event date.
- Feature-level data leakage checks will be performed during feature engineering.

Objective:

Implement chronological temporal splitting for supervised ML model development using the existing ground-truth dataset.

Source table:

"mer_wealth_dev.mer_wealth_mra_mlops.member_retention_ground_truth"

Modelling grain:

Exactly one row per account_id per as_of_date.

Step 1 – Review existing implementation

Review the existing project structure, configuration files, naming conventions and the following files:

- "ml_mscs_mrt_historical_snapshots.py"
- "ml_mscs_mrt_target_labels.py"
- "mult_snap_sanity_check.sql"

Reuse existing utilities and configuration wherever applicable.

Step 2 – Determine eligible snapshots

- Use the configured 90-day outcome horizon.
- Include only snapshots with fully observable outcome windows.
- Validate outcome completeness against verified source coverage.
- Exclude incomplete snapshots from training, validation and testing.
- Preserve incomplete records in the original ground-truth table.
- Do not hardcode July 2026 as the only excluded snapshot.
- Make source coverage configurable.

Step 3 – Temporal splitting

- Split eligible snapshots chronologically into TRAIN, VALIDATION and TEST datasets.
- Prefer approximately 70%, 15% and 15% of usable snapshots, subject to outcome-window leakage protection.
- Do not use random splitting.
- Keep all records belonging to the same snapshot in the same split.
- Introduce the necessary purge or embargo periods between splits.
- Ensure the last training outcome window ends before the first validation snapshot.
- Ensure the last validation outcome window ends before the first test snapshot.
- Make split boundaries configurable and reproducible.
- Preserve naturally occurring churn distributions.
- Do not perform oversampling, undersampling or SMOTE at this stage.
- Keep the test dataset untouched for final model evaluation.

Step 4 – Implementation

- Follow existing project naming and coding conventions.
- Create a dedicated temporal splitting Python module, preferably "ml_mscs_mrt_temporal_split.py", if an equivalent module does not already exist.
- Use PySpark and Databricks-compatible APIs.
- Avoid converting large datasets into Pandas DataFrames or collecting account-level records into driver memory.
- Add a configurable dry-run mode that reports proposed split boundaries and statistics without writing data.
- Design the output as a persistent Delta table, not a view.
- Prefer a lightweight split assignment table keyed by account_id and as_of_date, rather than unnecessarily duplicating the entire ground-truth dataset.
- Include split_type, exclusion_reason and relevant outcome-window metadata.
- Explicitly distinguish incomplete-outcome and purge-period records from TRAIN, VALIDATION and TEST records.
- Make future execution idempotent.

Step 5 – Validation requirements

Provide validation queries or checks for:

1. Total eligible and excluded snapshots.
2. Total eligible and excluded records.
3. Snapshot date ranges for each split.
4. Record counts per split.
5. Distinct account counts per split.
6. Churn and retained counts per split.
7. Churn percentage per split.
8. Duplicate account_id and as_of_date records.
9. Overlapping snapshot dates between splits.
10. Outcome-window leakage between splits.
11. Incomplete outcome records included in supervised splits.
12. Total record reconciliation, including excluded records.

The same account may appear in different chronological snapshots and splits. This is acceptable for the intended temporal evaluation. However, no account_id and as_of_date combination should be assigned to multiple splits.

Step 6 – Deliverables

Provide:

- Proposed temporal split date ranges.
- New or modified file names.
- Recommended persistent output table name and schema.
- Explanation of the purge or embargo strategy.
- Configuration parameters.
- Manual execution instructions.
- Expected validation results.

Clearly distinguish proposed results from actual execution results.

Strict restrictions:

- Do not execute any Python files, SQL scripts, notebooks or terminal commands.
- Do not run background processes.
- Do not trigger Databricks jobs or workflows.
- Do not start or restart Databricks compute.
- Do not create, overwrite, update or delete any Databricks tables during this task.
- Do not modify the existing historical snapshot or target label generation logic.
- Do not proceed with feature engineering, EDA or model training.

Only implement the temporal splitting code and required validation logic.

I will manually review and execute the implementation in Databricks after reviewing the proposed split strategy.
