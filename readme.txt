Yes, but don’t choose an arbitrary amount yet.

A fixed threshold like amount >= 100 may ignore genuinely meaningful withdrawals for small-balance accounts. Better options are:

minimum transaction amount, confirmed by business;

percentage of account balance, such as withdrawal ≥ 5% or 10% of balance;

both amount and percentage together.


Since reliable historical balance is not currently available, for this POC use a business-approved minimum amount threshold only, and keep the raw amount/count features as well.

Ask Copilot with this prompt:

> Update the revised churn dataset SQL to add a configurable minimum partial-withdrawal amount threshold.

Add this parameter:

CAST(100.00 AS decimal(18,2)) AS min_partial_withdrawal_amount

Use it only for partial-withdrawal feature creation.

Requirements:

1. Keep the original raw features:

partial_withdrawal_count_12m

partial_withdrawal_amount_12m



2. Add threshold-based features using only individual partial-withdrawal transactions where the validated withdrawal amount is greater than or equal to min_partial_withdrawal_amount:

significant_partial_withdrawal_count_12m

significant_partial_withdrawal_amount_12m

days_since_last_significant_partial_withdrawal_12m

significant_partial_withdrawal_flag_12m



3. Do not remove small transactions from the raw dataset features.


4. Do not use partial withdrawal directly to create target_churn.


5. Keep one row per ACCOUNT_ID.


6. Add profiling showing, for thresholds 0, 50, 100, 500 and 1000:

qualifying transaction count

distinct account count

total withdrawal amount

percentage of partial-withdrawal accounts retained



7. Return the profiling query first. Do not change the full dataset query until the threshold distribution is reviewed.


