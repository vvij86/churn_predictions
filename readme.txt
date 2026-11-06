Use the current validated XGBoost local technical scoring pipeline, but run a new real-data scoring test using:

"AsOfDate = '2025-04-01'"

The purpose is to generate a business-review sample with better behavioural variety, especially external rollover information.

Do NOT fabricate any rollover values or churn scores.

1. Use the same approved feature logic

Use the existing approved consolidated feature dataset / deterministic sampled version.

Keep the grain:

"one row per accountID + AsOfDate"

Use:

"AsOfDate = 2025-04-01"

All model input features must use only data available on or before 2025-04-01.

Do not introduce future information or target leakage.

2. Use XGBoost

Use the selected XGBoost model/configuration from the previous model comparison.

Do not switch back to Random Forest for this run.

Keep the same risk thresholds:

- High >= 0.70
- Medium >= 0.40 and < 0.70
- Low < 0.40

Generate churn_probability using XGBoost predict_proba.

3. Net Money Flow business decision

The client has indicated that "accountNetMoneyFlow" is not considered an important source for the business-facing churn-driver view.

Therefore:

- Do NOT use "net_flow_12m" as the primary churn driver.
- Do NOT use net money flow related features as additional business-facing churn drivers for this sample.
- Do not delete the feature from the technical feature dataset unless required.
- It may remain internally available to the model for now, but it should not be exposed as a churn driver in the business sample.

Prefer business-relevant drivers from the approved feature groups such as:

- Employer contribution cessation
- Employer SG contribution decline
- Salary sacrifice cessation
- Member voluntary contribution decline
- Reduced contribution frequency
- Long gap since last contribution
- Partial rollover-out activity
- External rollover activity
- Rollover / consolidation enquiry
- Complaint / escalation activity
- Retirement / pension enquiry
- Investment switch activity
- Low digital / web engagement
- Long gap since web activity
- Helpline engagement
- workflow/member-driven activity

4. External rollover fields

Inspect the real source fields in:

"edgeSource.accountRolloverPayment"

Use actual source columns only.

Populate, where supported:

- "external_rollover_flag"
- "latest_rollover_destination_type"
- "latest_rollover_destination_name"
- "external_rollover_count_12m"
- "external_rollover_count_6m"

Exclude internal transfers.

Use only qualifying rollover records on or before AsOfDate.

Do not invent destination names.

If destination name/type is unavailable in the source, leave NULL and document it.

5. Specifically validate rollover population

For the 2025-04-01 scoring population print:

- external_rollover_flag = Yes count
- external_rollover_flag = No count
- destination type populated count
- destination name populated count
- external_rollover_count_12m > 0 count
- external_rollover_count_6m > 0 count

Also validate:

"external_rollover_count_6m <= external_rollover_count_12m"

for every account.

6. Final output columns

Generate:

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
- risk_rank
- risk_percentile
- driver_count
- scoring_run_timestamp
- data_quality_flag

Note:
"net_flow_12m" may remain in the output for reference if already required, but it should NOT be used as a displayed churn driver.

Set model_version to something clear such as:

"XGB_local_v1"

7. Churn-driver generation

Use SHAP / account-level XGBoost contribution logic.

Do not use global feature importance as an account-specific driver.

Map technical features to business-friendly driver labels.

Exclude net-money-flow features from the business-facing driver selection.

For each account:

- primary_churn_driver = strongest strategically meaningful driver
- additional_churn_drivers = other meaningful drivers, comma separated
- driver_count = count of significant drivers

Do not force a fixed number of drivers.

8. Generate full scoring output

Create/update:

"member_retention_ml_scoring_output.csv"

using the 2025-04-01 XGBoost scoring result.

9. Generate 15-row business sample

Create:

"member_retention_ml_scoring_sample_15.csv"

The 15 rows must come directly from the real scoring output.

Where available, select:

- 5 High
- 5 Medium
- 5 Low

The sample should also deliberately include variety in rollover behaviour.

Where the real data permits, include at least:

- 2 or more accounts with "external_rollover_flag = Yes"
- at least 1 account with "latest_rollover_destination_type" populated
- at least 1 account with "latest_rollover_destination_name" populated
- accounts with different external_rollover_count_12m values
- accounts with external rollover = No

Do NOT manufacture rollover rows if the real output does not contain enough.

Also include variety in:

- primary churn driver
- additional churn drivers
- FUM
- tenure_years
- days_since_last_contribution
- churn probability
- risk bands

10. Sample selection preference

When selecting the 15 rows, prefer accounts with richer business information.

Priority for representative sample selection:

1. High-risk accounts with real external rollover activity
2. High-risk accounts with contribution / rollover / complaint / retirement signals
3. Medium-risk accounts with different behavioural drivers
4. Low-risk accounts for contrast

Do NOT change scores or model results to satisfy this preference.

11. Validate 15-row sample

Print:

- total rows = 15
- High count
- Medium count
- Low count
- external rollover Yes count
- external rollover No count
- destination name populated count
- destination type populated count

Also confirm:

- every sample row exists unchanged in the full XGBoost output
- no duplicate account + scoring date rows
- no manually edited values

12. Compare with previous snapshot

At the end compare the 2025-04-01 result with the previous selected scoring run.

Show:

"AsOfDate | High | Medium | Low | Max Probability | External Rollover Yes | Destination Name Populated"

This will help determine whether 2025-04-01 gives a better business-review sample.

13. Final output

At the end show:

A. 2025-04-01 full risk distribution

B. External rollover coverage

C. 15-row sample risk distribution

D. Complete 15-row sample

E. Top primary churn drivers excluding Net Money Flow

F. Any source limitations for rollover destination

Important:
Do not lower thresholds, fabricate rollover data, fabricate destination names, or manipulate scores simply to make the sample look better.
