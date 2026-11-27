existing_columns = spark.table(
    GROUND_TRUTH_TARGET_TABLE
).columns

required_columns = [
    "outcome_horizon_mode",
    "outcome_horizon_value",
    "outcome_horizon_days",
    "outcome_horizon_months",
    "outcome_horizon_key"
]

for col in required_columns:
    print(
        col, ":",
        "EXISTS" if col in existing_columns
        else "MISSING"
    )
