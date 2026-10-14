Continue FEATURE ENGINEERING PROTOTYPING for the MercerEdge churn model.

This is STEP 4.

IMPORTANT:
- Do NOT modify Step 1, Step 2 or Step 3 SQL files.
- Do NOT overwrite:
  - build_merceredge_feature_dataset_step1.sql
  - build_merceredge_feature_dataset_step2.sql
  - build_merceredge_feature_dataset_step3.sql

Create a separate new SQL file:

build_merceredge_feature_dataset_step4.sql

Environment:
- MercerEdge UAT SQL Server only
- No Databricks
- No Bronze views
- No PySpark
- No model training
- Prototype only

Use Step 3 as the starting point:

build_merceredge_feature_dataset_step3.sql

The Step 4 SQL must be standalone and executable in a fresh SSMS window.
Do not depend on temporary tables created in another SQL file/session.

Rebuild/reuse the approved Step 3 baseline internally if required.

Preserve exactly:
- one row per account_id + as_of_date
- Step 1 features
- Step 2 features
- Step 3 features
- target_churn
- retained_flag
- eligibility logic
- historical_eligibility_status
- death exclusion
- internal-transfer exclusion
- AsOfDate / FeatureStartDate / Outcome window logic

Do not redesign any previously approved logic.


STEP 4 SCOPE
------------

Implement only:

INVESTMENT AND INSURANCE FEATURES

Use only these approved UAT tables:

1. edgeSource.accountInvestments
2. edgeSource.AccountInsuranceCurrent

Do not start:
- categorical encoding
- missing-value treatment across the entire dataset
- model training
- feature selection
- Step 5


REFERENCE FILES
---------------

Use:

- build_merceredge_feature_dataset_step3.sql
- build_merceredge_feature_dataset_step2.sql
- build_merceredge_feature_dataset_step1.sql
- build_merceredge_base_historical_dataset.sql
- All_table_scripts.sql
- All_Other_tables_Not_explored.sql
- MercerEdge_ML_Churn_Driver_EDA_Phase2.xlsx
- MercerEdge_ML_Churn_Driver_EDA_Remaining_Tables_part2.xlsx
- MercerEdge_Churn_Candidate_Feature_List.xlsx, if available
- validate_candidate_churn_features.sql, if available
- historical_snapshot_profile_results.json, if available

Use actual DDL/EDA column names.
Do not guess columns.


POINT-IN-TIME SAFETY
--------------------

This is critical.

Only use a feature if it can reasonably represent information available on or before @AsOfDate.

For tables with transaction/event/history dates:

use only rows where:

event/effective date >= @FeatureStartDate
AND event/effective date <= @AsOfDate

For current-state snapshot tables such as AccountInsuranceCurrent:

do NOT automatically assume the current value was historically true at @AsOfDate.

Classify fields as:

- POINT_IN_TIME_SAFE
- REVIEW REQUIRED
- EXCLUDE

depending on whether historical validity can be established.

Do not create historical values from current-state fields by assumption.


FEATURE GROUP 1 – INVESTMENT FEATURES
-------------------------------------

Review edgeSource.accountInvestments.

Create only features supported by actual source columns.

Potential features may include:

- investment_option_count
- distinct_investment_option_count
- investment_change_count_12m
- days_since_last_investment_change
- recent_investment_change_count_90d
- prior_investment_change_count_90d
- investment_value_total
- investment_allocation_count
- dominant_investment_option
- investment_diversification_indicator

If values or allocation percentages exist, consider:

- total investment value
- number of investment options
- maximum allocation percentage
- concentration / diversification indicators

Only include value/allocation fields if they are historically valid at @AsOfDate.

Do not use future investment changes.


FEATURE GROUP 2 – INSURANCE FEATURES
------------------------------------

Review edgeSource.AccountInsuranceCurrent.

Potential features may include:

- has_insurance_flag
- insurance_cover_type
- insurance_cover_count
- total_cover_amount
- premium_amount
- insurance_status
- days_since_insurance_start, if start date exists and is historically safe
- insurance_change / cancellation indicators, only if historical dates exist

IMPORTANT:

Because the table name is AccountInsuranceCurrent, treat it carefully.

If the table only represents today's/current insurance status and cannot reconstruct what the member's insurance looked like at the historical @AsOfDate:

- do not automatically mark those fields INCLUDE
- mark them REVIEW REQUIRED for historical modelling
- explain why

If effective/start/end dates allow reconstruction of historical status at @AsOfDate, use those dates explicitly.


AGGREGATION RULE
----------------

Both investment and insurance sources may contain multiple rows per account.

Aggregate to account level before joining.

Do not directly join raw records if that can duplicate the base population.

Final grain must remain:

one row per account_id + as_of_date


NULL HANDLING FOR STEP 4
------------------------

Do not perform full dataset-wide imputation yet.

For Step 4 only:

- retain genuine NULL where source information is unavailable
- do not automatically convert NULL to zero unless NULL clearly means "no activity/no product"
- document the interpretation

Examples:

No investment activity row may potentially mean 0 activity only if source semantics confirm this.

Missing current insurance data must not automatically be interpreted as no insurance without confirming source meaning.


VALIDATION REQUIRED
-------------------

Validate:

1. row_count_before_step4
2. row_count_after_step4
3. duplicate account_id + as_of_date count
4. Step 3 feature columns retained
5. target_churn counts before and after
6. retained counts before and after
7. eligible population unchanged
8. NULL count and NULL percentage per Step 4 feature
9. MIN / MAX / AVG for numeric features
10. distinct values for categorical/flag features
11. negative or impossible amounts
12. future-dated investment rows used in features
13. future-dated insurance records used in features
14. point-in-time safety per feature
15. leakage risk per feature
16. whether any join increased/decreased the account population


TARGET VALIDATION
-----------------

Do not change:

- target_churn
- retained_flag
- is_eligible_for_modelling
- historical_eligibility_status
- death exclusion
- internal-transfer exclusion

Validate that these remain unchanged:

row count
churn count
retained count
null target count


FEATURE REVIEW OUTPUT
---------------------

For each Step 4 feature return:

- Feature Name
- Feature Category
- Business Meaning
- Source Table
- Source Column(s)
- Calculation
- Feature Window / Historical Rule
- Point-in-Time Status
- Leakage Risk
- NULL Percentage
- Validation Result
- Recommendation
- Reason

Recommendation values:

- INCLUDE
- REVIEW REQUIRED
- EXCLUDE


SPECIAL REVIEW
--------------

Pay particular attention to:

1. Whether accountInvestments is historical/event-based or current-state.
2. Whether AccountInsuranceCurrent can reconstruct historical status at @AsOfDate.
3. Whether investment values represent values at the historical date or today's values.
4. Whether insurance cover/premium/status fields are historically valid.
5. Whether any fields may change after @AsOfDate and therefore create point-in-time leakage.

Do not mark uncertain current-state fields as INCLUDE merely because the SQL executes successfully.


FINAL OUTPUT
------------

Create:

build_merceredge_feature_dataset_step4.sql

At the end report:

- Step 4 feature count
- INCLUDE count
- REVIEW REQUIRED count
- EXCLUDE count
- row count before Step 4
- row count after Step 4
- duplicate count
- churn counts before/after
- retained counts before/after
- point-in-time safety result
- investment features added
- insurance features added
- current-state/historical-data limitations
- business questions
- whether Step 4 is technically ready

Do not start Step 5 automatically.

Stop after Step 4 is generated and validated.
