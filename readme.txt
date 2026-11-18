
view_name = "mer_wealth_dev.mer_wealth_landing_edge.mscs_mrt_account_summary"

print("Starting Databricks view access test")

df = spark.sql(f"SELECT * FROM {view_name} LIMIT 5")

df.show(truncate=False)

print("View access test completed successfully")

