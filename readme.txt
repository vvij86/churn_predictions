The consolidated SQL feature dataset already contains the approved behavioural features, including rollover features.

I need the Python/XGBoost pipeline to use all approved predictive feature columns available in the consolidated feature dataset, instead of a manually restricted feature subset.

Do not add synthetic features.

Do not include identifiers, target fields, future information, or reporting-only output columns.

1. Inspect the actual dataset columns

After loading the feature dataset, print:

- total column count
- all column names
- data types

Then classify each column into:

1. Predictive model feature
2. Identifier/reference only
3. Target/outcome field
4. Reporting/output-only field
5. Excluded leakage/future field

Show the classification before training.

2. Include all approved predictive features

Automatically include all valid predictive feature columns from the consolidated dataset.

Do not manually restrict the model to only a small feature list.

This should include approved feature groups such as:

Account/profile

- account tenure
- member age
- member source
- benefit type/class
- super/pension indicators
- other approved account profile attributes

Contribution / money inflow

- contribution_count_12m
- contribution_amount_12m
- avg_contribution_transaction_amount_12m
- contribution_active_months_12m
- days_since_last_contribution
- recent_contribution_amount_90d
- prior_contribution_amount_90d
- contribution_decline_flag
- months_of_declining_contribution
- employer SG current/baseline/change/cessation features
- salary sacrifice current/baseline/change/cessation/increase features
- member voluntary contribution current/baseline/change/cessation/increase features

Rollover

Include all existing approved rollover features in the SQL output, especially:

- partial_rollover_count_12m
- partial_rollover_amount_12m
- days_since_last_partial_rollover
- recent_partial_rollover_count_90d
- recent_partial_rollover_amount_90d

If these columns exist in the dataset, they MUST be included in the XGBoost feature matrix unless there is a documented technical reason not to.

Also include any approved external rollover count features if they are genuine model features rather than output-only fields.

Helpline

Include approved helpline behavioural features such as:

- contact count
- inquiry count
- active days
- days since last contact
- recent 90-day activity
- approved inquiry/theme features

Workflow

Include approved member-driven workflow features.

Website

Include approved website engagement features where populated.

Campaign

Include approved campaign/event behavioural features currently in scope.

Investment

Include:

- investment option count
- direct investment flag
- approved investment switch features
- other approved investment behavioural features

Insurance

Include approved active cover / cover amount features.

Third party authority

Include approved authority flags/counts.

Other approved behavioural features

Include all other predictive columns already present in the consolidated feature dataset.

3. Explicitly exclude non-model fields

Exclude from model training:

- accountID / account_id
- memberID / memberNumber / member_id
- AsOfDate
- fundJoinDate
- fundID where used only for reporting/reference
- MonthKey
- ml_scoring_date
- exitDateRecorded
- target_churn from X
- any outcome-window fields
- churn_probability
- risk_band
- retention_category
- model_version
- primary_churn_driver
- additional_churn_drivers
- risk_trend
- risk_change
- previous_churn_probability
- scoring_run_timestamp
- data_quality_flag
- latest_rollover_destination_name
- latest_rollover_destination_type
- any post-AsOfDate/future fields
- any target leakage fields

Do not exclude a valid predictive feature just because it contains the word "rollover".

4. Verify rollover features specifically

After building X_train / model feature matrix, print whether each rollover feature is present.

For example:

"partial_rollover_count_12m -> FOUND / NOT FOUND"
"partial_rollover_amount_12m -> FOUND / NOT FOUND"
"days_since_last_partial_rollover -> FOUND / NOT FOUND"
"recent_partial_rollover_count_90d -> FOUND / NOT FOUND"
"recent_partial_rollover_amount_90d -> FOUND / NOT FOUND"

If any existing approved rollover feature is missing, fix the feature-selection logic before training.

5. Print final XGBoost feature list

Before model.fit(), print:

- number of model features
- complete final feature list

Also save it to:

"member_retention_xgboost_feature_list.txt"

6. Retrain XGBoost

Retrain XGBoost using the full approved predictive feature matrix.

Use the same:

- real-data sample
- target
- train/validation split
- preprocessing
- fixed risk thresholds

Do not change thresholds:

High >= 0.70
Medium >= 0.40 and < 0.70
Low < 0.40

7. Recalculate account-level SHAP

After retraining, recalculate account-level SHAP values using the full feature matrix.

For accounts with rollover activity, verify whether rollover features now appear among the top positive contributors.

Do not force rollover to be a driver.

It should appear only when its actual SHAP contribution is material.

8. Driver mapping

Map approved raw rollover features to business-friendly labels:

- partial_rollover_count_12m -> Partial rollover-out activity
- partial_rollover_amount_12m -> Partial rollover-out activity
- days_since_last_partial_rollover -> Recent partial rollover activity
- recent_partial_rollover_count_90d -> Recent partial rollover activity
- recent_partial_rollover_amount_90d -> Recent partial rollover activity

Avoid displaying multiple raw features from the same feature family as separate duplicate business drivers.

Group them into one meaningful business driver where appropriate.

9. Driver validation

For at least 10 rollover-positive accounts print:

- account_id
- churn_probability
- rollover feature values
- top 10 positive SHAP features
- primary_churn_driver
- additional_churn_drivers

Confirm whether rollover is:

- primary driver
- additional driver
- not significant

based on actual SHAP contribution.

10. Regenerate final outputs

After retraining and driver validation, regenerate:

- "member_retention_ml_scoring_output.csv"
- "member_retention_ml_scoring_sample_15.csv"
- "member_retention_ml_scoring_validation.md"

The 15-row sample should still aim for:

- 5 High
- 5 Medium
- 5 Low

where naturally available.

Also include several rows with real rollover activity if available.

11. Final validation summary

At the end show:

- total model feature count before and after this fix
- rollover features included
- XGBoost validation metrics
- risk-band distribution
- top primary driver distribution
- count of rollover-positive accounts
- count where rollover is primary driver
- count where rollover is additional driver
- count where rollover is not significant

Important:
Use all approved predictive features from the actual consolidated dataset. Do not manually omit rollover or other behavioural features without a documented reason.
