Review and correct the existing Step 1 prototype SQL:

build_merceredge_feature_dataset_step1.sql

Context:
- This is still only a MercerEdge UAT SQL Server prototype.
- Do NOT use Databricks.
- Do NOT use Bronze views.
- Do NOT use PySpark.
- Do NOT create notebooks.
- Work only with the existing approved UAT source tables and existing SQL prototype.
- Do not start Step 2 behavioural feature engineering yet.

IMPORTANT HISTORICAL SNAPSHOT RULE
----------------------------------

For this prototype, fundJoinDate is the agreed historical account-existence anchor.

Use:

fundJoinDate <= @AsOfDate

to determine whether an account existed at a historical snapshot.

Interpretation:

Example 1:
fundJoinDate = 2023-08-15
AsOfDate     = 2024-03-31

The account existed by the AsOfDate and can be considered for modelling, subject to the other eligibility rules.

Example 2:
fundJoinDate = 2024-06-01
AsOfDate     = 2024-03-31

The account did not exist yet at that historical snapshot and must not be eligible for modelling for that AsOfDate.

If fundJoinDate is NULL:
- retain the existing conservative handling unless there is another approved source proving the account did not exist
- clearly flag/document this assumption
- do not silently treat NULL fundJoinDate as confirmed historical existence


AS-OF DATE RULE
---------------

@AsOfDate is the manually supplied historical prediction cutoff.

It is NOT derived from reportingDate or fundJoinDate.

fundJoinDate is only used to check whether the account existed by @AsOfDate.

Example:

@AsOfDate = '2024-03-31'

FeatureStartDate should remain derived from the agreed lookback period.

OutcomeStartDate should remain @AsOfDate + 1 day.

OutcomeEndDate should remain based on the agreed 3-month outcome window.


DO NOT USE REPORTINGDATE AS THE HISTORICAL EXISTENCE ANCHOR
-----------------------------------------------------------

Previous profiling showed that edgeSource.accountSummary should not automatically be treated as a reliable historical snapshot series.

Therefore:

- Do not use accountSummary.reportingDate to determine whether the account existed at @AsOfDate.
- Do not treat reportingDate <= @AsOfDate plus ROW_NUMBER ranking as proof that accountSummary contains the true historical profile state.
- Do not create a pseudo-historical account snapshot from accountSummary unless the source profiling genuinely supports that interpretation.

Review the current block:

"Latest accountSummary snapshot as of the as-of date"

and determine whether it is actually needed.

If accountSummary is effectively one row per account/current-state data, simplify the logic rather than ranking it by reportingDate for historical reconstruction.


STEP 1 SCOPE
------------

Only review and correct:

ACCOUNT / TENURE / PRODUCT FEATURES

Current candidate features include:

- account_tenure_months
- account_tenure_years
- member_age_years
- member_source
- is_super_flag
- is_pension_flag
- benefit_type
- benefit_class
- database_code
- fund_active_flag
- fund_portal_enabled_flag
- has_active_third_party_authority_flag

Do NOT add:
- behavioural features
- transaction features
- rollover features
- campaign features
- investment features
- insurance features
- future churn outcome fields as predictive features


TENURE LOGIC
------------

Tenure must be calculated relative to @AsOfDate.

Use:

fundJoinDate -> @AsOfDate

Do NOT use GETDATE() or today's date.

Rules:

- fundJoinDate <= @AsOfDate:
  tenure can be calculated.

- fundJoinDate > @AsOfDate:
  account was not yet present at that snapshot.
  tenure must not be calculated as a valid feature.
  account must not be eligible for modelling for that snapshot.

- fundJoinDate IS NULL:
  tenure should remain NULL.
  document the historical-existence assumption separately.

Check both:

account_tenure_months
account_tenure_years


REVIEW CURRENT ELIGIBILITY LOGIC
--------------------------------

Confirm that:

1. Account must have existed by @AsOfDate.
2. Account must not have exited on or before @AsOfDate.
3. Account must not be deceased on or before @AsOfDate.
4. Internal-transfer and future churn outcome logic remain separate.
5. Accounts with fundJoinDate > @AsOfDate are not eligible.
6. Final modelling grain remains:
   one row per account_id + as_of_date.

Do not change the already agreed churn target definition unless a clear defect is found.


REASSESS ACCOUNT SUMMARY FEATURES
---------------------------------

For every Step 1 field sourced from edgeSource.accountSummary, reassess whether it is historically defensible.

Review:

- fundJoinDate
- dateOfBirth
- memberSource
- isSuperFlag
- isPensionFlag
- benefitType
- benefitClass
- databaseCode
- any other Step 1 profile field

For each feature classify as:

1. HISTORICALLY SAFE / STATIC
2. REFERENCE ONLY
3. REVIEW REQUIRED
4. EXCLUDE

Do not mark something historically safe merely because the column exists.

Guidance:

fundJoinDate:
- generally stable and used for historical existence / tenure.

dateOfBirth:
- generally stable and can support age derived relative to @AsOfDate.

memberSource:
- review whether it is stable enough historically.

isSuperFlag / isPensionFlag:
- confirm whether these are static or could change over time.

benefitType / benefitClass:
- review carefully because these may represent mutable product/account state.

databaseCode:
- likely reference/stable identifier, but validate.

If historical safety cannot be demonstrated, change the recommendation to REVIEW REQUIRED rather than INCLUDE.


MEMBER AGE
----------

member_age_years must be calculated from:

dateOfBirth -> @AsOfDate

Do not use currentAge or currentAgeBand as the preferred historical feature unless their historical validity is proven.

Prefer deriving age from static dateOfBirth.

Check:
- negative ages
- unrealistic ages
- future DOB
- NULL DOB


FUND REFERENCE FEATURES
-----------------------

Review:

fund_active_flag
fund_portal_enabled_flag

Confirm:
- source = tableau.fundListSource
- join does not duplicate account rows
- whether these are static/reference attributes or current mutable statuses

If the source does not provide historical state as of @AsOfDate, do not automatically mark these as point-in-time safe.

Classify appropriately:
- INCLUDE only if defensible
- otherwise REVIEW REQUIRED or REFERENCE ONLY


THIRD PARTY AUTHORITY FEATURE
-----------------------------

Keep:

has_active_third_party_authority_flag

as REVIEW REQUIRED unless there is strong evidence it is suitable as a churn predictor.

Reason:
It represents a relationship/process status and may not be a simple static profile/product attribute.

Validate its active-as-of-date logic using:
- dateAuthorityRequested <= @AsOfDate
- terminationDate > @AsOfDate OR terminationDate IS NULL

Do not use future status information.


VALIDATION REQUIRED
-------------------

Re-run and validate the corrected Step 1 query.

Validation must include:

1. Total row count before feature engineering.
2. Total row count after feature engineering.
3. Duplicate account_id + as_of_date count.
4. Count of accounts where fundJoinDate > @AsOfDate.
5. Of those future-fundJoinDate accounts:
   - total count
   - eligible count
   - ineligible count
6. Confirm eligible count must be 0 for:
   fundJoinDate > @AsOfDate
7. Count of NULL fundJoinDate.
8. Tenure NULL count.
9. Negative tenure count.
10. Min / max / avg tenure.
11. Future dateOfBirth count.
12. Invalid / unrealistic age count.
13. Null percentages for every Step 1 feature.
14. Distinct distributions for categorical features.
15. Point-in-time safety assessment.
16. Leakage assessment.
17. Confirmation that one row per account_id + as_of_date is preserved.


IMPORTANT CHECK FOR THE PREVIOUS RESULT
---------------------------------------

The previous validation showed a large number of rows with:

fundJoinDate > @AsOfDate

Investigate this explicitly.

Explain:

- Why these rows remain in the overall account universe.
- Whether they are correctly marked as:
  historical_eligibility_status = 'future_commencement'
- Whether:
  is_eligible_for_modelling = 0
- Whether they are excluded from the final eligible modelling population.

It is acceptable for such accounts to exist in an intermediate/account-universe dataset for validation.

It is NOT acceptable for them to be eligible training rows for that historical AsOfDate.


VALIDATION SUMMARY OUTPUT
-------------------------

Produce a final summary table with:

Feature Name
Source Table
Source Column
Business Meaning
Point-in-Time Status
Validation Result
Recommendation
Reason

Allowed Point-in-Time Status values:

- SAFE
- REFERENCE ONLY
- REVIEW REQUIRED
- NOT SAFE

Allowed Validation Result values:

- PASS
- REVIEW REQUIRED
- FAIL

Allowed Recommendation values:

- INCLUDE
- REVIEW REQUIRED
- EXCLUDE


FINAL OUTPUT
------------

Update:

build_merceredge_feature_dataset_step1.sql

At the end, clearly report:

1. Whether the query executed successfully.
2. Total rows before and after feature engineering.
3. Duplicate count.
4. Future fundJoinDate count.
5. Whether any future-join account is incorrectly eligible.
6. Final INCLUDE feature list.
7. Final REVIEW REQUIRED feature list.
8. Final EXCLUDE feature list.
9. Any remaining business questions.
10. Whether Step 1 is technically ready to proceed to Step 2.

Do not start Step 2 automatically.

Stop after reviewing, correcting and validating Step 1.
