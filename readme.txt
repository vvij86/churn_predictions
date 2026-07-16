This is a technical POC to compare machine-learning models using currently available SonataODS data. BA confirmation is happening separately and must not block the POC.
Use the revised Version 1 column specification already produced.
Apply the following provisional POC target rules:
Exclude death-related outcome records where EXIT_TYPE.IS_DEATH_FLAG = 'Y'.
Define account closure provisionally as either:
ACCOUNT.EXIT_DATE falling within the outcome window, or
ACCOUNT.STATUS_CODE = 'CLOS'.
Define external rollover as:
EXIT_TYPE.IS_ROLLOVER_FLAG = 'Y'
COALESCE(EXIT_TYPE.IS_INTERNAL_FLAG, 'N') <> 'Y'
COALESCE(EXIT_TYPE.IS_DEATH_FLAG, 'N') <> 'Y'.
Set target_churn = 1 when the account is closed in the outcome window, regardless of whether an external rollover is present.
Set target_churn = 0 when the account remains active/not closed.
Keep external rollover fields as target-supporting audit fields only; do not use them as ML features.
Do not distinguish partial and full rollover.
Use:
feature window: 2024-01-01 to 2024-12-31
as_of_date: 2024-12-31
outcome window: 2025-01-01 to 2025-03-31
Exclude all FUM/balance features.
Exclude date_status_changed_recency_days from Version 1 unless point-in-time validity can be guaranteed.
Clearly mark all target rules as POC assumptions pending BA confirmation.
Now generate:
One complete read-only SQL query producing one row per account_id for the specified as_of_date.
Separate feature, target-supporting, exclusion and target sections using CTEs.
Strict date filters preventing post-as_of_date information from entering ML features.
A final output containing the ML features, audit fields, exclusion flag and target_churn.
Basic validation queries for row count, churn distribution, duplicate account_id, null percentages and death-exclusion count.
