I want to develop my customer churn model POC incrementally.

For Version 1, I want to use only SonataODS data and create an
account-level baseline training dataset.

Later, in Version 2, I will add Salesforce features and compare whether
they improve model performance.

Please help me design only the SonataODS baseline dataset now.

Context:
- One row must represent one account_id.
- target_churn = 0 for retained accounts based on FR-RR-006.
- target_churn = 1 for not-retained accounts based on FR-RR-007.
- Partial rollover is not complete churn and should be captured separately.
- Death-related exits must be excluded from model training.
- Source DEV tables are read-only.
- I will run a SELECT query and export the result locally.
- I am new to ML development.

Please provide:
1. The SonataODS tables and columns I need to supply.
2. The proposed account-level feature categories.
3. Which columns are used only to create the target.
4. Which columns should be excluded because of data leakage.
5. A sample SonataODS-only training dataset structure.
6. A step-by-step checklist before writing the SQL.
7. Do not include Salesforce features at this stage.
