from ml_mscs_mrt_config import (
    TARGET_OUTCOME_HORIZON_MODE,
    TARGET_OUTCOME_HORIZON_VALUE,
    TARGET_OUTCOME_HORIZON_DAYS,
    GROUND_TRUTH_TARGET_TABLE,
)

print("Horizon mode:", TARGET_OUTCOME_HORIZON_MODE)
print("Horizon value:", TARGET_OUTCOME_HORIZON_VALUE)
print("Legacy horizon days:", TARGET_OUTCOME_HORIZON_DAYS)
print("Ground Truth table:", GROUND_TRUTH_TARGET_TABLE)



from ml_mscs_mrt_target_labels import (
    run_target_label_pipeline,
)

single_snapshot_df = run_target_label_pipeline(
    spark=spark,
    as_of_date="2024-03-31",
    outcome_horizon_days=90,
    outcome_horizon_mode="calendar_months",
    outcome_horizon_value=6,
    persist_output=False,
    target_table_name=GROUND_TRUTH_TARGET_TABLE,
    feature_table_name=(
        "mer_wealth_dev.mer_wealth_mra_mlops."
        "member_retention_features"
    ),
)

display(
    single_snapshot_df.groupBy("target_churn").count()
)
