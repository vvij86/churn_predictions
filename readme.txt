# Member Retention ML - Copilot Context Instructions

## 1. Business Reference SQL
Use the following business reference SQL as supporting logic for source mappings, lookup logic, description filters and type filters:

- MemberRetention_01-AccountBase_v006.sql
- MemberRetention_03-MemberRetentionMetrics_v005.sql

Use these as reference sources of truth where applicable.
Do not blindly copy all queries. Reuse only relevant logic, joins, mappings and filters.

## 2. Training History
The tactical ML solution is expected to use approximately 36 months of historical data for model training, subject to available source history.

Feature windows for individual snapshots may still use shorter periods such as the previous 12 months.

## 3. Primary Source Tables
Review the following approved source tables/views:

- edgeSource.accountSummary
- edgeSource.accountEngagementWorkflow
- edgeSource.accountEngagementHelpline
- edgeSource.accountEngagementWeb
- edgeSource.AccountInsuranceCurrent
- edgeSource.accountInvestments
- edgeSource.accountMoneyInflow
- edgeSource.accountNetMoneyFlow
- edgeSource.accountRolloverPayment
- edgeSource.campaignEventDetails
- edgeSource.campaignEvents
- edgeSource.customerMapping
- edgeSource.customerSummary
- edgeSource.thirdPartyAuthority
- tableau.fundListSource

Do not introduce additional source tables unless clearly required and supported by the reference logic.

## 4. Data Exploration References
Use the following EDA workbooks to understand useful churn-driver fields, data quality and source behaviour:

- MercerEdge_ML_Churn_Driver_EDA_Phase2.xlsx
- MercerEdge_ML_Churn_Driver_EDA_Remaining_Tables_part2.xlsx

## 5. DDL References
Use the following SQL files for table definitions, column names and data types:

- All_table_scripts.sql
- All_Other_tables_Not_explored.sql

## 6. Python Environment / Validation
Use the existing Python environment for any validation/profiling scripts.

Use:
- `.env` for required credentials/configuration
- `sample.py` as the reference database connection example

Do not hard-code credentials.

## 7. General ML Rules
- Grain: one row per account_id + AsOfDate.
- Use fundJoinDate <= AsOfDate for historical account existence.
- Use exitDateRecorded, not exitDate.
- exitDateRecorded can be used for eligibility and target creation, but not as a predictive feature.
- Internal transfers are not churn.
- Death-related exits are excluded.
- Predictive features must only use information available on or before AsOfDate.
- Do not use future outcome information as features.
- Maintain point-in-time safety.
- Reuse exact business mapping/filter logic from reference SQL where available.
- Do not invent lookup values, flow mappings, join keys or business meanings.
- If unclear, mark:
  TODO - BUSINESS / REFERENCE CONFIRMATION REQUIRED
- accountEngagementWeb is empty in UAT but populated in Prod:
  keep web features in scope,
  keep them NULL/unavailable in UAT,
  and mark them for Prod validation.
