Create a Power BI sample output dataset with at least 1,000 rows using MercerEdge source data.

Use the column list from the attached mapping screenshots / existing mapping sheet.

Requirements:

1. Use real data from the MercerEdge database wherever a source table is identified.
2. Use the table mappings already provided, including tables such as:
   - edgeSource.accountSummary
   - edgeSource.accountMoneyInflow
   - edgeSource.accountNetMoneyFlow
   - edgeSource.accountRolloverPayment
   - edgeSource.accountInvestments
   - and any other MercerEdge table explicitly mapped to the requested output columns.
3. Read the SQL connection details from the existing .env file and reuse the existing working pyodbc connection logic.
4. Use account-level output grain:
   one row per account_id.
5. Generate at least 1,000 valid sample account rows.
6. Prefer accounts where the maximum number of mapped source attributes are available.
7. Do not fabricate source-backed fields if a real MercerEdge source exists.

Output columns should include the requested Power BI fields such as:

- Member Join Date
- Member Exit Date
- Latest Transaction Date
- Transaction Type
- Rollover In Amount
- Rollover Out Amount
- Benefit Paid Amount
- Outflow Destination
- Receiving Fund
- Investment Option
- Valuation Date
- Account Balance
- Unit Balance
- Last Contribution Date
- Last Transaction Date
- Retained Flag
- Internal Transfer Flag
- External Transfer Flag
- Account ID
- Member ID
- Fund ID
- Sub-Plan
- Employer Name
- Gender
- Age Band
- FUM Band
- Tenure Band
- Account Status
- Account Type
- Category
- Account Source
- Active Member
- Exit Member
- New Member
- Contribution Type
- Contribution Amount
- Exit Type
- Financial Activity
- Inactive Member
- Transfer Type
- Full / Partial Exit
- Life Stage
- Channel

For columns marked as NOT AVAILABLE in the source, leave them blank/null unless they are ML/demo output fields.

For ML/output-only columns, generate realistic sample values for Power BI testing only:

- Churn_Risk_Score
- Churn_Risk_Band
- Risk_Drivers
- CSAT_Score
- NPS_Score

Important:
- Clearly mark these generated fields as synthetic/demo values.
- Churn_Risk_Score should be between 0 and 1.
- Churn_Risk_Band can be derived as:
  Low: < 0.30
  Medium: 0.30 to < 0.70
  High: >= 0.70
- Risk_Drivers must be a single comma-separated string.

Example Risk_Drivers:
"Reduced contribution activity, Low campaign engagement, Recent partial rollover"

Generate realistic Risk_Drivers using only plausible churn-driver names, for example:
- Reduced contribution activity
- No recent contribution
- Low campaign engagement
- No recent web activity
- Increased helpline contacts
- Recent partial rollover
- Negative net money flow
- Reduced account balance
- Recent investment change
- Low communication engagement

For source-derived fields:
- preserve realistic data types
- preserve actual source values
- use latest/relevant record where multiple rows exist
- aggregate transaction/event data appropriately to one row per account
- do not duplicate accounts

For date-based fields:
- use the latest valid historical date for that account where appropriate
- do not use obviously invalid/future dates unless the source itself contains them and they are intentionally retained

For amount fields:
- use actual MercerEdge amounts where available
- if an account has no relevant transaction, use NULL or 0 consistently depending on the business meaning

For Retained Flag / Active Member / Exit Member / Inactive Member:
derive them from available account status / exit-related fields only if the logic can be supported by the source data.
Do not invent business rules silently.
If logic is uncertain, document it in a Notes sheet.

Create an Excel workbook named:

MercerEdge_PowerBI_Sample_Output_1000.xlsx

Workbook requirements:

Sheet 1: Sample_Output
- At least 1,000 account-level rows
- All requested Power BI columns
- Risk_Drivers as comma-separated text

Sheet 2: Column_Mapping
Include:
- Output Column
- Source Schema
- Source Table
- Source Column / Derivation
- Real vs Synthetic
- Transformation / Aggregation Logic
- Notes

Sheet 3: Validation
Include:
- Total rows generated
- Distinct account_id count
- Duplicate account_id count
- Null count by output column
- Source-backed columns used
- Synthetic columns generated
- Columns unavailable from MercerEdge
- Any mapping/logic assumptions

Important validation:
- final row count >= 1000
- one row per account_id
- no duplicate account_id
- real source values should be used whenever available
- ML/not-available fields must not overwrite or pretend to be source data
- Risk_Drivers must remain comma-separated in one Excel cell
- print a final summary in the terminal before completion

Before generating the workbook, inspect the mapped MercerEdge tables and confirm that the referenced columns actually exist. If any mapping from the screenshots does not exactly match the physical column name, resolve it using the DDL/schema and document the correction in Column_Mapping.

Do not modify any SQL Server data.
Read-only queries only.

