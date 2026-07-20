The modelling query returns 793,990 rows, but the validated trainable cohort contains 793,915 rows. This is 75 extra rows, so the join is likely creating duplicate account records.
Please create diagnostic SQL queries to check:
Duplicate ACCOUNT_ID values in the features CTE.
Duplicate ACCOUNT_ID values in the target_cte.
Duplicate ACCOUNT_ID values in the final joined result.
The total row count and distinct account count for each CTE and the final result.
The expected final result must contain exactly one row per ACCOUNT_ID.
After identifying the duplicate source, modify the SQL safely so each CTE returns one row per account before joining.
Do not use SELECT DISTINCT as a blind fix.
Do not generate Python code yet.
