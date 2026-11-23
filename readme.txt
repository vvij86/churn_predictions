from pyspark.sql import SparkSession

spark = SparkSession.builder.getOrCreate()

CATALOG = "mer_wealth_dev"
SCHEMA = "mer_wealth_mra_mlops"
TEST_TABLE = f"{CATALOG}.{SCHEMA}._member_retention_write_preflight"

print("Starting Delta write preflight...")

try:
    spark.sql(f"USE CATALOG {CATALOG}")
    spark.sql(f"USE SCHEMA {SCHEMA}")

    # Clean up any old test table first
    spark.sql(f"DROP TABLE IF EXISTS {TEST_TABLE}")

    # Actual Delta create/write test
    spark.sql(f"""
        CREATE TABLE {TEST_TABLE}
        USING DELTA
        AS
        SELECT
            1 AS test_id,
            current_timestamp() AS created_at
    """)

    # Read test
    result = spark.sql(f"SELECT COUNT(*) AS row_count FROM {TEST_TABLE}").collect()[0]["row_count"]
    print(f"Write/read test passed. Row count: {result}")

    # Cleanup
    spark.sql(f"DROP TABLE {TEST_TABLE}")

    print("DELTA WRITE PREFLIGHT: PASS")

except Exception as e:
    print("DELTA WRITE PREFLIGHT: FAIL")
    print(str(e))
    raise
