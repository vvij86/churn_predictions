Continue FEATURE ENGINEERING PROTOTYPING for the MercerEdge churn model.

This is STEP 5.

IMPORTANT:
- Do NOT modify Step 1, Step 2, Step 3 or Step 4 SQL files.
- Create a separate new SQL file:

build_merceredge_feature_dataset_step5.sql

Environment:
- MercerEdge UAT SQL Server only
- No Databricks
- No Bronze views
- No PySpark
- No model training
- No train/validation/test split

Use Step 4 as the starting point:

build_merceredge_feature_dataset_step4.sql

The Step 5 SQL must be standalone and executable in a fresh SSMS window.
Do not depend on temporary tables created in another SQL file/session.

Preserve:
- one row per account_id + as_of_date
- all approved Step 1 features
- all approved Step 2 features
- all approved Step 3 features
- all approved Step 4 features
- target_churn
- retained_flag
- eligibility logic
- historical_eligibility_status
- death exclusion
- internal transfer exclusion
- AsOfDate / FeatureStartDate / Outcome window logic

Do not redesign the target or previously approved feature definitions.


STEP 5 SCOPE
------------

Perform:

FINAL FEATURE CONSOLIDATION
+
MISSING VALUE TREATMENT
+
CATEGORICAL FEATURE PREPARATION

Do not start model training.


1. CONSOLIDATE FEATURES
-----------------------

Build one consolidated Step 5 dataset containing all approved Step 1–4 features.

Keep:
- INCLUDE features
- REVIEW REQUIRED features, but clearly flag them

Do not silently use EXCLUDE features as predictive inputs.

Keep target_churn only as the ML label.


2. MISSING VALUE HANDLING
-------------------------

Review missing values feature by feature.

Do NOT apply one generic rule to all NULLs.

Classify NULL meaning as one of:

A. NO_ACTIVITY
Example:
No transaction/event rows may genuinely mean the member had no activity.

Only where source semantics support this:
- count fields may be converted to 0
- amount fields may be converted to 0 if absence truly means no amount/activity

B. UNKNOWN_OR_MISSING
Keep as NULL or prepare a missing indicator.

C. SOURCE_NOT_AVAILABLE_IN_UAT
Keep as NULL.
Do NOT convert to 0.

IMPORTANT UAT RULE:

edgeSource.accountEngagementWeb is known to be empty/not populated in UAT.

Therefore all web-derived features must:
- remain in scope
- remain NULL in the UAT prototype
- NOT be converted to 0
- NOT be dropped just because they are 100% NULL in UAT
- be documented as:
  "UAT source not populated; revalidate against Prod/Databricks source"

NULL for web features means:
"data unavailable in UAT"

It does NOT mean:
"member had zero web activity"


3. INVESTMENT / INSURANCE NULLS
-------------------------------

Do not automatically convert investment or insurance NULLs to zero.

For investment features:
- determine whether no source row genuinely means no investment activity
- otherwise retain NULL

For insurance:
- because AccountInsuranceCurrent may represent current-state data,
  retain NULL unless source semantics clearly prove "no insurance"

Do not infer no insurance from missing data without evidence.


4. CATEGORICAL FEATURES
-----------------------

Review all categorical features from Steps 1–4.

Examples may include:
- member_source
- benefit_type
- benefit_class
- database_code
- investment categories
- insurance categories
- campaign/event categories

Do NOT one-hot encode them in SQL unless there is a strong reason.

For this prototype:
- retain clean raw categorical values
- standardize obvious blank/NULL representations
- optionally create an explicit 'UNKNOWN' category only where appropriate
- document high-cardinality categorical fields
- document categories with very low frequency

Do not invent category groupings without business support.


5. CONSTANT / LOW-VARIANCE FEATURES
-----------------------------------

Identify:

- all-NULL features
- constant features
- near-constant features
- extremely sparse features

Do NOT automatically remove web features only because they are all NULL in UAT.

For all other all-NULL or constant features:
classify as REVIEW REQUIRED or EXCLUDE depending on source/business meaning.


6. REVIEW REQUIRED FEATURES
---------------------------

Keep a clear list of all REVIEW REQUIRED features.

Examples may include:
- current-state insurance features without historical proof
- historically uncertain investment fields
- campaign/event types requiring business confirmation
- web features not testable in UAT

Do not silently promote these to INCLUDE.


7. TARGET / LEAKAGE SAFETY
--------------------------

target_churn must remain label-only.

Ensure none of these are predictive inputs:
- target_churn
- retained_flag
- future outcome indicators
- MEMBER_EXIT
- exitDate
- future rollover/closure events
- death outcome indicators
- any post-AsOfDate data

Validate point-in-time safety again.


8. VALIDATION REQUIRED
----------------------

Validate:

- row_count_before_step5
- row_count_after_step5
- duplicate account_id + as_of_date count
- churn count before/after
- retained count before/after
- null target count
- eligible population count
- feature count before/after consolidation
- INCLUDE count
- REVIEW REQUIRED count
- EXCLUDE count

For every feature report:

- Feature Name
- Feature Category
- Data Type
- NULL Count
- NULL Percentage
- Distinct Count
- Constant / Low Variance Flag
- Missing Value Meaning
- Missing Value Treatment
- Point-in-Time Status
- Leakage Risk
- Recommendation
- Reason


9. SPECIAL WEB FEATURE VALIDATION
---------------------------------

Explicitly identify all features derived from:

edgeSource.accountEngagementWeb

For those features return:

source_status = 'UAT_NOT_POPULATED'

missing_value_treatment = 'KEEP_NULL_IN_UAT'

recommendation = 'INCLUDE_PENDING_PROD_VALIDATION'

Do not convert these NULLs to zero.


10. FINAL STEP 5 OUTPUT
-----------------------

Create:

build_merceredge_feature_dataset_step5.sql

At the end report:

- row count before Step 5
- row count after Step 5
- duplicate count
- churn/retained counts before and after
- total feature count
- INCLUDE count
- REVIEW REQUIRED count
- EXCLUDE count
- list of features converted from NULL to 0 and why
- list of features where NULL remains NULL and why
- categorical fields requiring later encoding
- web features retained but unavailable in UAT
- business questions
- whether Step 5 is technically ready

Do NOT start Step 6 automatically.

Stop after Step 5 is generated and validated.
