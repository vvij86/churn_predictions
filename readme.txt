Follow ".github/copilot-instructions.md".

Implement the necessary corrections identified in the Step 2 historical consolidated feature dataset review.

Requirements:

1. Move the existing historical end date (2026-07-31) into the shared configuration file. Preserve the existing historical start date and monthly snapshot frequency.

2. Introduce a configurable feature-only execution option in "ml_mscs_mrt_historical_snapshots.py" so that historical consolidated features can be generated and persisted independently of target labels.

3. When feature-only execution is selected:
   
   - Do not execute the target label pipeline.
   - Do not execute target-specific historical validation.
   - Do not generate temporal splits.
   - Perform consolidated feature validation and persistence only.

4. Preserve the existing consolidated feature pipeline containing all nine feature modules.

5. Ensure each snapshot passes validation before persistence.

6. Preserve Delta MERGE behavior using account_id + as_of_date. Verify that rerunning a snapshot cannot leave stale account keys, duplicate records or modify unrelated snapshots. Apply a minimal snapshot-scoped correction only if required.

7. Preserve stop-on-first-failure behavior and allow safe resumption from a failed snapshot. Previously completed valid snapshots should remain intact.

8. Ensure repeated monthly execution does not introduce cache accumulation or CACHE_DATAFRAME_ACCESS_AFTER_UNCACHE errors.

9. Preserve all existing feature calculations, historical coverage assumptions, NULL/zero handling, runtime leakage safeguards and newly joined account eligibility.

10. Preserve the existing target table name:
    mer_wealth_dev.mer_wealth_mra_mlops.member_retention_features

11. Provide concise per-snapshot execution logs including snapshot date, base count, persisted row count, validation status and execution duration.

12. Preserve the existing target-label execution functionality for future use without changing its business rules.

Restrictions:

- Modify only the historical snapshots and configuration files wherever possible.
- Modify the consolidated feature file only if strictly necessary for safe persistence or cache lifecycle management.
- Do not modify individual feature modules.
- Do not create new files or notebooks.
- Do not introduce unnecessary architectural changes.
- Do not execute scripts, SQL, notebooks, jobs or terminal commands.
- Do not write or overwrite Databricks tables.
- Do not proceed with model training or MLflow.

Finally, provide:

- Modified files and concise change summary.
- Exact Databricks Python execution code for feature-only persistence of one snapshot (2024-03-31).
- Execution code for the complete historical monthly range.
- Execution code for resuming from a failed snapshot.
- Read-only SQL to validate persisted snapshot counts and duplicate keys.
