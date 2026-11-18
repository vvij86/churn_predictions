
from databricks.connect import DatabricksSession

spark = DatabricksSession.builder.serverless().getOrCreate()

print("Connected to Databricks Serverless!")

df = spark.range(5)
df.show()

print("Serverless test successful!")

