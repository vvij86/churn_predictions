Follow .github/copilot-instructions.md.

Update only multi_snap_sanity_check.sql:

- Replace old ground-truth table references with member_retention_ground_truth_6m.
- Change expected churn count from 18771 to 36432 for 2024-03-31.
- Ensure all parameter blocks use calendar_months, 6, and exclude_payment_to_ato=true.
- Preserve existing business logic and account-level grain.

Do not modify other files or execute queries. Keep response concise.
