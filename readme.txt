
I need to perform ML-focused data exploration on all tables defined in the file:

All_Other_tables_Not_explored.sql

This file contains the CREATE TABLE DDLs for the remaining MercerEdge tables that have not yet been explored.

Use the existing project Python environment and reuse the existing SQL Server connection approach from the .env file.

Connection requirements:
- Read SQL_SERVER, SQL_DATABASE and SQL_DRIVER from .env
- Use Windows Authentication / Trusted_Connection
- Use pyodbc
- Reuse the existing working SQL connection logic already present in this project if available
- Do not hardcode credentials in Python files

The final output must be an Excel workbook similar in structure and style to:

MercerEdge_ML_Churn_Driver_EDA_Phase2.xlsx

Create one worksheet per table defined in All_Other_tables_Not_explored.sql.

IMPORTANT:
- Every table in All_Other_tables_Not_explored.sql must be included
- Every column from every DDL must be included
- Do not drop columns just because they appear irrelevant
- The Excel column counts must exactly reconcile with the DDL column counts
- Do not use only a small sample to decide whether a column exists
- Use the DDL as the source of truth for table and column structure
- Use live SQL data only to enrich the DDL columns with profiling information

For each table worksheet, create these columns:

1. Ordinal
2. Column Name
3. Data Type
4. Key Role
5. Feature Group
6. Useful for Churn
7. Decision
8. Reason
9. Data Quality Notes
10. Row Count
11. Null Count
12. Null %
13. Blank Count
14. Blank %
15. Distinct Count
16. Sample Values
17. Min Value / Date
18. Max Value / Date
19. Date Coverage
20. Leakage Risk
21. Recommended Action

Useful for Churn must contain only:
- Yes
- Maybe
- No

Decision should use values such as:
- Include
- Consider
- Investigate
- Skip
- Join Key Only

Assess every column individually for churn/retention modelling relevance.

Use churn-related feature groups where applicable, for example:
- Identification
- Account / Product
- Demographics
- Status / Lifecycle
- Contributions / Money Inflow
- Withdrawals / Money Outflow
- Rollovers
- Balance / FUM
- Net Cashflow
- Engagement - Web
- Engagement - Helpline
- Insurance
- Investments
- Communication
- Geographic
- Preferences
- Date / Tenure
- Other

Key Role examples:
- Account Key
- Member Key
- Customer Key
- Identifier
- Date
- Category
- Numeric Measure
- Status
- Flag
- Free Text
- Unknown

For data profiling, query the actual SQL Server tables and capture where technically possible:
- total row count
- null count
- null percentage
- blank count for character columns
- blank percentage
- distinct count
- a small set of representative sample values
- minimum and maximum values for numeric/date columns
- minimum and maximum dates for date columns
- obvious constant columns
- 100% null columns
- very high-cardinality columns
- low-cardinality categorical columns
- date coverage
- columns with suspiciously recent/future values

Use efficient aggregate SQL. Do not load full large tables into pandas unnecessarily.

For sample values:
- use TOP / DISTINCT sampling
- limit sample values to a small readable set
- do not expose unnecessary PII values in the final workbook
- for obvious PII columns, describe the pattern instead of printing sensitive sample values where appropriate

For Data Quality Notes, summarize findings such as:
- Complete
- X% null
- 100% null - unusable
- Mostly null
- Blank values present
- Constant column
- High cardinality
- Categorical values need mapping
- Limited date coverage
- Future dates detected
- Duplicate-like identifier
- No major data-quality issue observed

For Leakage Risk:
- High
- Medium
- Low
- None

Mark High leakage risk where the field may only become available after churn or directly reveals the churn outcome, such as:
- exit status
- exit date
- closure status
- final withdrawal
- full rollover completion
- post-exit state
or similar future/outcome fields.

For Recommended Action, use values such as:
- Candidate feature
- Candidate after transformation
- Investigate further
- Exclude from ML
- Join key only
- Reference only
- Business confirmation required

Create an Overview worksheet summarizing each table with:

- Table Name
- Total Columns
- Yes
- Maybe
- No
- Include
- Consider
- Investigate
- Skip
- Join Key Only
- 100% Null Columns
- High Leakage Risk Columns
- Important Feature Groups
- General Comments

IMPORTANT:
Overview values must be calculated from the actual per-table worksheet rows.
Do not independently estimate overview counts.
The sum of Yes + Maybe + No must equal Total Columns for each table.
The decision counts must also reconcile with the total column count where applicable.

Also create a Validation worksheet containing:

- table name
- DDL column count
- generated worksheet column-row count
- missing column count
- extra column count
- profiling status
- DB accessibility status
- any errors

Validation requirements:
- every DDL table must have one worksheet
- every DDL column must appear exactly once in its corresponding worksheet
- no DDL column may be silently dropped
- overview table count must equal the number of tables in the SQL file
- overview total column counts must reconcile with per-table worksheets
- print a final validation summary in the terminal

Use the existing churn context:
- modelling grain is account level
- eventual modelling grain will be one row per account_id + as_of_date
- account/member/customer IDs are normally identifiers or join/reference fields, not predictive features
- avoid future-information leakage
- assess whether each column could contribute to churn-driver feature engineering later

Do NOT:
- create target_churn
- build the final modelling dataset
- perform model training
- modify source data
- create/update SQL Server tables

This task is only for data exploration and churn-driver identification.

Create the final workbook as:

MercerEdge_ML_Churn_Driver_EDA_Remaining_Tables.xlsx

Before declaring completion, run and print these checks:

1. Number of tables parsed from All_Other_tables_Not_explored.sql
2. Number of table worksheets generated
3. Total DDL columns parsed
4. Total worksheet column rows generated
5. Missing DDL columns
6. Extra columns
7. Tables with DB access/profiling failures
8. Overview reconciliation status

Do not consider the task complete unless:
- all tables are represented
- all columns are represented
- no columns are silently skipped
- overview counts reconcile
- validation checks pass or any unavoidable failures are explicitly listed
- the final Excel workbook is successfully generated
