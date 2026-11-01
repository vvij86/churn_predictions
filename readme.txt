Review and validate the existing SQL file "consolidated_behavioural_feature_dataset_review.sql".

Context:

- Project: Mercer Member Retention Analytics
- Database: MercerEDGE (SQL Server)
- Current AsOfDate: "2024-03-31"
- Current query output: approximately 785,462 rows
- Dataset grain: One row per "accountID + as_of_date"
- Purpose: Technical validation of the consolidated behavioural feature dataset before ML training.

Important: Do not modify the existing SQL file or change its business logic. Create a separate validation SQL file named "consolidated_behavioural_feature_validation.sql".

Validation requirements

1. Dataset uniqueness

- Check total rows and distinct "accountID + as_of_date" combinations.
- Identify duplicate account/date combinations.
- Report duplicate counts and sample records.

2. Feature coverage analysis

- Automatically identify all behavioural feature columns from the consolidated dataset.
- Calculate populated count, NULL count and NULL percentage for each feature.
- Include zero-value counts separately from NULL counts.
- Highlight features with more than 90% NULL values.
- Pay particular attention to helpline features such as "helpline_contact_count_12m", "helpline_inquiry_count_12m", "helpline_active_days_12m", and "days_since_last_helpline_contact".

3. Source data availability

- Identify the source tables/views used for each behavioural feature group.
- Check whether source data exists within the relevant historical feature window.
- Report available record counts, distinct account counts, and date ranges.
- Clearly distinguish missing source data from missing join matches.

4. Join validation

- Review account-level joins between eligible accounts and behavioural source tables.
- Check unmatched account counts and match percentages.
- Identify joins that could introduce duplicates or unexpectedly produce NULL values.
- Confirm transactional and event records are aggregated to account level before joining.

5. Date validation

- Confirm no behavioural features use information after "@AsOfDate".
- Validate the applicable 12-month feature window.
- Identify any potential future-data leakage.
- Verify source date columns and boundary conditions.

6. Missing-value interpretation

- Distinguish between no recorded activity, unavailable source data, and failed joins.
- Do not automatically replace NULL values with zero.
- Note that "edgeSource.accountEngagementWeb" is currently empty in UAT; preserve NULL handling for unavailable website features.

Expected output

Generate executable, read-only SQL Server validation queries that produce:

1. Dataset summary and duplicate checks.
2. Feature coverage report with NULL percentages.
3. Source-table availability report.
4. Join-match coverage report.
5. Feature-window and leakage checks.
6. A concise PASS/WARN/FAIL summary with explanations and recommended fixes.

Use the actual table names, column names, join conditions, filters and feature definitions from the existing SQL files. Do not assume or invent schema details.

Constraints:

- Do not change the original consolidated dataset.
- Do not add ML training, scoring, deployment or MLOps logic.
- Do not execute expensive full-table scans unnecessarily.
- Do not claim a validation has passed without evidence.
- If an individual check cannot be implemented with the available schema, explain what is missing rather than inventing logic.

First inspect the existing SQL and create the validation script. Do not modify the original file.
