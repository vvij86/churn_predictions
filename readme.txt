Before making further changes to the base historical modelling dataset query, I want to verify whether MercerEdge contains a genuine historical account snapshot source.

IMPORTANT CONTEXT
-----------------
We have already confirmed that:

- edgeSource.accountSummary contains only one distinct row per accountID
- there are no duplicate accountIDs in accountSummary
- for exited accounts, reportingDate appears to be updated to the exit date
- in observed exited records:

  reportingDate = exitDate

Therefore:

- do NOT assume accountSummary is a historical snapshot table
- do NOT use reportingDate as the model as_of_date
- do NOT use exitDate as the model as_of_date
- @AsOfDate must remain a fixed modelling cutoff date defined by us

The current task is ONLY to investigate which table(s), if any, can provide a genuine historical account snapshot.

Do NOT modify the modelling query yet.
Do NOT start feature engineering yet.

IN-SCOPE MERCEREDGE TABLES
--------------------------
Please investigate all of these 18 tables:

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

IMPORTANT PROJECT FILES
-----------------------
Use the following files already available in the workspace:

1. All_table_scripts.sql
   - main DDL/source structure
   - use this as a source of truth for actual table and column names

2. All_Other_tables_Not_explored.sql
   - additional DDL/source structure
   - use this to verify columns for remaining tables

3. MercerEdge_ML_Churn_Driver_EDA_Phase2.xlsx
   - previous EDA for the initially explored tables
   - use this for data availability, nulls, date coverage, and ML relevance

4. MercerEdge_ML_Churn_Driver_EDA_Remaining_Tables_part2.xlsx
   - EDA for the remaining MercerEdge tables
   - use this for historical/date coverage and data quality understanding

5. build_merceredge_base_historical_dataset.sql
   - current generated base historical dataset query
   - review it only to understand what assumptions it currently makes
   - do NOT modify it yet

6. .env
   - database connection values

7. sample.py
   - known working pyodbc / SQL Server connection example

Use the actual DDL files as the source of truth.
Do NOT guess column names.

DATABASE ACCESS
---------------
Use read-only SQL only.

Reuse the existing connection approach from:

sample.py
.env

Use:
- pyodbc
- python-dotenv
- trusted connection / Windows authentication if already configured
- TrustServerCertificate if required

Do not create/update/delete anything in MercerEdge.

PRIMARY INVESTIGATION
---------------------
For each of the 18 tables, determine:

1. Does accountID exist?
2. If yes, can the same accountID appear multiple times?
3. What date/datetime columns are available?
4. What is the business meaning of each relevant date column?
5. Does the date represent:
   - historical snapshot date
   - transaction/event date
   - effective date
   - created/updated timestamp
   - outcome date
   - current/latest record date
6. Can the table reconstruct what an account looked like at a historical @AsOfDate?
7. Does the table contain historical account-level attributes?
8. Is the table suitable as:
   - historical account snapshot source
   - historical event/transaction source
   - current/static lookup
   - target/outcome source
   - feature-engineering source only

HISTORICAL SNAPSHOT DEFINITION
------------------------------
A genuine historical snapshot table should ideally look conceptually like:

accountID | snapshot_date | account_status | balance | other fields
A1001     | 2024-03-31    | Active         | ...
A1001     | 2024-06-30    | Active         | ...
A1001     | 2024-09-30    | Active         | ...
A1001     | 2024-12-31    | Active         | ...

The same account should be capable of appearing at multiple historical dates.

Do NOT classify a table as a historical snapshot table just because it has a date column.

For example:

- workflow dates are event dates
- contribution/payment dates are transaction dates
- campaign dates are engagement dates
- exitDate is an outcome date

Those are historical event sources, not necessarily historical account snapshots.

IMPORTANT ACCOUNT-LEVEL FIELDS
------------------------------
Specifically investigate whether any table can provide historical values for:

- account status
- account type
- account balance
- FUM
- member/account state
- active/inactive state
- investment value
- pension status
- insurance status
- other important account-level profile attributes

We need to know whether these values existed historically at each @AsOfDate or whether only the latest/current value is available.

PROFILING QUERIES
-----------------
For each table containing accountID, run read-only profiling such as:

SELECT
    COUNT(*) AS total_rows,
    COUNT(DISTINCT accountID) AS distinct_accounts
FROM <table>;

If:

total_rows > distinct_accounts

then identify sample accountIDs with multiple rows:

SELECT TOP 20
    accountID,
    COUNT(*) AS row_count
FROM <table>
WHERE accountID IS NOT NULL
GROUP BY accountID
HAVING COUNT(*) > 1
ORDER BY row_count DESC;

For a few accounts with multiple rows, inspect the records ordered by the most relevant date column.

Example pattern:

SELECT *
FROM <table>
WHERE accountID = <sample_account>
ORDER BY <candidate_date_column>;

Do not assume the date column.
Choose it only after checking the DDL.

ACCOUNT SUMMARY SPECIFIC CHECK
------------------------------
For edgeSource.accountSummary confirm:

- total rows
- distinct accountIDs
- duplicate accountID count
- reportingDate coverage
- exitDate coverage
- count where reportingDate = exitDate
- count where reportingDate <> exitDate
- count where exitDate IS NULL
- whether any account has multiple historical records

If only one row per accountID exists, classify accountSummary appropriately as:

current/latest account-level source
and/or
target/outcome source

but NOT as a historical snapshot source.

Also clearly state which fields from accountSummary can still safely be used for:

- identifiers
- churn outcome
- death exclusion
- internal transfer support
- static/reference attributes

and which fields cannot safely be used historically without point-in-time evidence.

DATE COLUMN REVIEW
------------------
For each of the 18 tables, produce:

Table
Candidate Date Column(s)
Recommended Date Column
Date Meaning
Historical Snapshot / Event / Lookup / Outcome
Can Use for Feature Window?
Can Use for As-of Snapshot?
Leakage Risk
Comments

Important:

@AsOfDate must remain a manually supplied modelling date.

Do NOT recommend any source-table date column as the model as_of_date unless there is a very strong, verified reason.

The expected modelling concept remains:

@FeatureStartDate
       ↓
historical observations/events
       ↓
@AsOfDate
       ↓
future outcome period
       ↓
@OutcomeEndDate

HISTORICAL EVENT TABLES
-----------------------
If a table is not a snapshot table but contains valid history, classify it separately.

Examples could include:

- accountMoneyInflow
- accountNetMoneyFlow
- accountRolloverPayment
- accountEngagementWeb
- accountEngagementHelpline
- accountEngagementWorkflow
- accountInvestments
- campaignAccountMapping
- campaignEventDetails

For such tables, determine the best date column for later feature-window filtering:

@FeatureStartDate <= event_date <= @AsOfDate

Do NOT create the features now.

This is only source/date assessment.

TARGET / OUTCOME SOURCES
------------------------
Identify which table/date is appropriate for churn outcome creation.

Current expected primary outcome source:

accountSummary.exitDate

The target should later be determined independently from the historical feature snapshot:

exitDate > @AsOfDate
AND exitDate <= @OutcomeEndDate

Do not mix future exit rows into historical feature data.

IMPORTANT:
Since reportingDate = exitDate for exited accounts, explicitly explain whether this confirms that reportingDate is acting as an update/latest-record date rather than a reliable historical snapshot date.

OUTPUT REQUIRED
---------------
Create a clear summary table with columns:

Table Name
Has AccountID?
Total Rows
Distinct Accounts
Multiple Rows per Account?
Candidate Date Columns
Recommended Date Column
Date Meaning
Historical Snapshot Source?
Historical Event Source?
Current/Static Lookup?
Target/Outcome Source?
Feature Engineering Later?
Leakage Risk
Recommendation

Then create a second shortlist:

A. Best candidate historical snapshot table(s)

B. Historical transaction/event tables

C. Current/static/reference tables

D. Target/outcome tables

E. Tables not useful for historical reconstruction

FINAL CONCLUSION
----------------
At the end, clearly answer:

1. Is there a genuine historical account snapshot table among these 18 tables?

2. If yes:
   - which table
   - which snapshot date column
   - what historical fields it provides
   - why it is suitable

3. If no:
   clearly state:
   "No genuine historical account snapshot table was identified among the 18 in-scope MercerEdge tables."

4. If no historical snapshot exists:
   explain which parts of the churn modelling dataset can still be reconstructed reliably from event/transaction history.

5. Identify which account-level attributes cannot be made point-in-time safe from the available tactical data.

6. Explain the implications for the tactical churn model.

7. Recommend what should be documented as a tactical data limitation and what should later be solved in the strategic/Silver/Gold data layer.

IMPORTANT:
Do not change build_merceredge_base_historical_dataset.sql yet.

First complete this investigation and show me the findings.

I will review the findings before we modify the base historical modelling dataset query.
