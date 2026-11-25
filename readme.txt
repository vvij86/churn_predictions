from ml_mscs_mrt_account_profile_features import (
    run_account_profile_feature_pipeline
)

account_profile_df = run_account_profile_feature_pipeline(
    spark=spark,
    as_of_date="2024-03-31"
)

display(account_profile_df.limit(20))
