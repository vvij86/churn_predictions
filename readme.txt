Based on your previous analysis, update only the existing "mult_snap_sanity_check.sql" file.

1. Fix the incorrect string literals in the consolidated Check 07 summary to correctly match ACCOUNT_FULL_EXIT and FULL_ROLLOVER_OUT.
2. Report distinct account counts and account_id + as_of_date counts separately for each churn source and their overlap.
3. Enhance Check 08c to distinguish partial withdrawal source candidates from actual violations where partial withdrawals alone incorrectly qualify an account as churn.
4. Include Check 13c account-level mismatch counts in the consolidated summary, with PASS only when both mismatch directions return zero.
5. Preserve all other existing validation logic and approved business rules.

Do not modify any Python files, including ml_mscs_mrt_target_labels.py.

Do not execute any SQL scripts, Python files, notebooks, terminal commands or background processes.

Do not modify or overwrite any Databricks tables.

I will manually execute the updated validation queries.
