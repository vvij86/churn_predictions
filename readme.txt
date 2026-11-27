Implement a minimal, configurable Payment to ATO exclusion in the existing Member Retention Analytics target label pipeline.

Business context:

- Six-calendar-month prediction window is confirmed.
- David has agreed to exclude Payment to ATO from churn.
- Nathan's final confirmation is pending.
- The exclusion must be easily reversible through central configuration.

Files in scope:

- ml_mscs_mrt_config.py
- ml_mscs_mrt_target_labels.py
- mult_snap_sanity_check.sql
- sqlserver_target_churn_validation_2024_03_31.sql

Follow the existing repository coding conventions and reuse previous review findings.

Requirements:

1. Add a central Boolean configuration parameter:
   
   EXCLUDE_PAYMENT_TO_ATO = True

2. When True, exclude qualifying Payment to ATO events from churn classification.

3. When False, restore the existing churn classification behaviour without the new ATO exclusion.

4. Ensure the ATO exclusion is consistently applied across both existing churn detection paths:
   
   - AccountSummary exit-based classification.
   - AccountRolloverPayment-based classification.

5. Use the existing payment classification and available source columns. Do not invent new payment types or classification rules.

6. Ensure the ATO payment is associated with the relevant exit event and outcome window. Do not exclude an account simply because it has an unrelated historical ATO payment.

7. For this provisional implementation, exclude ATO-related events from positive churn classification. Do not remove entire accounts from the modelling population. Preserve any independently qualifying churn events.

8. Align both existing target validation SQL scripts with the configurable ATO exclusion.

9. Preserve the existing six-calendar-month prediction horizon, outcome completeness checks, horizon metadata and account-level modelling grain.

10. Ensure rerunning an existing snapshot refreshes its target labels correctly without retaining stale labels.

Restrictions:

- Do not change Other payment type logic.
- Do not change Annuity classification.
- Do not change existing internal transfer or death exclusion rules.
- Do not change base population eligibility.
- Do not use AccountSummary.reportingDate for historical snapshot filtering or source row ordering.
- Do not modify feature engineering modules or consolidated feature logic.
- Do not modify historical snapshot orchestration or temporal split logic.
- Do not change existing table names.
- Do not regenerate the 40 historical feature snapshots.
- Do not create new files or notebooks.
- Do not execute scripts, SQL, jobs or terminal commands.
- Do not write, overwrite or delete Databricks table data.
- Do not proceed with model training or MLflow.

Finally, provide:

1. Modified files and concise change summary.
2. Explanation of how ATO exclusion works across both churn detection paths.
3. Exact configuration change required to revert the exclusion.
4. Databricks Python code to validate the 2024-03-31 snapshot without persistence.
5. Any assumptions or limitations in identifying ATO-related exits.

Keep the implementation minimal. Do not perform an unnecessary full repository analysis.
