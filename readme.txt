Please continue from the previous investigation, but DO NOT modify build_merceredge_base_historical_dataset.sql yet.

The previous analysis concluded that no genuine account-level historical snapshot table was identified among the 18 in-scope MercerEdge tables.

However, several rows in the investigation were based only on DDL/schema review and were marked as "Not executed here".

I now want you to VALIDATE the conclusion using actual read-only profiling against the MercerEdge database.

OBJECTIVE
---------
Profile all 18 in-scope tables and confirm:

1. whether accountID exists
2. total row count
3. distinct accountID count
4. whether the same accountID appears multiple times
5. relevant date column(s)
6. date coverage / min-max dates
7. whether rows represent:
   - historical snapshot/state
   - transaction/event history
   - current/latest reference data
   - target/outcome data
8. whether the table can be used safely for point-in-time modelling

DO NOT modify the modelling SQL yet.

IN-SCOPE TABLES
---------------
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
Use these workspace files:

1. All_table_scripts.sql
   - main DDL/source structure

2. All_Other_tables_Not_explored.sql
   - additional DDL/source structure

3. MercerEdge_ML_Churn_Driver_EDA_Phase2.xlsx
   - previous EDA findings

4. MercerEdge_ML_Churn_Driver_EDA_Remaining_Tables_part2.xlsx
   - remaining-table EDA findings

5. build_merceredge_base_historical_dataset.sql
   - current base historical dataset query
   - review only, DO NOT modify yet

6. .env
   - database connection values

7. sample.py
   - known working SQL Server/pyodbc connection example

Use the DDL files as the source of truth for actual column names.
Do not guess column names.

DATABASE ACCESS
---------------
Use read-only SQL only.

Reuse the working connection approach from:
- .env
- sample.py

Use:
- pyodbc
- python-dotenv
- existing trusted connection / Windows authentication pattern
- TrustServerCertificate if already required

Do not create, update, delete, alter, or truncate anything.

PROFILE EACH TABLE
------------------
For every table, first inspect whether accountID exists.

If accountID exists, run:

SELECT
    COUNT(*) AS total_rows,
    COUNT(DISTINCT accountID) AS distinct_accounts
FROM <table>;

Then calculate whether multiple rows per account exist.

Run:

SELECT TOP 20
    accountID,
    COUNT(*) AS row_count
FROM <table>
WHERE accountID IS NOT NULL
GROUP BY accountID
HAVING COUNT(*) > 1
ORDER BY row_count DESC;

If no duplicate accountIDs exist, state:

one row per accountID observed

If duplicates exist, inspect sample accounts.

DATE PROFILING
--------------
For every relevant date/datetime column identified from the DDL:

Run min/max/null profiling such as:

SELECT
    MIN(<date_column>) AS min_date,
    MAX(<date_column>) AS max_date,
    SUM(CASE WHEN <date_column> IS NULL THEN 1 ELSE 0 END) AS null_count,
    COUNT(*) AS total_rows
FROM <table>;

For tables with multiple date columns, profile all relevant ones.

Examples conceptually:
- reportingDate
- exitDate
- dateOfDeath
- jobStartDate
- callDate
- requestDate
- effectiveDateFrom / effectiveDateTo
- investmentDate
- inflowDateReceived
- referenceDate
- dateOfPayment
- eventDate
- accurateDate
- dateAuthorityRequested
- terminationDate
- startDate
- dateSent
- openDate
- clickDate

Use actual DDL column names only.

ACCOUNT SUMMARY DEEP CHECK
--------------------------
For edgeSource.accountSummary, explicitly validate:

1. total row count
2. distinct accountID count
3. duplicate accountID count
4. number of rows where reportingDate IS NULL
5. number of rows where exitDate IS NULL
6. number of rows where exitDate IS NOT NULL
7. number of exited rows where reportingDate = exitDate
8. number of exited rows where reportingDate <> exitDate
9. min/max reportingDate
10. min/max exitDate
11. whether any account has multiple historical rows

Also sample exited accounts:

SELECT TOP 50
    accountID,
    reportingDate,
    exitDate,
    exitType,
    dateOfDeath
FROM edgeSource.accountSummary
WHERE exitDate IS NOT NULL
ORDER BY exitDate DESC;

Use actual available columns.

If the evidence confirms:
- one row per accountID
- reportingDate = exitDate for most/all exited accounts

then classify accountSummary as:

- current/latest account-level source
- target/outcome support source
- NOT a genuine historical snapshot source

Do not classify it as historical snapshot based only on the presence of reportingDate.

MULTI-ROW TABLE VALIDATION
--------------------------
For each table where accountID has multiple rows:

Select 3-5 sample accountIDs with multiple records.

For each sample account, inspect rows ordered by the recommended business date.

Example:

SELECT *
FROM <table>
WHERE accountID = <sample_account>
ORDER BY <recommended_date_column>;

Determine whether rows look like:

A. repeated account snapshots/state records
or
B. distinct transactions/events

Do not infer snapshot capability just because an account has multiple rows.

A transaction/event table is NOT a historical snapshot table.

SPECIAL PARTIAL POINT-IN-TIME TABLES
------------------------------------
Validate whether these provide partial "as-of" state:

1. AccountInsuranceCurrent
   - effectiveDateFrom
   - effectiveDateTo
   - can it determine whether insurance was active at @AsOfDate?

2. accountInvestments
   - investmentDate
   - does it represent valuation/holding history?
   - can latest-known investment state before @AsOfDate be reconstructed?

3. thirdPartyAuthority
   - request/effective/termination dates
   - can active authority status be reconstructed at @AsOfDate?

4. customerMapping
   - accurateDate or equivalent
   - can member/customer mapping be determined as-of a historical cutoff?

5. pensionerData
   - lifecycle dates
   - does it provide one current row or historical repeated rows?

Clearly distinguish:
- full account snapshot
from
- partial subdomain point-in-time state

HISTORICAL EVENT TABLE VALIDATION
---------------------------------
For these expected historical event/transaction sources, validate date coverage and multi-row history:

- accountEngagementWorkflow
- accountEngagementHelpline
- accountEngagementWeb
- accountMoneyInflow
- accountNetMoneyFlow
- accountRolloverPayment
- campaignAccountMapping
- campaignEventDetails
- accountInvestments if event/valuation based

Confirm whether they can safely support:

@FeatureStartDate <= event_date <= @AsOfDate

Do NOT create features yet.

TARGET / OUTCOME VALIDATION
---------------------------
Validate that:

edgeSource.accountSummary.exitDate

is appropriate as the primary churn outcome date.

Check whether:
- exitDate has sufficient historical coverage
- exitType is available for internal-transfer interpretation
- dateOfDeath/death indicators are available for death exclusion

Also inspect accountRolloverPayment for:
- dateOfPayment
- internalTransferFlag
- any full/partial rollover indicators

Do not use future outcome records as model features.

OUTPUT REQUIRED
---------------
Create a profiling summary table with columns:

Table Name
Has AccountID?
Total Rows
Distinct Accounts
Accounts With Multiple Rows
Relevant Date Columns
Min Date
Max Date
Date Null %
Observed Row Grain
Historical Snapshot Source?
Historical Event Source?
Current/Static Source?
Target/Outcome Source?
Partial Point-in-Time Source?
Leakage Risk
Recommendation

Then provide a second summary grouped as:

A. Genuine historical account snapshot tables

B. Partial point-in-time subdomain tables

C. Historical transaction/event tables

D. Current/static/reference tables

E. Target/outcome tables

F. Tables not useful for historical reconstruction

IMPORTANT DECISION RULE
-----------------------
Only classify a table as a genuine historical account snapshot source if actual profiling shows that:

- the same account can appear at multiple historical dates
- those rows represent account state at those dates
- important account-level attributes are persisted historically
- historical state can be reconstructed for an arbitrary @AsOfDate

Do not classify event/transaction history as an account snapshot.

FINAL CONCLUSION
----------------
At the end, clearly answer:

1. Was the earlier conclusion correct?
2. Is there any genuine historical account snapshot table among the 18 tables?
3. Which tables provide partial point-in-time state only?
4. Which tables provide reliable historical event/transaction history?
5. Which account-level fields cannot be reconstructed historically?
6. Can the tactical churn model still be built defensibly using event history?
7. What exact tactical data limitations should be documented?
8. What should be solved later in the Silver/Gold strategic layer?

DO NOT modify:
build_merceredge_base_historical_dataset.sql

until the profiling is complete and the findings are shown to me.
