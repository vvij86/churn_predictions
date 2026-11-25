We are continuing the Member Retention Analytics ML development in Databricks.

Review and correct the recently generated files:

- ml_mscs_mrt_account_profile_features.py
- account_profile_features_validation.sql

1. Mandatory repository instructions

Before making any changes, read and strictly follow all applicable repository instruction files, including copilot-instructions.md.

Review the existing configuration, base population, historical snapshot implementation and approved business SQL references.

Do not override previously established business rules or architectural decisions.

2. Mandatory historical population rules

- Do NOT use AccountSummary.reportingDate for historical account eligibility, snapshot filtering, source row selection or ordering.
- reportingDate and exitDate are identical in many MercerEdge records. This limitation has already been identified during historical dataset development.
- Use fundJoinDate <= as_of_date for account joining eligibility.
- Reuse the existing validated historical base population logic.
- Do not introduce alternative account eligibility rules.
- Do not exclude accounts simply because reportingDate is NULL or greater than as_of_date.
- Do not introduce any additional population filters.

3. Account profile features

Retain the nine reviewed account profile features:

- account_tenure_months
- account_tenure_years
- member_age_years
- member_source
- is_super_flag
- is_pension_flag
- benefit_type
- benefit_class
- database_code

Verify each feature against behavioural_features_business_review.sql.

Do not introduce any additional unapproved features.

4. Point-in-time correctness

- Calculate account tenure using fundJoinDate and as_of_date.
- Calculate member age using dateOfBirth and as_of_date.
- Never use the current system date for historical feature calculations.
- Do not use reportingDate as a historical versioning timestamp.
- Do not assume fundJoinDate establishes historical validity for mutable account attributes.
- Where historical validity cannot be established, preserve NULL and document the limitation.
- Preserve NULL for unavailable attributes and flags instead of defaulting them to zero.
- Do not use exit-related or future outcome information as model predictors.
- Follow the existing approved business feature derivation logic.

5. Modelling grain and join integrity

- Strictly maintain account-level grain.
- Exactly one row per account_id per as_of_date.
- Preserve the existing eligible historical account population.
- Prevent duplicate records and multiplicative joins.
- Use deterministic source selection based on verified source semantics without relying on reportingDate.
- Report unresolved source ambiguity instead of arbitrarily selecting records.

6. Existing project constraints

- Historical source start date: 2023-04-01.
- Feature lookback window: 12 months, wherever applicable.
- Recent and prior windows: 90 days each.
- Support accounts with shorter tenure.
- Reuse existing configuration constants.
- AccountEngagementWeb still contains no data. Preserve existing NULL handling.
- CSAT, NPS and VOC data remain unavailable.
- Respect existing business-approved feature exclusions.
- ATO-related churn clarification is pending business confirmation.
- Do not introduce ATO, ST000 or migration-related exclusions.
- Feature engineering must remain independent of target labels and temporal split assignments.

7. Validation SQL correction

Update account_profile_features_validation.sql to align with the corrected Python implementation.

Include:

- Total record count.
- Distinct account snapshot key count.
- Duplicate account_id + as_of_date checks.
- Population reconciliation in both directions.
- NULL key checks.
- Invalid binary flag checks.
- Negative age and tenure checks.
- Future fundJoinDate and dateOfBirth checks for selected source records.
- Feature-level NULL distribution.
- Source-to-feature reconciliation.
- Historical attribute availability limitations.

Do not use reportingDate in the validation logic.

Do not report point-in-time validation as PASS where historical attribute validity cannot be established.

8. Manual execution instructions

Provide exact instructions to manually execute the corrected Python module in Databricks for the controlled snapshot:

as_of_date = 2024-03-31

Provide instructions to create the temporary validation view and execute the validation SQL within the same Spark session.

No permanent table creation is required for this standalone validation.

9. Strict scope restrictions

Modify ONLY:

- ml_mscs_mrt_account_profile_features.py
- account_profile_features_validation.sql

Do not modify:

- Repository instruction files.
- Configuration files.
- Base population logic.
- Historical snapshot generation.
- Target label generation.
- Temporal splitting.
- Consolidated feature modules.
- Other existing feature engineering modules.

Do not execute Python, SQL, notebooks, terminal commands or Databricks jobs.

Do not create, overwrite or delete any Databricks tables.

Do not proceed with workflow features, EDA or model training.

10. Expected implementation summary

After completing the corrections, provide:

- Files modified.
- Exact changes made.
- Confirmation that reportingDate is not used.
- Confirmation that existing historical population rules are preserved.
- Feature list and source mappings.
- Historical limitations.
- Expected output schema.
- Manual execution instructions.
- Expected validation results.

Perform a final static review against the repository instructions and existing business rules before completing the task.
