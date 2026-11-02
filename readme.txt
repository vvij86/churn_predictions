Investigate why "current_account_fum_amount" is NULL for 90,929 eligible accounts in "consolidated_behavioural_feature_dataset_review.sql".

Do not modify the feature logic yet.

Classify the NULL FUM accounts into clear reason groups:

- no "edgeSource.accountInvestments" record exists for the account
- investment records exist, but only after "@AsOfDate"
- investment records exist on/before "@AsOfDate" but are excluded by the current as-of logic
- join/mapping mismatch
- any other identifiable reason

For each reason group, provide:

- account count
- percentage of the 90,929 NULL-FUM accounts
- a few sample "accountID"s

Also confirm whether any of these NULLs are genuine zero-balance accounts.

Do not replace NULL with 0 and do not change the SQL. This is investigation only.

Return a short summary with the main cause and whether the current FUM logic needs correction or the NULLs are expected from source data availability.
