Follow .github/copilot-instructions.md.

Update only multi_snap_sanity_check.sql:

- Replace old ground-truth table references with member_retention_ground_truth_6m.
- Update expected churn count from 18771 to 36432 for 2024-03-31.
- Ensure all parameter blocks use calendar_months, 6, and exclude_payment_to_ato=true.
- Preserve existing business logic, account-level grain and Databricks SQL syntax.

Also provide a minimal read-only Python dry-run script for multi-snapshot target validation using the updated pipeline, with persist_output=False and complete outcome windows only.

Do not modify other files, execute queries or write to tables. Keep the response concise.
