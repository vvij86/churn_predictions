from pyspark.sql import SparkSession
from pyspark.sql import functions as F

# Get current Spark session
spark = SparkSession.builder.getOrCreate()

CATALOG = "mer_wealth_dev"
SCHEMA = "mer_wealth_mra_mlops"

print("Checking current catalog/schema access...")

# 1. Show current user
try:
    current_user = spark.sql("SELECT current_user() AS current_user").collect()[0]["current_user"]
    print(f"Current user: {current_user}")
except Exception as e:
    print(f"Unable to get current user: {e}")

# 2. Check catalog visibility
try:
    spark.sql(f"USE CATALOG {CATALOG}")
    print(f"USE CATALOG passed: {CATALOG}")
except Exception as e:
    print(f"USE CATALOG failed: {e}")

# 3. Check schema visibility
try:
    spark.sql(f"USE SCHEMA {CATALOG}.{SCHEMA}")
    print(f"USE SCHEMA passed: {CATALOG}.{SCHEMA}")
except Exception as e:
    print(f"USE SCHEMA failed: {e}")

# 4. Show grants on schema
try:
    print("\nSchema grants:")
    grants_df = spark.sql(
        f"SHOW GRANTS ON SCHEMA {CATALOG}.{SCHEMA}"
    )
    grants_df.show(truncate=False)
except Exception as e:
    print(f"SHOW GRANTS failed: {e}")

# 5. List existing tables
try:
    print("\nExisting tables:")
    spark.sql(
        f"SHOW TABLES IN {CATALOG}.{SCHEMA}"
    ).show(truncate=False)
except Exception as e:
    print(f"SHOW TABLES failed: {e}")
