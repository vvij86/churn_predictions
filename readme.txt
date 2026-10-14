I am currently doing FEATURE ENGINEERING PROTOTYPING in the MercerEdge UAT SQL Server environment.

IMPORTANT:
- Do NOT use Databricks.
- Do NOT use Bronze views.
- Do NOT use PySpark.
- Do NOT create notebooks.
- Work only with the existing 15 approved MercerEdge UAT source tables listed below.
- This is a prototype dataset query only.
- Once business confirms the feature logic, I will later convert the approved logic to Databricks views / PySpark.

Use the existing base historical dataset SQL as the starting point:

build_merceredge_base_historical_dataset.sql

The modelling grain must remain:

one row per account_id + as_of_date

Do not change:
- churn target definition
- eligibility rules
- death exclusion
- internal transfer exclusion
- AsOfDate / outcome window logic


IN-SCOPE UAT TABLES – 15 TABLES ONLY
------------------------------------

1. merceredge.edgeSource.accountSummary

2. merceredge.edgeSource.accountEngagementWorkflow

3. merceredge.edgeSource.accountEngagementHelpline

4. merceredge.edgeSource.accountEngagementWeb

5. merceredge.edgeSource.AccountInsuranceCurrent

6. merceredge.edgeSource.accountInvestments

7. merceredge.edgeSource.accountMoneyInflow

8. merceredge.edgeSource.accountNetMoneyFlow

9. merceredge.edgeSource.accountRolloverPayment

10. merceredge.edgeSource.campaignEventDetails

11. merceredge.edgeSource.campaignEvents

12. merceredge.edgeSource.customerMapping

13. merceredge.edgeSource.customerSummary

14. merceredge.edgeSource.thirdPartyAuthority

15. merceredge.tableau.fundListSource


EXCLUDED / NOT IN SCOPE
-----------------------

Do not use:

- edgePortalSource.pensionerData
- edgeSource.campaign
- edgeSource.campaignAccountMapping

Business has confirmed pensionerData is not required.

The current prototype scope is only the 15 tables listed above.


REFERENCE FILES
---------------

Use the following files as supporting references:

1. build_merceredge_base_historical_dataset.sql
   - Current validated base historical dataset query
   - Use this as the starting point
   - Do not change the already agreed target / eligibility / exclusion logic unnecessarily

2. All_table_scripts.sql
   - DDL / CREATE TABLE scripts for the original explored MercerEdge tables
   - Use this to confirm actual table and column names

3. All_Other_tables_Not_explored.sql
   - DDL / CREATE TABLE scripts for additional MercerEdge tables
   - Use only as a schema reference where one of the 15 in-scope tables appears

4. MercerEdge_ML_Churn_Driver_EDA_Phase2.xlsx
   - Existing EDA for the original explored tables
   - Use this to understand column availability, nulls, values, and ML relevance

5. MercerEdge_ML_Churn_Driver_EDA_Remaining_Tables_part2.xlsx
   - EDA for the additional explored tables
   - Use only for the 15 approved in-scope tables

6. MercerEdge_Churn_Candidate_Feature_List.xlsx
   - Candidate churn feature inventory, if available
   - Use as a feature-identification reference only
   - Validate all source columns before using them

7. validate_candidate_churn_features.sql
   - Existing read-only profiling / validation queries, if available
   - Reuse findings where relevant

8. historical_snapshot_profile_results.json
   - Profiling evidence showing which sources are historical event sources,
     partial point-in-time sources, current/latest sources, etc.
   - Use this when deciding whether a field is historically safe

9. profile_historical_snapshot_sources.py
   - Profiling script used to validate historical source behaviour, if available
   - Reference only; do not modify unless explicitly required


STEP 1 ONLY
-----------

Implement only:

ACCOUNT, TENURE AND PRODUCT FEATURES

Do not start behavioural, transaction, rollover, campaign, investment or insurance feature engineering yet unless a field is required purely as a reference for Step 1.


CANDIDATE FEATURE AREAS TO REVIEW
---------------------------------

Review only historically defensible account-level features such as:

- account tenure
- months since fund join / commencement
- member source
- super indicator
- pension indicator
- fund-related information
- account/product type where historically safe
- stable product/reference attributes
- age / age band only if historically defensible
- other stable account profile fields already identified during EDA


SOURCE SELECTION RULE
---------------------

For every candidate feature:

1. Identify the actual source table.
2. Identify the actual source column.
3. Confirm the column exists using the DDL files.
4. Check the EDA/profile results.
5. Confirm whether the field is historically safe as of @AsOfDate.
6. Do not guess column names.
7. Do not invent business definitions.


POINT-IN-TIME RULE
------------------

Every predictive feature must represent information available on or before @AsOfDate.

Do not use:

- exitDate as a predictive feature
- future churn / outcome fields
- MEMBER_EXIT
- future rollover / withdrawal completion
- future payment events
- current/latest mutable fields if they cannot be reconstructed historically
- any field that directly reveals churn

Current/latest accountSummary or customerSummary fields must only be used where they are defensibly static/reference fields.

If a field cannot be proven historically safe, classify it as:

REVIEW REQUIRED

rather than using it automatically.


TENURE RULE
-----------

If tenure is derived, calculate it relative to @AsOfDate.

Do NOT use GETDATE() or today's date.

Example:

tenure_months =
months between fundJoinDate / valid commencement date and @AsOfDate

If an account has less than 12 months of history, keep it unless the existing eligibility logic explicitly excludes it.

Do not artificially require 12 months tenure unless business confirms that rule.


DELIVERABLE
-----------

Create a new SQL file:

build_merceredge_feature_dataset_step1.sql

The SQL should:

1. Reuse the existing base historical dataset logic.
2. Add only Step 1 account / tenure / product features.
3. Preserve:
   one row per account_id + as_of_date
4. Keep target creation separate from predictive features.
5. Use LEFT JOINs / aggregation carefully so joins do not duplicate accounts.
6. Add clear comments for every engineered feature.


For every engineered feature, document:

- Feature Name
- Simple Business Meaning
- Source Table
- Source Column(s)
- Calculation / derivation
- Why it may help predict churn
- Point-in-time safe? Yes / No / Review
- Recommendation: INCLUDE / REVIEW REQUIRED / EXCLUDE


VALIDATION REQUIRED
-------------------

At the end of the SQL file, add read-only validation queries.

Validate:

1. Total row count before feature engineering
2. Total row count after feature engineering
3. Duplicate account_id + as_of_date count
4. NULL count for each new feature
5. NULL percentage where useful
6. Invalid negative tenure
7. Future fundJoinDate / commencement date relative to @AsOfDate
8. MIN / MAX / AVG for numeric features
9. Distinct values and counts for categorical features
10. Suspicious / unrealistic values
11. Point-in-time violations
12. Leakage concerns
13. Whether the final grain remains one row per account_id + as_of_date


VALIDATION RESULT FORMAT
------------------------

At the end, produce a simple summary:

Feature Name
Source Table
Source Column
Validation Result
Key Observation
Recommendation

Validation Result values:

- PASS
- REVIEW REQUIRED
- FAIL


EXECUTION / QUERY VALIDATION
----------------------------

After generating the SQL:

1. Run the read-only validation queries against the MercerEdge UAT database.
2. Confirm all referenced tables and columns exist.
3. Fix syntax errors.
4. Fix incorrect column names using DDL as the source of truth.
5. Confirm the query executes successfully.
6. Do not perform INSERT / UPDATE / DELETE / ALTER / DROP on permanent source objects.
7. Temporary tables are allowed if required for the prototype.
8. Do not modify the existing source tables.


STOP CONDITION
--------------

Stop after Step 1 is completed and validated.

Do NOT continue to:

- behavioural features
- transaction features
- rollover features
- campaign features
- investment features
- insurance features
- model training

At the end, show me:

- SQL file created
- total Step 1 features added
- features marked INCLUDE
- features marked REVIEW REQUIRED
- features excluded
- validation issues found
- business questions that still need confirmation
