from ml_mscs_mrt_feature_validation import run_feature_validation

result_df = run_feature_validation(
    spark=spark,
    as_of_date="2024-03-31"
)

display(result_df)
