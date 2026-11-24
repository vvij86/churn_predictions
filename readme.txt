Audit "ml_mscs_mrt_target_labels.py" against the current Databricks SQL validation.

Do NOT change any code yet.

For snapshot:

"as_of_date = 2024-03-31"

Current ground-truth result:

"target_churn = 1" count = 8,751

Manual raw churn validation currently gives:

- RAW_NOT_GT = 10,020
- GT_NOT_RAW = 33

The manual raw churn logic currently uses:

- eligible accounts from "member_retention_features" for "2024-03-31"
- "exitDateRecorded > 2024-03-31"
- "exitDateRecorded <= 2024-06-29"
- "exitType = 'Exit'"
- "dateOfDeath IS NULL"
- exclude "AccountRolloverPayment.internalTransferFlag = true"

Please inspect the exact implementation in "ml_mscs_mrt_target_labels.py" and report:

1. Every source table used to derive "target_churn"
2. Every condition required for "target_churn = 1"
3. Any additional exit/churn source besides "AccountSummary.exitDateRecorded"
4. Exact internal-transfer exclusion logic
5. Exact death/deceased exclusion logic
6. Any databaseCode or eligibility filtering applied during target creation
7. Any date-window difference from the manual SQL
8. Any deduplication / precedence rule between multiple churn sources
9. Why 10,020 raw churn candidates are not labelled churn
10. Why 33 ground-truth churn accounts are not captured by the manual raw query

Then provide an equivalent Databricks SQL query that reproduces the exact "target_churn = 1" count for "2024-03-31".

Do not modify feature logic, target logic, or persisted tables in this step.
