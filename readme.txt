I am creating a beginner-level POC to evaluate the best machine-learning model for customer churn analytics.

Context:

1. My source data is available in read-only DEV tables.
2. The sources include SonataODS tables and Salesforce tables.
3. I have already completed EDA and identified potentially useful churn-driver columns.
4. The required dataset grain is account level, meaning one row per account_id.
5. FR-RR-006 defines retained accounts.
6. FR-RR-007 defines not-retained/churned accounts.
7. The target column must be:

   target_churn = 0 for retained accounts
   target_churn = 1 for not-retained/churned accounts

8. Partial rollover should not be classified as complete churn. It should be captured as a separate feature or flag.
9. Death-related exits should be excluded from the normal churn-model training population.
10. I have only read access, so I cannot create or update DEV tables.
11. I will run a SELECT query, export the result as CSV or Parquet, and perform the ML model evaluation locally using Python.
12. I am new to ML development, so explain everything clearly and step by step.

Do not write the final SQL query yet.

First, help me design the training dataset specification.

Please provide:

1. The categories of columns required in the training dataset.
2. The mandatory identifier and target columns.
3. Suggested account-level churn-driver features from SonataODS.
4. Suggested Salesforce churn-driver features.
5. Columns required to create the retained/not-retained target.
6. Columns required for death-related exclusion.
7. Features that must be calculated for a historical period, such as the previous 12 months.
8. Features that could cause data leakage and must not be included.
9. A sample final dataset structure with example column names and descriptions.
10. A checklist of information I need to provide before you can generate the SQL query.

Clearly separate:
- identifier columns
- feature columns
- target-supporting columns
- exclusion columns
- final target column
