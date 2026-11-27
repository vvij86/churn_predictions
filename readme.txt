print(GROUND_TRUTH_TARGET_TABLE)

spark.table(
    GROUND_TRUTH_TARGET_TABLE
).printSchema()
