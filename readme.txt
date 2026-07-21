Update the existing churn dataset SQL query to incorporate the business-provided Sonata partial withdrawal logic.
Business logic:
CASE
    WHEN trev.event_type_code IN ('ETC','ETCV','FLCL','PFCO') THEN 0
    ELSE 1
END AS partial_withdrawal_flag
Source table:
sonatadm.sonata.transaction_event trev
Requirements:
Keep the existing cohort, feature-window, outcome-window, death-exclusion and target logic unchanged unless explicitly stated below.
Join transaction_event to the correct account or transaction-level source using the validated business key already available in the existing query.
Before changing the churn target, create profiling SQL that shows for each event_type_code:
row count
distinct account count
minimum and maximum event date
partial withdrawal flag based on the business rule
number of accounts that later closed
number of accounts with external rollover outcome
Add historical partial-withdrawal features only from the 12-month feature window up to as_of_date:
partial_withdrawal_count_12m
partial_withdrawal_amount_12m, if a validated amount field exists
days_since_last_partial_withdrawal_12m
partial_withdrawal_flag_12m
Do not use any transaction-event record after as_of_date as an ML feature.
Do not directly label partial withdrawal as churn. Treat it as a churn-risk or FUM-leakage feature because the account may remain open.
Keep full account closure and qualifying external full-exit logic as the churn target.
Add clear comments explaining that partial withdrawal indicates FUM leakage/churn risk, not confirmed full churn.
Ensure the final modelling dataset still contains exactly one row per ACCOUNT_ID.
Provide:
the profiling query first
then the revised full dataset query
then a validation query for row count, distinct account count, target distribution and duplicates
Do not generate Python code yet.
