from pyspark.sql import SparkSession

spark = SparkSession.builder.getOrCreate()

CATALOG = "mer_wealth_dev"
SCHEMA = "mer_wealth_mra_mlops"
TEST_TABLE = f"{CATALOG}.{SCHEMA}._ml_delta_write_test"

print("Starting ML cluster Delta write preflight...")

try:
    # Set catalog/schema
    spark.sql(f"USE CATALOG {CATALOG}")
    spark.sql(f"USE SCHEMA {SCHEMA}")

    # Cleanup old test table if any
    spark.sql(f"DROP TABLE IF EXISTS {TEST_TABLE}")

    # Actual Delta create/write
    spark.sql(f"""
        CREATE TABLE {TEST_TABLE}
        USING DELTA
        AS
        SELECT
            1 AS test_id,
            current_timestamp() AS created_at
    """)

    # Read-back validation
    result = spark.sql(
        f"SELECT COUNT(*) AS row_count FROM {TEST_TABLE}"
    ).collect()[0]

    print(f"Read-back row count: {result['row_count']}")

    # Cleanup
    spark.sql(f"DROP TABLE {TEST_TABLE}")

    print("ML CLUSTER DELTA WRITE PREFLIGHT: PASS")

except Exception as e:
    print("ML CLUSTER DELTA WRITE PREFLIGHT: FAIL")
    print(type(e).__name__)
    print(str(e))
    raise
