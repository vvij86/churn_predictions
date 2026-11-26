Historical_Feature_Dataset_Generation


from ml_mscs_mrt_historical_snapshots import (
    run_historical_snapshot_pipeline,
    EXECUTION_MODE_FEATURES_ONLY,
)

from ml_mscs_mrt_consolidated_features import (
    FEATURE_SNAPSHOT_TARGET_TABLE,
)

result = run_historical_snapshot_pipeline(
    spark=spark,
    start_date="2024-03-31",
    end_date="2024-03-31",
    execution_mode=EXECUTION_MODE_FEATURES_ONLY,
    feature_table_name=FEATURE_SNAPSHOT_TARGET_TABLE,
    stop_on_first_failure=True,
)

print(result["overall_status"])
print(result["snapshot_results"])
