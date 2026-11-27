Based on your previous prediction window configuration review, implement the minimum necessary changes to support configurable churn prediction horizons for the Member Retention Analytics project.

Reuse your previous analysis and findings. Do not repeat the entire repository analysis.

Files in scope:

- ml_mscs_mrt_config.py
- ml_mscs_mrt_target_labels.py
- ml_mscs_mrt_historical_snapshots.py
- ml_mscs_mrt_temporal_split.py
- sqlserver_target_churn_validation_2024_03_31.sql
- mult_snap_sanity_check.sql
- temporal_split_validation.sql (only if required)

Modify only the files that genuinely require changes. If any additional file requires modification, report it separately with justification before modifying it.

Implementation requirements:

1. Support both the existing day-based prediction horizon and calendar-month-based prediction horizons through central configuration.

2. Support the following configurations:
   
   - 90 days (existing default)
   - 180 days
   - 3 calendar months
   - 6 calendar months

3. Preserve the existing 90-day default until business confirmation.

4. Ensure Ground Truth generation, outcome date calculations, temporal split metadata and purge boundary logic consistently respect the configured prediction horizon.

5. Calculate the outcome start date as as_of_date + 1 day.

6. For calendar-month horizons, calculate the outcome end date as the last day of the corresponding future month for month-end snapshots.
   
   Example for as_of_date = 2024-03-31:
   
   - 90 days: 2024-06-29
   - 180 days: 2024-09-27
   - 3 calendar months: 2024-06-30
   - 6 calendar months: 2024-09-30

7. Ensure historical target generation dynamically checks complete future outcome availability against the verified source coverage end date. Do not assume source coverage based solely on the latest transaction date. If verified coverage is unavailable, require an explicit coverage cutoff before generating final labels.

8. Incomplete future outcome windows must not be incorrectly labelled as non-churn. Exclude incomplete snapshots from supervised modelling datasets.

9. Keep the historical feature snapshot end date independent of the latest eligible Ground Truth snapshot date.

10. Parameterise all relevant hardcoded 90-day conditions in the existing target validation SQL files. Ensure SQL and Python outcome date calculations remain consistent.

11. Ensure temporal split boundaries prevent overlapping outcome windows across training, validation and test datasets. For calendar-month horizons, use actual calculated outcome end dates rather than approximate fixed-day purge windows.

12. Ensure Ground Truth prediction horizon metadata is traceable. Prevent accidental mixing of target labels generated using different prediction horizons, including when rerunning the same snapshot.

13. Preserve the modelling grain of one row per account_id and as_of_date within each horizon-specific dataset.

14. Preserve existing function signatures and backward compatibility wherever possible.

Restrictions:

- Do not modify ATO exclusion logic at this stage.
- Do not modify Other payment type logic.
- Do not modify existing churn classification or account eligibility rules.
- Do not modify individual feature modules.
- Do not modify consolidated feature engineering logic.
- Do not regenerate the existing 40 historical feature snapshots containing 32,616,602 records.
- Do not modify the historical feature table.
- Do not create unnecessary files or notebooks.
- Do not introduce unnecessary architectural changes.
- Do not execute scripts, SQL, notebooks, jobs or terminal commands.
- Do not write, overwrite or delete any Databricks table data.
- Do not proceed with model training, scoring or MLflow.

Finally, provide:

1. List of modified files with a concise change summary.
2. Exact configuration examples for 90 days, 180 days, 3 calendar months and 6 calendar months.
3. Explanation of incomplete outcome window handling.
4. Explanation of temporal leakage prevention.
5. Explanation of how different prediction horizons are kept separate.
6. Exact Databricks Python execution code for validating a single Ground Truth snapshot without persistence, if supported.
7. Recommended read-only validation SQL queries.
8. Any remaining risks or dependencies.

Keep the implementation focused, minimal and reusable.
