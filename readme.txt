The current XGBoost output contains accounts where:

- "external_rollover_flag = Yes"
- "external_rollover_count_12m > 0"
- rollover destination fields are populated

but the generated "primary_churn_driver" is often something else such as Campaign activity, Member service activity, Account tenure, etc.

I need to verify whether external rollover features are actually being considered correctly in the account-level churn-driver logic.

Please do the following.

1. Confirm rollover features are in the XGBoost feature matrix

Print whether the following fields, or their actual equivalent feature names, are included in model training/scoring:

- external_rollover_flag
- external_rollover_count_12m
- external_rollover_count_6m
- partial_rollover_count_12m
- partial_rollover_amount_12m
- days_since_last_partial_rollover
- recent_partial_rollover_count_90d
- recent_partial_rollover_amount_90d

Use the actual feature names present in the dataset.

If any rollover fields are output-only and not model features, state that clearly.

2. Validate account-level SHAP values

For accounts where:

"external_rollover_flag = Yes"

and/or:

"external_rollover_count_12m > 0"

calculate ACCOUNT-LEVEL SHAP values from the selected XGBoost model.

Do not use global feature importance for this check.

For at least 15 such accounts, print:

- account_id
- churn_probability
- risk_band
- external_rollover_flag
- external_rollover_count_12m
- external_rollover_count_6m
- latest_rollover_destination_type
- latest_rollover_destination_name
- rollover-related feature name
- actual rollover feature value
- rollover SHAP contribution
- rollover SHAP rank among all positive contributors
- current primary_churn_driver
- current additional_churn_drivers

3. Print top positive SHAP contributors

For the same accounts print the top 10 positive SHAP contributors:

- raw feature name
- actual feature value
- SHAP value
- mapped business driver name
- rank

I want to see whether rollover-related features are genuinely weaker than the current primary driver, or whether the mapping/selection logic is dropping them.

4. Check driver mapping

Verify that rollover raw features map to business-friendly driver labels such as:

- "External rollover activity"
- "Partial rollover-out activity"
- "Recent external rollover activity"
- "Repeated external rollover activity"

Do not allow valid rollover features to fall into an unmapped/ignored category.

5. Check driver-selection threshold

Review the current threshold used to decide whether a SHAP contributor becomes:

- primary_churn_driver
- additional_churn_drivers

If the additional-driver threshold is too restrictive and causes valid material rollover contributors to be dropped, adjust it to a reasonable relative/significance rule.

Do NOT force rollover to appear merely because the rollover flag is Yes.

The driver must still have a meaningful positive account-level SHAP contribution.

6. Specific expected logic

Example:

If an account has:

- external_rollover_flag = Yes
- external_rollover_count_12m = 2

and SHAP values are:

- external_rollover_count_12m = +0.28
- campaign_activity = +0.10
- account_tenure = +0.06

then expected output should be approximately:

Primary Driver:
"External rollover activity"

Additional Drivers:
"Campaign activity, Account tenure"

But if:

- campaign_activity = +0.24
- external_rollover_count_12m = +0.05

then Campaign activity may correctly remain primary, and External rollover may appear only as an additional driver if significant.

7. Check leakage safety

Only rollover events occurring on or before AsOfDate may be considered.

Internal transfers must remain excluded.

Do not use:

- post-AsOfDate rollover events
- full exit completion events from the outcome window
- future rollover information

as predictive drivers.

8. Driver distribution check

After fixing/validating the logic, print the full distribution of "primary_churn_driver".

Show:

- driver name
- account count
- percentage

Also specifically show:

- number of accounts with external rollover activity
- number of those where rollover is primary driver
- number where rollover is additional driver
- number where rollover is not a significant driver

9. Regenerate output only if required

If the investigation identifies a mapping or driver-selection bug, regenerate:

- "primary_churn_driver"
- "additional_churn_drivers"
- "driver_count"

in:

"member_retention_ml_scoring_output.csv"

and:

"member_retention_ml_scoring_sample_15.csv"

Do not change:

- churn_probability
- risk_band
- model scores
- risk thresholds

unless model scoring itself is found to be wrong.

10. Final conclusion

At the end clearly state one of these:

A. Rollover features are working correctly and their SHAP contribution is genuinely lower than other drivers.

OR

B. Rollover features had significant SHAP contribution but were missing because of driver mapping / selection logic, and the output has now been corrected.

Also show 5 example accounts with external rollover activity before and after the driver validation.
