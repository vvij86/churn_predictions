Please review the current base historical dataset SQL and correct the date-handling logic.

IMPORTANT:
Do NOT use edgeSource.accountSummary.reportingDate as the model as_of_date.

The model as_of_date must be a fixed parameter that we define, for example:

DECLARE @AsOfDate DATE = '2025-03-31';

Keep:

@FeatureStartDate
@AsOfDate
@OutcomeStartDate
@OutcomeEndDate

The purpose of source-table date columns is only to identify which source records were available within the historical feature window or which record represents the correct historical snapshot.

For each of the following 18 MercerEdge tables, inspect the actual DDL and identify the most appropriate date column(s) for historical filtering/snapshot selection:

1. merceredge.edgeSource.accountSummary
2. merceredge.edgeSource.accountEngagementWorkflow
3. merceredge.edgePortalSource.pensionerData
4. merceredge.edgeSource.accountEngagementHelpline
5. merceredge.edgeSource.accountEngagementWeb
6. merceredge.edgeSource.AccountInsuranceCurrent
7. merceredge.edgeSource.accountInvestments
8. merceredge.edgeSource.accountMoneyInflow
9. merceredge.edgeSource.accountNetMoneyFlow
10. merceredge.edgeSource.accountRolloverPayment
11. merceredge.edgeSource.campaignEventDetails
12. merceredge.edgeSource.campaignEvents
13. merceredge.edgeSource.customerMapping
14. merceredge.edgeSource.customerSummary
15. merceredge.edgeSource.thirdPartyAuthority
16. merceredge.tableau.fundListSource
17. merceredge.edgeSource.campaign
18. merceredge.edgeSource.campaignAccountMapping

For each table, provide:

- table name
- candidate date columns
- recommended date column
- why it is appropriate
- whether it should be used for:
  - snapshot selection
  - feature-window filtering
  - target/outcome logic
  - reference only
- whether it presents any target-leakage risk

Use the actual DDL files as the source of truth:
- All_table_scripts.sql
- All_Other_tables_Not_explored.sql

Do NOT guess column names.

DATE LOGIC
----------

The modelling dates must work like this:

Feature window:
@FeatureStartDate <= source_event_date <= @AsOfDate

Outcome window:
@OutcomeStartDate <= qualifying_exit_date <= @OutcomeEndDate

The model as_of_date must always remain:

@AsOfDate AS as_of_date

Do NOT set:

as_of_date = reportingDate
as_of_date = exitDate
as_of_date = transactionDate
as_of_date = eventDate

For accountSummary:

- reportingDate may be used to select the latest available historical snapshot on or before @AsOfDate
- exitDate must be used only for churn target / eligibility logic
- dateOfDeath must be used only for death exclusion logic
- do not treat exitDate as a feature-window date

For transaction/event tables:

Use the actual event/transaction/business-effective date column appropriate to that table.

Examples conceptually:
- contribution/payment table -> contribution/payment date
- rollover table -> rollover/payment date
- web table -> web activity date
- helpline table -> call/contact date
- campaignEventDetails -> eventDate
- campaignAccountMapping -> dateSent/openDate/clickDate as appropriate

But verify all column names from the DDL before changing SQL.

IMPORTANT:
Do NOT start feature engineering yet.

This review is only to make sure the base historical dataset uses correct historical date columns and a fixed modelling as_of_date.

At the end, produce a summary table like:

Table | Recommended Date Column | Purpose | Leakage Risk | SQL Usage

Then update the base historical dataset SQL accordingly.
