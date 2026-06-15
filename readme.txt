You can add these descriptions in ADO for each task:

1. Review SonataODS table and column details

Review the 13 SonataODS source tables and capture available columns, data types, key fields, and initial relevance for churn/retention analysis. Document columns as Yes, Maybe, or No based on possible feature usage.

2. Explore relationships between tables

Analyze how the SonataODS tables are related using keys such as ACCOUNT_ID, CLIENT_ID, transaction IDs, and other join fields. Identify possible join paths required to prepare an account/member-level analytical dataset.

3. Identify blank/unusable columns

Identify columns that are fully blank, empty, technically unusable, or not meaningful for churn/retention modelling. Document these columns separately and mark them as excluded from feature consideration.

4. Perform basic data quality checks

Perform basic quality checks on key tables and important columns, including row counts, null counts, duplicate key checks, distinct values, date ranges, and join coverage. Document observations and possible impact on feature usage.

5. Understand business meaning of important columns

Review important Yes/Maybe columns and understand their business meaning in the context of retention, churn, rollover, inactivity, payment, transaction, and account status. Mark columns that need BA/business clarification.

6. Identify potential churn driver columns

Identify columns that may act as potential churn drivers or retention-risk indicators, such as account status, exit details, rollover out, inactivity, payment behaviour, financial outflows, tenure, and member/account attributes. Prepare the final list of recommended feature columns.

7. Prepare data exploration summary

Prepare a summary document covering tables reviewed, relationships, excluded columns, data quality observations, potential churn driver columns, assumptions, and open questions for business confirmation. This will be used as the final output of the data exploration activity.
