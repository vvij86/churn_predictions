The latest XGBoost output still needs two corrections.

Issue 1

The final CSV does not clearly contain/populate the required rollover amount fields and "model_version".

Issue 2

Accounts with qualifying external / partial rollover activity are still not showing rollover as a high-priority business-facing churn driver.

Please fix both without changing churn_probability or risk_band.

1. Mandatory final output schema

Regenerate "member_retention_ml_scoring_output.csv" with these columns explicitly present in the final exported DataFrame and CSV:

- account_id
- member_id
- fundJoinDate
- fundID
- MonthKey
- ml_scoring_date
- churn_probability
- risk_band
- primary_churn_driver
- additional_churn_drivers
- retention_category
- current_account_fum_amount
- model_version
- risk_trend
- risk_change
- tenure_years
- days_since_last_contribution
- net_flow_12m
- previous_churn_probability

External rollover reporting fields

- external_rollover_flag
- latest_rollover_destination_type
- latest_rollover_destination_name
- external_rollover_count_12m
- external_rollover_count_6m
- external_rollover_amount_12m
- external_rollover_amount_6m

Partial rollover model/reporting fields

- partial_rollover_count_12m
- partial_rollover_amount_12m
- days_since_last_partial_rollover
- recent_partial_rollover_count_90d
- recent_partial_rollover_amount_90d

Additional useful fields

- risk_rank
- risk_percentile
- driver_count
- scoring_run_timestamp
- data_quality_flag

Before saving the CSV, print the final DataFrame column list and confirm every required column is present.

2. model_version

Populate:

"model_version = 'XGB_local_v1'"

for every scored row.

Validate:

- model_version NULL count = 0
- distinct model_version values

Expected result:

"XGB_local_v1"

Do not allow model_version to disappear during final column selection/export.

3. External rollover amount calculation

Use actual qualifying records from:

"edgeSource.accountRolloverPayment"

and actual "paymentAmount".

Generate:

external_rollover_amount_12m

Sum qualifying external rollover amount between:

"AsOfDate - 12 months" and "AsOfDate"

external_rollover_amount_6m

Sum qualifying external rollover amount between:

"AsOfDate - 6 months" and "AsOfDate"

Exclude:

- internal transfers
- events after AsOfDate
- non-qualifying rollover/payment types

Do not fabricate amounts.

If no qualifying external rollover exists, use 0 only when that genuinely means no qualifying event; otherwise preserve NULL according to the source logic.

4. Validate external rollover amounts

Print:

- accounts with external_rollover_flag = Yes
- accounts with external_rollover_amount_12m > 0
- accounts with external_rollover_amount_6m > 0
- min / median / max external rollover amount
- count where external_rollover_amount_6m > external_rollover_amount_12m

The last count should be 0.

Also identify any account where:

"external_rollover_flag = Yes"

but:

"external_rollover_amount_12m = 0 or NULL"

and explain why.

5. Business-prioritized churn-driver rule

For the BUSINESS-FACING churn-driver fields, apply the following hierarchy.

This is a business explanation rule and must NOT change XGBoost probability, SHAP values or risk_band.

Priority 1 – Qualifying external rollover

If:

"external_rollover_count_12m > 0"

OR:

"external_rollover_amount_12m > 0"

then set:

"primary_churn_driver = 'External rollover activity'"

This applies only to genuine qualifying rollover activity before AsOfDate.

Priority 2 – Partial rollover

If there is no qualifying external rollover but:

"partial_rollover_count_12m > 0"

OR:

"partial_rollover_amount_12m > 0"

then:

"primary_churn_driver = 'Partial rollover-out activity'"

Priority 3 – Recent partial rollover

If there is no higher-priority rollover rule but:

"recent_partial_rollover_count_90d > 0"

OR:

"recent_partial_rollover_amount_90d > 0"

then:

"primary_churn_driver = 'Recent partial rollover activity'"

Priority 4 – Model / SHAP driver

If there is no qualifying rollover behaviour, use the strongest strategically meaningful positive SHAP driver.

6. Additional churn drivers

After applying the business-priority primary driver, populate "additional_churn_drivers" from the strongest remaining meaningful SHAP/business drivers.

Example:

Primary:
"External rollover activity"

Additional:
"Contribution decline, Long gap since last contribution"

Do not repeat rollover again in additional drivers.

Do not force low-value technical features simply to fill the field.

7. Preserve pure model explanation separately

To maintain transparency, add:

- "model_top_shap_driver"
- "model_top_shap_value"

Example:

"primary_churn_driver = External rollover activity"

but:

"model_top_shap_driver = Campaign activity"

This makes it clear that primary_churn_driver is business-prioritized, while the pure model explanation is still retained separately.

8. Rollover driver validation

After regeneration print:

- external rollover positive accounts
- partial rollover positive accounts
- accounts with External rollover activity as primary driver
- accounts with Partial rollover-out activity as primary driver
- accounts where business primary driver differs from model_top_shap_driver

Specifically show 10 example rollover-positive accounts containing:

- account_id
- churn_probability
- risk_band
- external_rollover_count_12m
- external_rollover_amount_12m
- external_rollover_count_6m
- external_rollover_amount_6m
- latest_rollover_destination_type
- latest_rollover_destination_name
- partial_rollover_count_12m
- partial_rollover_amount_12m
- primary_churn_driver
- additional_churn_drivers
- model_top_shap_driver

9. Regenerate both CSVs

Regenerate:

"member_retention_ml_scoring_output.csv"

and:

"member_retention_ml_scoring_sample_15.csv"

The 15-row sample must continue to contain:

- 5 High
- 5 Medium
- 5 Low

where available.

For the sample, deliberately select real rows so that some have qualifying rollover activity and populated rollover amount/destination information.

Do not modify churn probabilities to achieve this.

10. Final verification

Before finishing confirm:

- model_version exists and is populated
- external_rollover_amount_12m exists
- external_rollover_amount_6m exists
- partial_rollover_amount_12m exists
- recent_partial_rollover_amount_90d exists
- rollover-positive accounts show rollover as business-priority primary driver
- churn_probability unchanged
- risk_band unchanged
- XGBoost/SHAP values unchanged

Print PASS / FAIL for each item.

Important:
This change is to the BUSINESS-FACING driver presentation and final output schema. Do not manipulate the XGBoost prediction to artificially increase rollover importance.
