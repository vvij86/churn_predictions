The current Phase 3 SQL is excluding accounts where accountSummary.reportingDate is NULL because reportingDate is being used directly as as_of_date.

Please correct the existing Phase 3 SQL.

Important requirements:

The modelling grain remains: one row per account_id per as_of_date

as_of_date must be an explicit modelling snapshot date/parameter and must not depend on reportingDate being non-null.

Build the base account universe from all valid accountID values.

Do NOT exclude an account solely because reportingDate is NULL.


Use an explicit parameter such as:

DECLARE @as_of_date DATE = '2025-12-31';

For accountSummary attributes:

If reportingDate is available, select the latest valid record on or before @as_of_date.

If multiple records exist for the same account, use ROW_NUMBER() or equivalent logic to select the latest valid snapshot.

Do not use records with reportingDate > @as_of_date.


For accounts where reportingDate is NULL:

retain the account in the account universe

do not automatically use the NULL-dated row as a historical snapshot

first check whether another reliable source/date column can establish when that record was valid

if no reliable temporal date exists, keep the account but set affected time-sensitive accountSummary features to NULL

flag those records/features for business/data validation

do not drop the account


Do not use a current/null-dated record for a historical as_of_date unless it is proven that the record was available at that time.

Keep memberNumber/member_id as a reference field only and do not use it as a predictive ML feature.

Do not change the account-level grain.

Update the existing build_account_level_features.sql rather than rebuilding the entire Phase 3 solution.

Also add validation SQL showing:

1. total distinct accounts in the source/base account universe


2. total accounts in the final feature dataset


3. accounts excluded from the final feature dataset


4. accounts with NULL reportingDate


5. accounts with no valid accountSummary snapshot on or before @as_of_date


6. duplicate account_id + as_of_date combinations


7. null account_id


8. null as_of_date



The final feature dataset should still contain:

account_id

related memberNumber/member_id

as_of_date

engineered account-level features


and must contain only one row per:

account_id + as_of_date

Do not add target_churn yet.
