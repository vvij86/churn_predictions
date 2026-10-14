Continue FEATURE ENGINEERING PROTOTYPING for the MercerEdge churn model.

This is STEP 3.

IMPORTANT:
- Do NOT modify Step 1 or Step 2 SQL files.
- Do NOT overwrite:
  - build_merceredge_feature_dataset_step1.sql
  - build_merceredge_feature_dataset_step2.sql
- Create a separate new SQL file:
  build_merceredge_feature_dataset_step3.sql

Environment:
- MercerEdge UAT SQL Server only
- No Databricks
- No Bronze views
- No PySpark
- No notebooks
- Prototype only before business confirmation

Use Step 2 as the starting point:

build_merceredge_feature_dataset_step2.sql

Preserve:
- one row per account_id + as_of_date
- eligibility logic
- fundJoinDate historical existence rule
- target_churn logic
- retained_flag
- death exclusion
- internal-transfer exclusion
- AsOfDate / FeatureStartDate / outcome-window logic
- all Step 1 and Step 2 features unchanged


STEP 3 SCOPE
------------

Implement only:

CAMPAIGN / EVENT FEATURES

Use these approved UAT tables:

1. edgeSource.campaignEventDetails
2. edgeSource.campaignEvents

Do not use:
- campaign
- campaignAccountMapping
- pensionerData

unless explicitly requested later.


REFERENCE FILES
---------------

Use:

- build_merceredge_feature_dataset_step2.sql
- build_merceredge_feature_dataset_step1.sql
- build_merceredge_base_historical_dataset.sql
- All_table_scripts.sql
- All_Other_tables_Not_explored.sql
- MercerEdge_ML_Churn_Driver_EDA_Phase2.xlsx
- MercerEdge_ML_Churn_Driver_EDA_Remaining_Tables_part2.xlsx
- MercerEdge_Churn_Candidate_Feature_List.xlsx, if available
- validate_candidate_churn_features.sql, if available

Confirm actual table/column names from DDL.
Do not guess columns.


POINT-IN-TIME RULE
------------------

Use only campaign/event activity available on or before @AsOfDate.

Every source event used as a feature must satisfy:

eventDate >= @FeatureStartDate
AND eventDate <= @AsOfDate

Do not use any future event after @AsOfDate.


LEAKAGE RULE
------------

Review event types carefully.

Known high-risk / outcome-type events must NOT be used as predictive features.

Examples include:
- MEMBER_EXIT
- full rollover / final exit completion
- account closure outcome
- any event that directly confirms churn
- any event occurring in the future outcome window

If an event type appears to represent churn or post-churn processing:
mark it EXCLUDE.

If business meaning is unclear:
mark it REVIEW REQUIRED.


SAFE EVENT TYPES
----------------

Review historical pre-AsOfDate events such as:

- CONTACT_UPDATE
- INVESTMENT_CHANGE
- FINANCIAL_ADVICE
- HELP_DESK_CALL
- INSURANCE_OPT_IN
- NOMINATED_BENEFICIARY
- OUTBOUND_CALL
- POST_TAX_CONTRIBUTION
- ROLLIN

Only include them if:
- they exist in source data
- they occur on/before @AsOfDate
- they are not outcome leakage
- their business meaning is suitable for churn prediction


POTENTIAL FEATURE TYPES
-----------------------

Create account-level features only where supported by actual data.

Examples:

- campaign_event_count_12m
- distinct_campaign_event_type_count_12m
- days_since_last_campaign_event
- recent_campaign_event_count_90d
- prior_campaign_event_count_90d

Specific behavioural event counts may include:

- contact_update_count_12m
- investment_change_count_12m
- financial_advice_count_12m
- help_desk_event_count_12m
- outbound_call_count_12m
- rollin_event_count_12m

If eventAmount is meaningful and safe:
- total_event_amount_12m
- average_event_amount_12m

Do not create features merely because a column exists.


AGGREGATION RULE
----------------

campaignEventDetails may contain multiple rows per account.

Aggregate to:

one row per account_id

before joining to Step 2.

Final grain must remain:

one row per account_id + as_of_date


EVENT LOOKUP RULE
-----------------

Use campaignEvents to map:

eventID -> eventName

Validate that the mapping is correct.

Do not assume campaignID and eventID are the same.


VALIDATION REQUIRED
-------------------

Validate:

1. Row count before Step 3
2. Row count after Step 3
3. Duplicate account_id + as_of_date count
4. target_churn distribution before vs after
5. Step 1 / Step 2 feature columns remain unchanged
6. Event rows before FeatureStartDate
7. Event rows after AsOfDate
8. Future event rows accidentally included in features
   - must be 0
9. Count of MEMBER_EXIT events
10. Confirm MEMBER_EXIT is excluded from predictive features
11. Count of each included event type
12. NULL percentage per new feature
13. MIN / MAX / AVG for numeric features
14. Leakage assessment
15. Point-in-time safety


FEATURE CLASSIFICATION
----------------------

For each Step 3 feature return:

- Feature Name
- Simple Business Meaning
- Source Table
- Source Column(s)
- Event Type
- Calculation
- Feature Window
- Point-in-Time Status
- Leakage Risk
- Validation Result
- Recommendation
- Reason

Recommendation values:

- INCLUDE
- REVIEW REQUIRED
- EXCLUDE


VERY IMPORTANT
--------------

Do not change:
- target_churn
- retained_flag
- is_eligible_for_modelling
- historical_eligibility_status
- death exclusion
- internal transfer exclusion

target_churn must remain a label only.


FINAL OUTPUT
------------

Create:

build_merceredge_feature_dataset_step3.sql

At the end report:

- Step 3 feature count
- INCLUDE count
- REVIEW REQUIRED count
- EXCLUDE count
- row count before and after
- duplicate count
- churn/retained counts before and after
- leakage events found
- excluded event types
- business questions
- whether Step 3 is technically ready

Do not start Step 4 automatically.

Stop after Step 3 is generated and validated.
