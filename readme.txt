spark.sql("""
CREATE TABLE IF NOT EXISTS mer_wealth_dev.mer_wealth_mra_mlops._ml_write_access_test
USING DELTA
AS SELECT 1 AS test_value
""")

spark.sql("""
SELECT * 
FROM mer_wealth_dev.mer_wealth_mra_mlops._ml_write_access_test
""").show()

spark.sql("""
DROP TABLE mer_wealth_dev.mer_wealth_mra_mlops._ml_write_access_test
""")
