from ml_mscs_mrt_historical_snapshots import (
    run_historical_snapshot_pipeline,
    EXECUTION_MODE_FEATURES_ONLY,
    HISTORICAL_START_DATE,
    HISTORICAL_END_DATE,
)

from ml_mscs_mrt_consolidated_features import (
    FEATURE_SNAPSHOT_TARGET_TABLE,
)

result = run_historical_snapshot_pipeline(
    spark=spark,
    start_date=HISTORICAL_START_DATE,
    end_date=HISTORICAL_END_DATE,
    execution_mode=EXECUTION_MODE_FEATURES_ONLY,
    feature_table_name=FEATURE_SNAPSHOT_TARGET_TABLE,
    stop_on_first_failure=True,
)

print(result["overall_status"])
print(result["successful_snapshot_count"])
print(result["failed_snapshot_count"])
