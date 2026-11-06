The current XGBoost scoring output is suspicious because almost every account has:

"primary_churn_driver = Account tenure"

and:

"additional_churn_drivers = No additional drivers"

However, several scored accounts clearly have behavioural values such as:

- external_rollover_flag = Yes
- external_rollover_count_12m > 0
- latest_rollover_destination_type populated
- latest_rollover_destination_name populated
- contribution / engagement / investment-switch features

Please validate the account-level churn-driver generation before accepting this output.

1. Confirm that churn drivers are being generated from ACCOUNT-LEVEL SHAP values from the selected XGBoost model, not global feature importance.

2. For at least 10 accounts, print the top 10 positive SHAP contributors with:
   
   - raw feature name
   - actual feature value
   - SHAP contribution
   - mapped business driver name

3. Specifically check accounts where:
   
   - external_rollover_flag = Yes
   - external_rollover_count_12m > 0

Show whether rollover-related features have positive SHAP contributions.

4. Confirm that these feature groups are included in the explainability input where available:
   
   - contribution decline / cessation
   - days since last contribution
   - partial / external rollover
   - rollover count 6M / 12M
   - helpline activity
   - workflow activity
   - web activity
   - investment switch
   - retirement / pension signals
   - account tenure

5. Check whether the additional-driver significance threshold is too restrictive.

Do not force a fixed number of drivers, but retain other strategically meaningful positive contributors when their contribution is material.

6. Check the business-name mapping. Ensure rollover raw features map to labels such as:

"External rollover activity"

or

"Partial rollover-out activity"

rather than being dropped.

7. Print the distribution of primary_churn_driver across the full scoring output.

If more than an unusually high proportion of accounts have "Account tenure", investigate why and report:

- percentage with Account tenure as primary
- second/third most common primary drivers
- whether tenure genuinely dominates SHAP values or whether this is a driver-selection/mapping bug

8. Regenerate:
   - primary_churn_driver
   - additional_churn_drivers
   - driver_count

only after the validation is complete.

Do not artificially promote rollover as a driver merely because rollover fields are populated. The driver must be supported by the account-level model contribution.
