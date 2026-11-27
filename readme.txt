Review only the following existing files:

- ml_mscs_mrt_config.py
- ml_mscs_mrt_temporal_split.py
- ml_mscs_mrt_historical_snapshots.py
- ml_mscs_mrt_target_labels.py

Our prediction horizon is now 6 calendar months. Historical feature generation is completed for all 40 monthly snapshots.

Verify the following:

1. Is the configured 90-day temporal purge applied as an additional gap after the actual six-month outcome end date? If so, can we set it to 0 while preserving strict outcome-window leakage prevention?
2. Does the temporal split pipeline use the newly configured member_retention_ground_truth_6m and member_retention_temporal_split_assignment_6m tables?
3. Can we generate all eligible Ground Truth snapshots independently using the existing persisted feature table without regenerating features?
4. Provide exact Databricks Python execution code for historical target-only generation and temporal split dry-run validation.
5. Confirm whether the persisted Ground Truth dataset already contains the modelling features and target label, or whether a separate modelling dataset preparation step is required.

Keep the response concise. Do not modify files, execute code, create files or write to any tables. Do not perform a full repository review.
