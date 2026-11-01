Run "consolidated_behavioural_feature_dataset_review.sql" for one sample "@AsOfDate" and validate the actual output.

Do not change the feature logic unless a clear execution issue is found.

Validate and report:

- query executes successfully
- total row count
- distinct "accountID" count
- duplicate "accountID + as_of_date" count
- confirm final grain is one row per "accountID + as_of_date"
- confirm no unexpected row multiplication
- confirm "current_account_fum_amount" is populated from the investment as-of logic
- check NULL counts for each feature group
- note that "edgeSource.accountEngagementWeb" is currently empty in UAT, so website features may be NULL/unavailable
- compare a small sample of accounts against the corresponding standalone feature queries and confirm values match
- identify any execution errors, unexpected NULLs, or mismatched feature values

Return a PASS / FAIL summary with exact issues found.

Do not start model training or target creation.
