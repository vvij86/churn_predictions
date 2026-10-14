I want to continue FEATURE ENGINEERING PROTOTYPING for the MercerEdge churn model.

This is STEP 2.

IMPORTANT:
- Do NOT modify Step 1 SQL.
- Do NOT overwrite build_merceredge_feature_dataset_step1.sql.
- Create a separate new SQL file for Step 2.
- Do NOT use Databricks.
- Do NOT use Bronze views.
- Do NOT use PySpark.
- Work only with the approved MercerEdge UAT SQL Server tables.
- This is still prototype work before business confirmation.

Create this new file:

build_merceredge_feature_dataset_step2.sql

Use the current validated Step 1 output/query as the starting point:

build_merceredge_feature_dataset_step1.sql

The modelling grain must remain:

one row per account_id + as_of_date

Keep the existing:
- eligibility logic
- fundJoinDate historical existence rule
- AsOfDate logic
- death exclusion
- internal transfer exclusion
- target_churn logic
- retained_flag
- outcome-window logic

Do not change any approved Step 1 logic unless required to fix a clear technical issue.


STEP 2 SCOPE
------------

Implement only:

BEHAVIOURAL, TRANSACTION, ROLLOVER AND ENGAGEMENT FEATURES

Do not start:
- campaign features
- investment features
- insurance features
- model training
- categorical encoding / final preprocessing beyond what is required for validation


IN-SCOPE TABLES FOR STEP 2
--------------------------

Review only the relevant approved UAT tables from this list:

1. edgeSource.accountEngagementWorkflow
2. edgeSource.accountEngagementHelpline
3. edgeSource.accountEngagementWeb
4. edgeSource.accountMoneyInflow
5. edgeSource.accountNetMoneyFlow
6. edgeSource.accountRolloverPayment

You may use accountSummary only as the already established base/account reference.

Do not use pensionerData.


REFERENCE FILES
---------------

Use these as supporting references:

- build_merceredge_feature_dataset_step1.sql
- build_merceredge_base_historical_dataset.sql
- All_table_scripts.sql
- All_Other_tables_Not_explored.sql
- MercerEdge_ML_Churn_Driver_EDA_Phase2.xlsx
- MercerEdge_ML_Churn_Driver_EDA_Remaining_Tables_part2.xlsx
- MercerEdge_Churn_Candidate_Feature_List.xlsx, if available
- validate_candidate_churn_features.sql, if available
- historical_snapshot_profile_results.json, if available

Use the DDL and EDA files to confirm actual source column names.

Do not guess column names.


POINT-IN-TIME RULE
------------------

Every Step 2 feature must use only information available on or before @AsOfDate.

Do not use:
- events after @AsOfDate
- future outcome events
- exitDate as a predictive feature
- full rollover completion if it is part of the churn outcome
- account closure outcome information
- MEMBER_EXIT or other future churn indicators
- any post-AsOfDate transaction/payment/workflow activity

All event date filters must satisfy:

event_date <= @AsOfDate

and where relevant:

event_date >= @FeatureStartDate


FEATURE WINDOW
--------------

Use the existing feature window:

@FeatureStartDate -> @AsOfDate

Use the same agreed lookback period already defined in the prototype.

Where useful, derive:
- 12-month counts
- 12-month amounts
- recency
- recent 90-day activity
- previous 90-day activity
- trend / decline indicators

Do not invent windows unless already supported by the existing design.


FEATURE GROUP 1 – HELPLINE ENGAGEMENT
-------------------------------------

Review accountEngagementHelpline and derive useful account-level features such as:

- helpline_contact_count_12m
- helpline_contact_days_12m
- days_since_last_helpline_contact
- recent_helpline_contact_count_90d
- prior_helpline_contact_count_90d
- repeat_contact_flag or similar, if supported by source data

Use only events on or before @AsOfDate.


FEATURE GROUP 2 – WEB ENGAGEMENT
--------------------------------

Review accountEngagementWeb and derive useful features such as:

- web_activity_count_12m
- web_active_days_12m
- days_since_last_web_activity
- recent_web_activity_count_90d
- prior_web_activity_count_90d

Only create features supported by actual source columns.


FEATURE GROUP 3 – WORKFLOW / PROCESS ACTIVITY
---------------------------------------------

Review accountEngagementWorkflow.

Potential features may include:

- workflow_count_12m
- completed_workflow_count_12m
- open_workflow_count_12m
- days_since_last_workflow
- recent_workflow_count_90d
- prior_workflow_count_90d

IMPORTANT:
Workflow records that occur after churn/exit or clearly represent downstream operational processing must not be used as predictive features.

Flag high-leakage workflow types as:
- EXCLUDE
or
- REVIEW REQUIRED


FEATURE GROUP 4 – MONEY INFLOW
------------------------------

Review accountMoneyInflow.

Potential features may include:

- contribution_count_12m
- contribution_amount_12m
- avg_contribution_amount_12m
- contribution_active_days_12m
- days_since_last_contribution
- recent_contribution_amount_90d
- prior_contribution_amount_90d
- contribution_decline_flag

Only use actual historical inflow events up to @AsOfDate.


FEATURE GROUP 5 – NET MONEY FLOW
--------------------------------

Review accountNetMoneyFlow.

Potential features may include:

- net_money_flow_12m
- negative_net_flow_count_12m
- outflow_count_12m
- days_since_last_outflow
- recent_net_flow_90d
- prior_net_flow_90d
- net_flow_decline_flag

Use caution:
Do not use future churn/exit payments.

If a row cannot be clearly classified as pre-churn behaviour, mark it REVIEW REQUIRED.


FEATURE GROUP 6 – ROLLOVER / WITHDRAWAL BEHAVIOUR
-------------------------------------------------

Review accountRolloverPayment.

Potential features may include:

- rollover_count_12m
- rollover_amount_12m
- partial_rollover_count_12m
- partial_rollover_amount_12m
- days_since_last_rollover
- recent_rollover_count_90d
- recent_rollover_amount_90d

IMPORTANT:
Internal transfers are not churn.

Do not use internal-transfer events as churn indicators.

Do not use full rollover / closure payment events from the future outcome window as predictive features.

Partial rollover may be retained as a risk feature only where it occurs on or before @AsOfDate.

If full vs partial cannot be reliably distinguished from source data, classify the feature as REVIEW REQUIRED.


AGGREGATION RULE
----------------

All Step 2 source tables may contain multiple rows per account.

Aggregate them to account level before joining.

The final output must remain:

one row per account_id + as_of_date

Do not directly join raw event-level tables in a way that duplicates accounts.


VALIDATION REQUIRED
-------------------

For every feature group, validate:

1. Row count before Step 2 feature joins
2. Row count after Step 2 feature joins
3. Duplicate account_id + as_of_date count
4. NULL count and NULL percentage
5. MIN / MAX / AVG for numeric features
6. Distinct values for flags
7. Negative / impossible values
8. Event dates after @AsOfDate
9. Event dates before @FeatureStartDate
10. Leakage risk
11. Whether joins created duplicate accounts
12. Whether target_churn distribution remained unchanged
13. Whether Step 1 features remained unchanged
14. Whether the eligible modelling population remained unchanged


VERY IMPORTANT TARGET CHECK
---------------------------

Step 2 feature engineering must not alter:

- target_churn
- retained_flag
- is_eligible_for_modelling
- historical_eligibility_status
- death exclusion flags
- internal transfer exclusion flags

Validate before vs after counts for:

- total eligible rows
- target_churn = 1
- target_churn = 0
- target_churn IS NULL

These counts should remain unchanged unless there is a clear bug in the existing data logic.


FEATURE REVIEW OUTPUT
---------------------

For each Step 2 feature, produce:

- Feature Name
- Feature Category
- Simple Business Meaning
- Source Table
- Source Column(s)
- Calculation
- Feature Window
- Point-in-Time Status
- Leakage Risk
- Validation Result
- Recommendation

Allowed recommendations:

- INCLUDE
- REVIEW REQUIRED
- EXCLUDE


FINAL OUTPUT
------------

Create:

build_merceredge_feature_dataset_step2.sql

The final SQL should contain:

1. Step 1 dataset logic reused as the base
2. Step 2 behavioural / transaction / rollover / engagement aggregations
3. Account-level joins
4. Step 1 features retained
5. target_churn retained as label only
6. Validation queries
7. Final feature review summary

At the end, clearly report:

- SQL file created
- number of Step 2 features added
- INCLUDE features
- REVIEW REQUIRED features
- EXCLUDE features
- row count before Step 2
- row count after Step 2
- duplicate count
- target_churn count before and after
- any leakage issues found
- any business questions
- whether Step 2 is technically ready for review

Do not start Step 3 automatically.

Stop after Step 2 is generated and validated.
