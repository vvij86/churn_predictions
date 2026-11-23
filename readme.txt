from pyspark.sql import SparkSession

spark = SparkSession.builder.getOrCreate()

CATALOG = "mer_wealth_dev"
SCHEMA = "mer_wealth_mra_mlops"
TEST_TABLE = f"{CATALOG}.{SCHEMA}._serverless_delta_write_test"

spark.sql(f"USE CATALOG {CATALOG}")
spark.sql(f"USE SCHEMA {SCHEMA}")

spark.sql(f"DROP TABLE IF EXISTS {TEST_TABLE}")

spark.sql(f"""
CREATE TABLE {TEST_TABLE}
USING DELTA
AS
SELECT
    1 AS test_id,
    current_timestamp() AS created_at
""")

spark.sql(f"SELECT * FROM {TEST_TABLE}").show()

spark.sql(f"DROP TABLE {TEST_TABLE}")

print("SERVERLESS DELTA WRITE TEST: PASS")
