display(
    single_snapshot_df.select(
        "outcome_horizon_mode",
        "outcome_horizon_value",
        "outcome_horizon_key"
    ).distinct()
)




from pyspark.sql import functions as F

display(
    single_snapshot_df.agg(
        F.count("*").alias("total_rows"),
        F.countDistinct("account_id").alias(
            "distinct_accounts"
        ),
        F.count_if(
            F.col("account_id").isNull()
            | F.col("as_of_date").isNull()
        ).alias("null_keys")
    )
)
