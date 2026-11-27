Follow .github/copilot-instructions.md.

Generate an executable Databricks Python validation script for the 2024-03-31 snapshot using the existing target label pipeline.

Requirements:

- Run once with EXCLUDE_PAYMENT_TO_ATO = False and once with EXCLUDE_PAYMENT_TO_ATO = True.
- Ensure the imported target label module actually uses the respective flag for each execution.
- Use the existing six-calendar-month outcome horizon from the config.
- Explicitly set persist_output=False for both runs.
- Compare total accounts, churn accounts, non-churn accounts, null targets, churn percentage and duplicate counts.
- Identify accounts whose churn label changed from 1 to 0 and verify their ATO payment events.
- Validate potential date mismatches between ATO payments and AccountSummary exits.
- Ensure independently qualifying non-ATO churn events remain unaffected.
- Maintain account-level grain: one row per account_id per as_of_date.
- Do not use AccountSummary.reportingDate for historical filtering or source row ordering.
- Restore the original configuration after validation.

Display a before-and-after comparison table with PASS/FAIL validation results.

Do not modify existing files, business logic or persistent Databricks tables. Provide only the executable Python validation script.
