All diagnostic CTEs return zero duplicates. The current account base contains 794,328 unique accounts and 338 death exclusions, producing 793,990 trainable rows.
My previously validated dataset contained 793,915 trainable rows, so there is a difference of 75 accounts.
Compare the current modelling query against the original validated dataset query and identify exactly which cohort, date, death-exclusion, or target filter changed.
Create a diagnostic query that returns the 75 account IDs included in the current query but excluded from the original validated query, along with:
ACCOUNT_ID
COMMENCE_DATE
EXIT_DATE
STATUS_CODE
death outcome flag
external rollover outcome flag
target_churn
exclude_from_training_flag
a text column explaining why each account differs
Do not modify the modelling query yet. Return only the comparison diagnostic SQL.
