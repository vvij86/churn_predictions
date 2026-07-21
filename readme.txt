

The profiling supports using 100 as a reasonable POC threshold:

Keeps 441,280 accounts — 64.74% of partial-withdrawal accounts.

Keeps about 4.84 million transactions.

Retains approximately 98% of the total withdrawal amount compared with no threshold.

Removes many very small-value transactions without losing much monetary value.


So you can proceed with 100, but document it as a POC threshold pending business approval.

Use this Copilot prompt:

> Update the revised full churn dataset SQL using 100.00 as the configurable minimum significant partial-withdrawal amount.

Keep the existing raw partial-withdrawal features unchanged:

partial_withdrawal_count_12m

partial_withdrawal_amount_12m

days_since_last_partial_withdrawal_12m

partial_withdrawal_flag_12m


Add these threshold-based features using only individual partial-withdrawal transactions with an amount greater than or equal to 100.00:

significant_partial_withdrawal_count_12m

significant_partial_withdrawal_amount_12m

days_since_last_significant_partial_withdrawal_12m

significant_partial_withdrawal_flag_12m


Add this configurable parameter:

CAST(100.00 AS decimal(18,2)) AS min_partial_withdrawal_amount

Requirements:

1. Keep the existing cohort, feature window, outcome window, target logic and death exclusions unchanged.


2. Partial withdrawal must remain a feature only and must not directly create target_churn.


3. Use only transactions on or before as_of_date for these features.


4. Preserve exactly one row per ACCOUNT_ID.


5. Add comments stating that the 100.00 threshold is for the POC and requires business confirmation.


6. Return the complete revised dataset query.


7. Also return validation SQL for:

row count

distinct account count

duplicate account check

target distribution

counts of accounts with raw and significant partial withdrawals




Do not generate Python code yet.
