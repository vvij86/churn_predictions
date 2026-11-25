We are continuing the Member Retention Analytics ML development in Databricks.

Current progress:

- Historical snapshot generation completed.
- Ground-truth and target label generation completed.
- Ground-truth sanity checks completed.
- Temporal splitting implementation and dry run completed.
- Historical dataset contains 32,616,602 records across 40 monthly snapshots.
- Business clarification regarding ATO-related account exits is pending.
- Final temporal split persistence is temporarily on hold.

We want to continue feature engineering independently of the pending churn definition clarification.

Objective:

Review all existing feature engineering Python modules, consolidated feature generation logic, configuration files, reviewed business SQL queries and feature definitions available in the repository.

Do not recreate existing feature engineering modules unnecessarily.

1. Existing implementation review

For each feature engineering module, identify:

- File name.
- Feature category.
- Source tables and columns.
- Features currently implemented.
- Business rules and filters applied.
- Whether the implementation supports a single snapshot or multiple historical snapshots.
- Whether any changes are required.

2. Modelling grain

The modelling grain must strictly remain at account level.

- Exactly one row per account_id per as_of_date.
- Aggregate transaction-level, member-level and engagement-level records to account snapshot level as appropriate.
- Identify potential duplicate records and incorrect join conditions.
- Ensure consolidated feature joins use both account_id and as_of_date.

3. Historical snapshot support

Review whether the existing feature modules can support all 40 historical monthly snapshots rather than only DEFAULT_AS_OF_DATE.

- Historical source start date: 2023-04-01.
- Feature lookback window: 12 months.
- Recent window: 90 days.
- Prior window: 90 days.
- Support shorter historical windows where full history is unavailable.
- Identify how insufficient historical coverage is represented.
- Avoid treating unavailable history as zero activity.

4. Point-in-time correctness and leakage prevention

Review every feature for potential temporal leakage.

- Only use information available on or before the respective as_of_date.
- Check whether source records were actually available at the historical snapshot date.
- Identify features derived from current-state fields that may not be historically accurate.
- Exclude future exit events, completed full rollovers and other outcome-related information from predictors.
- Ensure target_churn, outcome dates, churn event details and transition-related outcome flags are not used as model features.
- Identify any limitations in achieving complete point-in-time correctness.

5. Feature categories

Review all existing feature groups, including:

- Account and demographic features.
- Account tenure.
- Financial and balance features.
- Contribution behaviour.
- Withdrawal behaviour.
- Investment switching behaviour.
- Campaign engagement.
- Web engagement.
- Insurance features.
- Activity frequency and recency.
- Other previously reviewed business features.

Do not introduce new business features without identifying them separately as recommendations.

Preserve NULL handling for unavailable data sources. Do not replace unavailable web engagement or VOC data with artificial zero values.

6. Independence from target labels

- Feature engineering should depend on the historical account snapshot population and as_of_date, not on target_churn.
- Do not introduce ATO-related target exclusions until business confirmation is received.
- Identify any feature modules that currently depend on ground-truth labels or temporal split assignments.
- Recommend how to minimise feature engineering rework if the churn definition changes.

7. Performance and scalability

Considering the historical dataset contains approximately 32.6 million account snapshot records:

- Review PySpark and Spark SQL implementation efficiency.
- Identify expensive joins, repeated source scans and unnecessary snapshot loops.
- Avoid collecting large datasets into driver memory or converting them into Pandas.
- Review incremental processing and persistent Delta table options.

8. Expected review output

Provide a consolidated review table containing:

- Module/file name
- Feature category
- Number of implemented features
- Multi-snapshot readiness
- Account-level grain compliance
- Point-in-time correctness
- Potential leakage
- Performance concerns
- Required changes
- Priority
- Readiness status: READY / NEEDS CHANGE / BLOCKED / NOT VERIFIED

Also provide a recommended implementation sequence and clearly identify which existing Python files require changes.

Distinguish confirmed code findings from assumptions and recommendations.

Strict restrictions:

- This is a read-only code review.
- Do not create or modify any files.
- Do not execute Python, SQL, notebooks or terminal commands.
- Do not run background processes or Databricks jobs.
- Do not create, overwrite or modify Databricks tables.
- Do not modify historical snapshot, target label or temporal splitting logic.
- Do not proceed with EDA or model training.

Provide the review findings and recommendations only.
