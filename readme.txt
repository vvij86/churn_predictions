Task: SQL Server Table vs View Column Comparison

I have uploaded two SQL Server DDL files:

1. tables_ddl.sql – Contains CREATE TABLE scripts for 15 source tables.
2. views_ddl.sql – Contains CREATE VIEW scripts for 15 corresponding views.

Objective

Compare the columns available in each source table against its corresponding view and identify whether all source table columns are exposed in the view.

Instructions

Step 1: Identify Table and View Mappings

- Parse both SQL files completely.
- Identify all 15 source tables and their corresponding views.
- Match tables and views based on their object names, ignoring database and schema differences where appropriate.
- Report any tables or views without a matching counterpart.

Step 2: Extract Column Details

- Extract all column names from each CREATE TABLE definition.
- Extract the output column names from each CREATE VIEW definition.
- Resolve column aliases, including "AS" expressions, where possible.
- Handle "SELECT *", table aliases, joins, CTEs, subqueries and calculated columns correctly.
- If a view references multiple tables, identify which output columns originate from its corresponding source table.
- Do not assume that every column referenced in a view is exposed in its final output.

Step 3: Compare Columns
For each matching table and view:

- Identify columns available in both the table and view.
- Identify source table columns missing from the view.
- Identify additional view output columns not found in the source table.
- Identify renamed or aliased columns separately.
- Perform case-insensitive column-name comparison.
- Do not treat a renamed column as missing if its source-to-output mapping can be reliably established.
- Mark any uncertain mappings as "Requires Manual Verification".

Step 4: Generate Detailed Comparison Report

Prepare an Excel-ready report with the following columns:

Column| Description
Table Name| Source table name
View Name| Corresponding view name
Table Column Name| Column defined in the source table
View Column Name| Matching or aliased view output column
Available in View?| Yes / No / Requires Verification
Status| Matched / Missing / Renamed / Additional in View / Requires Verification
Remarks| Explanation of any mismatch

Include every source table column, even when it is missing from the view. Also include additional view-only output columns as separate rows.

Step 5: Generate Summary Report

Create a second report with these columns:

Table Name| View Name| Table Column Count| Matched Column Count| Missing Column Count| Additional View Column Count| Status

Status values:

- PASS – All source table columns are exposed in the view.
- FAIL – One or more source table columns are missing.
- REVIEW – Column mapping cannot be determined reliably.

Also provide a consolidated list of missing columns grouped by table/view.

Important Requirements

- Perform the comparison strictly using the uploaded DDL files.
- Do not connect to or modify the SQL Server database.
- Do not assume table and view columns are identical merely because their names match.
- Do not invent missing column definitions.
- Preserve the exact column names from the SQL scripts.
- Ensure all 15 table/view pairs are processed.
- If any CREATE VIEW definition is incomplete or references unresolved SQL objects, clearly flag it.

Expected Output

Generate an Excel workbook with three sheets:

1. Column_Comparison – Detailed column-by-column results.
2. Table_View_Summary – Summary of all 15 table/view comparisons.
3. Missing_Columns – Only columns missing from their respective views, with table and view names.

If Excel file generation is unsupported, produce three clearly separated CSV-ready tables.

Finally, provide a brief summary stating how many table/view pairs were compared, how many passed, how many failed, and the total number of missing source table columns.
