The current issue is that "consolidated_behavioural_feature_dataset_review.sql" is too heavy to complete in the local session.

Do NOT replace the approved feature logic with synthetic/random data.

I need a smaller deterministic REAL-data sample from the same approved feature dataset so that the local Random Forest scoring pipeline can complete.

Please do the following:

1. Keep the existing feature engineering logic unchanged wherever possible.

2. Create a technical sample version of the SQL using a deterministic account subset.

Preferred approach:

- first identify eligible accountIDs
- select a deterministic subset such as TOP 5,000 or TOP 10,000 accountIDs ordered by accountID
- apply all remaining feature joins/calculations only to those selected accounts

Do not use "TOP" only at the final SELECT because that would still execute the full heavy query first.

3. Keep the same grain:
   one row per "accountID + AsOfDate"

4. Keep the current AsOfDate logic.

5. Execute the reduced real-data query and validate:

- total rows
- distinct accountID
- duplicate accountID + AsOfDate count
- missing accountID
- missing memberID
- feature column count
- target_churn distribution if available

Duplicate accountID + AsOfDate must be 0.

6. Use this real sampled dataset in the existing local Random Forest pipeline.

7. Generate the required ML output columns:

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
- external_rollover_flag
- latest_rollover_destination_type
- latest_rollover_destination_name
- external_rollover_count_12m
- external_rollover_count_6m

Also add only these useful end-user fields:

- risk_rank
- risk_percentile
- driver_count
- scoring_run_timestamp
- data_quality_flag

Do NOT add priority_segment for now.

8. Important:
   Do not fabricate previous_churn_probability, risk_change, or risk_trend.

If only one scoring snapshot exists:

- previous_churn_probability = NULL
- risk_change = NULL
- risk_trend = 'New / No Previous Score'

If possible, generate one previous monthly snapshot too so that these values can be calculated properly.

9. For churn drivers:
   Use actual feature values / account-level explainability.

Do not use overall Random Forest feature importance as an account-specific churn driver.

Keep only strategically meaningful drivers.

10. For rollover destination:
    Inspect the actual "accountRolloverPayment" columns first.

Do not invent destination names/types.

If unavailable, populate NULL and document the limitation.

11. Validate final output:

- one row per account + scoring date
- probability between 0 and 1
- risk-band thresholds correct
- no future leakage
- risk_change arithmetic correct
- 6M rollover count <= 12M rollover count
- external rollover flag consistent with counts
- no synthetic business values

12. Generate:

- full scoring CSV
- 15-row real sample CSV
- validation markdown

Use:
"member_retention_ml_scoring_output.csv"
"member_retention_ml_scoring_sample_15.csv"
"member_retention_ml_scoring_validation.md"

13. Show me the 15 real rows only after all validation checks pass.

The purpose is a LOCAL TECHNICAL SAMPLE for business / Power BI review, not production model output.
