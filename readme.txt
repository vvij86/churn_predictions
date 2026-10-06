Please perform a read-only churn-event validation across the MercerEdge tactical source.

Goal:
Confirm which actual events in the available MercerEdge data should be classified as:

1. Primary churn events
2. Churn-support / exit events
3. Non-churn exclusions
4. Risk indicators only
5. Unclear events requiring business confirmation

Use the following project files as the main reference:

- All_table_scripts.sql
- All_Other_tables_Not_explored.sql
- MercerEdge_ML_Churn_Driver_EDA_Phase2.xlsx
- MercerEdge_ML_Churn_Driver_EDA_Remaining_Tables_part2.xlsx
- build_merceredge_base_historical_dataset.sql
- profile_historical_snapshot_sources.py
- historical_snapshot_profile_results.json
- .env
- sample.py

Use read-only SQL only.

Review all relevant in-scope MercerEdge tables, especially:

- edgeSource.accountSummary
- edgeSource.accountRolloverPayment
- edgeSource.accountMoneyInflow
- edgeSource.accountNetMoneyFlow
- edgeSource.campaignEventDetails
- edgeSource.campaignEvents
- edgeSource.accountEngagementWorkflow
- edgePortalSource.pensionerData

Validate actual values and event patterns for:

- exitDate
- exitType
- internalTransferFlag
- dateOfPayment
- full / partial rollover indicators if available
- withdrawal / benefit payment indicators
- account closure / zero-balance exit patterns
- death indicators / dateOfDeath / deceasedDate
- MEMBER_EXIT
- ROLLOVER
- PAYMENT_MEMBER
- PAYMENT_EXTERNAL
- other exit-like event types found in the data

Do not assume an event is churn just because the name sounds like churn.

For every candidate event, check:
- which table and column it comes from
- actual distinct values / event names
- row counts
- whether it represents full exit, partial exit, transfer, death, or normal activity
- whether it occurs before, on, or after exitDate
- whether it can be used as the churn target
- whether it should only be used as supporting evidence
- whether using it as a feature would cause target leakage

Please create a summary table with:

Event / Rule
Source Table
Source Column(s)
Observed Values
Observed Count
Churn?
Exclude?
Risk Indicator Only?
Target Leakage Risk?
Recommended Use
Business Confirmation Needed?

Expected classification to verify, not blindly assume:

- Full rollover out -> likely churn
- Full withdrawal / full benefit payment -> likely churn
- Account exit / closure -> likely churn
- Internal transfer -> not churn
- Death exit -> exclude from churn modelling
- Partial rollover / partial withdrawal -> risk indicator, not churn
- MEMBER_EXIT -> likely outcome/target support, not feature

Also explicitly check whether "account closure", "full withdrawal", and "full rollover" are directly distinguishable in the current MercerEdge data or whether exitDate is the only reliable common churn outcome field.

At the end provide:

1. Final validated churn-event list
2. Final exclusion list
3. Final risk-indicator list
4. Events that should never be used as predictive features due to leakage
5. Items still requiring business SME confirmation

Do not modify any SQL or Python files.
Stop after showing the findings.
