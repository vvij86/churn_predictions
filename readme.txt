Please fix build_merceredge_feature_dataset_step3.sql.

Current error:

"Step 2 dataset #step2_feature_dataset is not available"
"Invalid object name '#step2_feature_dataset'"

Reason:
#step2_feature_dataset is a local SQL Server temporary table and Step 3 is being executed independently in another SSMS session/tab.

I want Step 3 SQL to be standalone and executable independently.

Requirements:

1. Do NOT modify:
   - build_merceredge_feature_dataset_step1.sql
   - build_merceredge_feature_dataset_step2.sql

2. Modify only:
   build_merceredge_feature_dataset_step3.sql

3. Do NOT require #step2_feature_dataset to already exist.

4. Reuse/include the approved Step 2 dataset-building logic inside Step 3 so that Step 3 can first recreate the required Step 2 baseline and then add the Step 3 campaign/event features.

5. Preserve exactly:
   - Step 1 features
   - Step 2 features
   - target_churn
   - retained_flag
   - eligibility logic
   - death exclusion
   - internal-transfer exclusion
   - AsOfDate / FeatureStartDate / Outcome window logic
   - one row per account_id + as_of_date

6. Do not redesign or change Step 1/Step 2 feature definitions.

7. Step 3 should then add only the approved campaign/event features.

8. The complete build_merceredge_feature_dataset_step3.sql must run by itself in a fresh SSMS query window.

9. Add validation confirming:
   - Step 2 baseline row count
   - Step 3 final row count
   - duplicate account_id + as_of_date = 0
   - target_churn counts unchanged
   - Step 1 and Step 2 features retained

10. Do not start Step 4.

After updating, clearly confirm that Step 3 no longer depends on a temp table created by another SQL file/session.
