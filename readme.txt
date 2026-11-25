We are continuing the Member Retention Analytics ML development in Databricks.

Based on the recent feature engineering code review, account profile features and workflow behaviour features are missing from the existing Python implementation.

For this task, focus ONLY on account profile feature engineering.

1. Review existing references

Review the following files before implementation:

- behavioural_features_business_review.sql
- ml_mscs_mrt_config.py
- ml_mscs_mrt_base_population.py
- ml_mscs_mrt_consolidated_features.py
- ml_mscs_mrt_historical_snapshots.py
- Existing individual feature engineering modules
- Repository Copilot instructions

Identify the reviewed account profile features from the business SQL and follow the existing Python coding conventions.

2. Create a dedicated Python module

Create:

ml_mscs_mrt_account_profile_features.py

Implement only the account profile features available in the reviewed business SQL and currently approved feature definitions.

Potential feature categories include:

- Account tenure
- Member demographics
- Account characteristics
- Fund and product characteristics
- Other reviewed account profile attributes

Do not assume column names or introduce unapproved features. Verify source mappings against existing repository references.

3. Modelling grain

The modelling grain must strictly remain at account level.

- Exactly one row per account_id per as_of_date.
- Use the existing historical account population as the base.
- Preserve all eligible account snapshot records.
- Prevent duplicate records from source joins.
- Support members with multiple accounts without combining their account-level features.
- Follow existing account_id and as_of_date key conventions.

4. Point-in-time correctness

All features must represent information valid and available as of the respective historical snapshot date.

- Calculate age and account tenure relative to as_of_date, where approved.
- Do not use the current system date for historical feature calculations.
- Do not use future events or future account information.
- Do not blindly use current-state demographic or account attributes for historical snapshots.
- Where historical validity cannot be established, preserve NULL and document the limitation.
- Do not use exit dates, future exit status, final payment information, target_churn or other outcome-related information as predictors.

5. Historical snapshot support

Follow the existing single-snapshot feature module design so the new module can be reused by the historical snapshot orchestration.

- Historical source start date: 2023-04-01.
- Use configurable as_of_date.
- Reuse existing configuration constants wherever applicable.
- Support accounts with shorter tenure.
- Do not exclude accounts merely because 12 months of history is unavailable.
- Do not artificially replace unavailable historical information with zero.

6. Source availability and business restrictions

- AccountEngagementWeb is still empty. Preserve NULL values for unavailable web engagement features in the existing implementation.
- Do not introduce web engagement features into the account profile module.
- Do not introduce unavailable CSAT or NPS features.
- Respect all existing business-approved feature exclusions.
- ATO-related churn definition clarification is still pending.
- Do not introduce any ATO-related target or population exclusions.
- Feature engineering must remain independent of target labels and temporal split assignments.

7. Performance and scalability

The historical dataset contains approximately 32.6 million account snapshot records across 40 monthly snapshots.

- Use PySpark or Spark SQL consistent with existing modules.
- Avoid Pandas conversion and large driver-side collections.
- Avoid unnecessary joins and repeated source scans.
- Use efficient aggregate-based validation.
- Maintain compatibility with existing Databricks execution patterns.

8. Validation SQL

Create a separate read-only Databricks SQL validation file:

account_profile_features_validation.sql

Include checks for:

- Total record count.
- Distinct account_id and as_of_date count.
- Duplicate account snapshot keys.
- Population reconciliation against the historical account base.
- Missing and invalid feature values.
- Age and tenure validity, where applicable.
- Future-date violations.
- Historical data availability limitations.
- Source-to-feature reconciliation for selected sample accounts.

Use actual existing table and column names. Do not assume an output table already exists.

9. Expected implementation summary

After implementing the module, provide:

- Files created or modified.
- Complete implemented feature list.
- Source table and column mapping for every feature.
- Feature derivation logic.
- Historical availability and point-in-time limitations.
- Features deferred due to unavailable source data.
- Expected output schema.
- Manual Databricks execution instructions for one controlled snapshot: 2024-03-31.
- Recommended validation procedure.

10. Strict scope restrictions

- Create only the account profile feature module and its validation SQL.
- Do not implement workflow behaviour features yet.
- Do not modify existing feature engineering modules.
- Do not modify base population, historical snapshots, target labels or temporal splitting logic.
- Do not update consolidated feature integration yet.
- Do not execute Python scripts, SQL queries, notebooks or terminal commands.
- Do not run Databricks jobs or background processes.
- Do not create, overwrite or delete Databricks tables.
- Do not proceed with EDA or model training.

If additional dependencies or changes to existing files are required, report them separately instead of making those changes.

Implement the code only and provide the implementation summary for manual review.
