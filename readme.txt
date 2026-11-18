view_name = "mer_wealth_dev.mer_wealth_landing_edge.mscs_mrt_account_summary"

df = spark.sql(f"SELECT * FROM {view_name} LIMIT 5")
display(df)
