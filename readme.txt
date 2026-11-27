Follow .github/copilot-instructions.md.

Update only multi_snap_sanity_check.sql:

- Replace old ground-truth table references with member_retention_ground_truth_6m.
- Update expected churn count from 18771 to 36432.
- Ensure calendar_months, 6, and exclude_payment_to_ato=true across all parameter blocks.

Separately, provide a read-only Databricks SQL query showing monthly churn-source event counts and data coverage for AccountSummary exits, full rollover outs and Payment to ATO from Jan 2024 to Oct 2026, to investigate the churn rate drop from 4.28% to 1.23%.

Preserve existing business logic and account-level grain. Do not use AccountSummary.reportingDate for historical filtering or ordering.

Do not modify other files or execute queries. Keep response concise.
