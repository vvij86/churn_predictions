Review Check 07 and Check 08 in the existing mult_snap_sanity_check.sql file.

Check 07 results:

- ACCOUNT_FULL_EXIT_accounts = 0
- FULL_ROLLOVER_OUT_accounts = 0
- overlap_account_snapshots = 343044
- overlap_accounts = 123490
- duplicate_positive_target_rows = 0

Check 08 results:

- internal_transfer_candidates = 0
- deceased_positive_labels = 0
- partial_withdrawal_rollover_rows = 93356
- out_of_scope_database_codes = 0

Explain why both churn source counts are zero despite the large overlap count.

Also confirm whether the 93356 partial withdrawal/rollover rows represent actual business-rule violations or merely source event candidates.

Review the SQL logic and explain the results. Do not modify any files or execute any scripts or commands. Recommend a targeted read-only validation query only if required.

Also explain what Check 13c validates and whether account-level reconciliation is complete.
