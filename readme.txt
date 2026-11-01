Validate "consolidated_behavioural_feature_dataset_review.sql" against "behavioural_features_business_review.sql".

Do not modify either file during this validation.

Check and report:

- final grain is exactly one row per "accountID + @AsOfDate"
- every consolidated feature exists in the validated standalone SQL
- no approved feature is missing
- no duplicate or unintended feature columns are added
- each feature block returns at most one row per "accountID" before joining
- no join can multiply account rows
- all source-date filters are point-in-time safe ("<= @AsOfDate")
- no post-AsOfDate or outcome-window data is used
- no "target_churn", exit outcome, or leakage field is used as a predictive feature
- internal-transfer and full/external-rollover exclusions are preserved
- website NULL handling is preserved
- "current_account_fum_amount" is derived from the validated "accountInvestments" as-of logic
- "total_investment_value_asof" is not duplicated if it represents the same FUM calculation
- final output contains "accountID", member reference/ID, "as_of_date", and all retained feature columns

Also provide:

1. total final feature count
2. feature count by group
3. any missing features
4. any extra features
5. any duplicate-risk joins
6. any point-in-time or leakage issues
7. PASS / FAIL summary with exact issues if any

Do not change the SQL. This is validation only.
