from ml_mscs_mrt_config import (
    GROUND_TRUTH_TARGET_TABLE,
    TARGET_OUTCOME_HORIZON_MODE,
    TARGET_OUTCOME_HORIZON_VALUE,
)

print("Ground Truth table:", GROUND_TRUTH_TARGET_TABLE)
print("Horizon mode:", TARGET_OUTCOME_HORIZON_MODE)
print("Horizon value:", TARGET_OUTCOME_HORIZON_VALUE)

print(
    "Table already exists:",
    spark.catalog.tableExists(GROUND_TRUTH_TARGET_TABLE)
)
