from ml_mscs_mrt_target_labels import (
    run_target_label_pipeline,
)

from ml_mscs_mrt_config import (
    GROUND_TRUTH_TARGET_TABLE,
    TARGET_OUTCOME_HORIZON_MODE,
    TARGET_OUTCOME_HORIZON_VALUE,
)

assert GROUND_TRUTH_TARGET_TABLE.endswith(
    "_ground_truth_6m"
)

assert not spark.catalog.tableExists(
    GROUND_TRUTH_TARGET_TABLE
)

single_snapshot_df = run_target_label_pipeline(
    spark=spark,
    as_of_date="2024-03-31",
    outcome_horizon_days=90,
    outcome_horizon_mode=TARGET_OUTCOME_HORIZON_MODE,
    outcome_horizon_value=TARGET_OUTCOME_HORIZON_VALUE,
    persist_output=True,
    target_table_name=GROUND_TRUTH_TARGET_TABLE,
    feature_table_name=(
        "mer_wealth_dev.mer_wealth_mra_mlops."
        "member_retention_features"
    ),
)

print(
    "Table created:",
    spark.catalog.tableExists(GROUND_TRUTH_TARGET_TABLE)
)
