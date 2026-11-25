from ml_mscs_mrt_consolidated_features import run_consolidated_feature_pipeline

consolidated_df = run_consolidated_feature_pipeline(
    spark=spark,
    as_of_date="2024-03-31",
    persist_output=False
)

print("Total rows:", consolidated_df.count())
print("Total columns:", len(consolidated_df.columns))

display(consolidated_df.limit(10))
