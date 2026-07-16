Please modify the existing full SonataODS training dataset query for the POC.
Apply these corrections:
In account_base, include only accounts that were active as of 2024-12-31:
a.COMMENCE_DATE <= p.as_of_date
AND (
    a.EXIT_DATE IS NULL
    OR CAST(a.EXIT_DATE AS date) > p.as_of_date
)
Remove ACCOUNT.STATUS_CODE = 'CLOS' from the churn-target logic because the current status may reflect a closure after the as-of date and would create future-data leakage.
Define account_closed_outcome_flag = 1 only when:
CAST(a.EXIT_DATE AS date)
    BETWEEN p.outcome_start_date AND p.outcome_end_date
Keep STATUS_CODE only as a diagnostic or target-supporting column. Do not use it as an ML feature or as a POC churn rule.
Define provisional target_churn as:
NULL for death-excluded accounts
1 when account_closed_outcome_flag = 1
1 when outcome_external_rollover_flag = 1
otherwise 0
Preserve:
one row per account_id
feature window 2024-01-01 to 2024-12-31
outcome window 2025-01-01 to 2025-03-31
death exclusions
existing historical ML features
no FUM or balance features
no partial/full rollover split
Do not redesign unrelated sections. Return:
the complete corrected SQL
a brief summary of exactly what changed
validation queries for row uniqueness, target distribution and closure/rollover overlap.
