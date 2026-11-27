from ml_mscs_mrt_target_labels import run_target_label_pipeline
from ml_mscs_mrt_config import (
    GROUND_TRUTH_TARGET_TABLE,
    TARGET_OUTCOME_HORIZON_DAYS,
    TARGET_OUTCOME_HORIZON_MODE,
    TARGET_OUTCOME_HORIZON_VALUE,
    EXCLUDE_PAYMENT_TO_ATO
)
from pyspark.sql import functions as F

# Verify configuration
assert EXCLUDE_PAYMENT_TO_ATO is True
assert TARGET_OUTCOME_HORIZON_MODE == "calendar_months"
assert TARGET_OUTCOME_HORIZON_VALUE == 6

snapshot_dates = [
    "2024-03-31",
    "2025-03-31",
    "2026-03-31"
]

results = []

for snapshot_date in snapshot_dates:

    print(f"Validating snapshot: {snapshot_date}")

    df = run_target_label_pipeline(
        spark=spark,
        as_of_date=snapshot_date,
        outcome_horizon_days=TARGET_OUTCOME_HORIZON_DAYS,
        outcome_horizon_mode=TARGET_OUTCOME_HORIZON_MODE,
        outcome_horizon_value=TARGET_OUTCOME_HORIZON_VALUE,
        persist_output=False,
        target_table_name=GROUND_TRUTH_TARGET_TABLE,
        feature_table_name=(
            "mer_wealth_dev.mer_wealth_mra_mlops."
            "member_retention_features"
        )
    )

    stats = df.agg(
        F.count("*").alias("total_accounts"),
        F.countDistinct(
            "account_id", "as_of_date"
        ).alias("distinct_accounts"),
        F.sum(
            F.when(F.col("target_churn") == 1, 1)
            .otherwise(0)
        ).alias("churn_accounts"),
        F.sum(
            F.when(F.col("target_churn") == 0, 1)
            .otherwise(0)
        ).alias("non_churn_accounts"),
        F.sum(
            F.when(F.col("target_churn").isNull(), 1)
            .otherwise(0)
        ).alias("null_targets")
    ).first()

    total = stats["total_accounts"]
    churn = stats["churn_accounts"] or 0
    non_churn = stats["non_churn_accounts"] or 0
    nulls = stats["null_targets"] or 0
    duplicates = total - stats["distinct_accounts"]

    churn_pct = round(
        churn * 100 / total, 4
    ) if total else 0.0

    status = "PASS" if (
        total > 0
        and duplicates == 0
        and nulls == 0
        and total == churn + non_churn
    ) else "FAIL"

    results.append((
        snapshot_date,
        total,
        churn,
        non_churn,
        nulls,
        duplicates,
        churn_pct,
        status
    ))

display(spark.createDataFrame(
    results,
    [
        "as_of_date",
        "total_accounts",
        "churn_accounts",
        "non_churn_accounts",
        "null_targets",
        "duplicate_count",
        "churn_percentage",
        "validation_status"
    ]
))
