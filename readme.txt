Please redo the churn-table prioritization using ONLY the 85 tables that came from:

All_Other_tables_Not_explored.sql

Do NOT include any of the previously explored 17 tables.

Use only the worksheets/tables that were generated from the 85-table exploration workbook:

MercerEdge_ML_Churn_Driver_EDA_Remaining_Tables.xlsx

I want a shortlist of the most useful tables among these 85 only.

Assess each table based on:
- churn/retention relevance
- behavioural usefulness
- financial usefulness
- lifecycle usefulness
- engagement usefulness
- account-level usability
- date coverage
- null percentage / data quality
- leakage risk
- ability to derive meaningful ML features
- whether the table can join reliably to account_id

Please classify the 85 tables into:

1. High Priority
2. Medium Priority
3. Low Priority / Reference Only
4. Exclude

For High Priority tables, provide:

- Table Name
- Why useful for churn
- Important candidate columns
- Example derived ML features
- Data quality concern
- Leakage concern
- Recommended action

IMPORTANT:
- Do not mention or compare against the previous 17 explored tables.
- Do not include any table unless it is present in All_Other_tables_Not_explored.sql.
- Be selective.
- Do not rank a table highly just because it has many columns.
- IDs/join keys alone do not make a table useful for churn.
- Tables with mostly null or unusable churn-related fields should be downgraded.
- Future/outcome fields should be marked as target-support / leakage risk, not predictive features.
- Prefer tables that can produce account-level behavioural or financial features before as_of_date.

At the end, give me:

1. Top 10 most important tables among these 85 only
2. Next 10 worth investigating
3. Target-support / churn-event tables among these 85
4. Join/reference-only tables among these 85
5. Tables that can be excluded from further ML work

Final Top 10 format:

Table Name | Priority | Main Churn Signal | Key Candidate Columns | Example Features | Main Concern | Recommended Action

Before finalizing, verify that every recommended table exists in All_Other_tables_Not_explored.sql.
