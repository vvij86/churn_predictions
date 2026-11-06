The current XGBoost scoring output looks good overall.

I now want to test a few more AsOfDates to find a real snapshot with better rollover activity coverage, especially accounts with rollover amounts that also naturally fall into High Risk.

Do NOT fabricate rollover values.
Do NOT change the risk thresholds.
Do NOT manually force rollover to become High Risk.

Keep the current XGBoost model / feature logic / driver logic unchanged unless required for the new AsOfDate runs.

1. Add age to final output

Add:

"age_years"

to:

- "member_retention_ml_scoring_output.csv"
- "member_retention_ml_scoring_sample_15.csv"

Use the existing approved member age feature already present in the consolidated feature dataset.

Do not derive a new age definition if an approved "member_age" / equivalent feature already exists.

Use a clear business-facing column name:

"age_years"

Validate:

- age_years populated count
- age_years NULL count
- min / median / max age

2. Test additional AsOfDates

Run the same scoring process for these AsOfDates:

- 2025-04-01
- 2025-05-01
- 2025-06-01
- 2025-07-01
- 2025-08-01
- 2025-09-01

If one date cannot run because of source coverage, report it and continue.

Use the same deterministic real-account sample approach for each date.

Keep:

- same approved feature engineering logic
- same XGBoost model approach
- same feature list
- same preprocessing
- same leakage controls
- same risk thresholds

3. Keep risk thresholds fixed

Use:

- High >= 0.70
- Medium >= 0.40 and < 0.70
- Low < 0.40

Do not lower the High threshold.

4. For each AsOfDate calculate overall risk distribution

Print:

- total rows
- High count
- Medium count
- Low count
- High %
- Medium %
- Low %
- min churn_probability
- P50
- P90
- P95
- P99
- max churn_probability

5. Specifically measure rollover coverage

For each AsOfDate report:

- accounts with "external_rollover_flag = Yes"
- accounts with "external_rollover_count_12m > 0"
- accounts with "external_rollover_amount_12m > 0"
- accounts with "partial_rollover_count_12m > 0"
- accounts with "partial_rollover_amount_12m > 0"
- destination type populated count
- destination name populated count

Also report:

- total external_rollover_amount_12m
- median external_rollover_amount_12m
- max external_rollover_amount_12m
- total partial_rollover_amount_12m
- median partial_rollover_amount_12m
- max partial_rollover_amount_12m

6. Identify rollover accounts that are High Risk

For each AsOfDate calculate:

External rollover High Risk

Count of accounts where:

"risk_band = 'High'"

AND:

"external_rollover_amount_12m > 0"

Also report:

- average churn_probability
- median rollover amount
- max rollover amount

Partial rollover High Risk

Count of accounts where:

"risk_band = 'High'"

AND:

"partial_rollover_amount_12m > 0"

Also report:

- average churn_probability
- median partial rollover amount
- max partial rollover amount

7. Create AsOfDate comparison table

Show:

AsOfDate | Total Rows | High | Medium | Low | External Rollover Yes | External Rollover Amt > 0 | High + External Rollover | Partial Rollover Amt > 0 | High + Partial Rollover | Max Probability

Use this table to identify which AsOfDate provides the strongest natural business-review variety.

Do NOT select solely based on rollover amount.

Prefer a date with:

- meaningful High / Medium / Low spread
- real rollover-positive accounts
- some High Risk accounts with rollover activity
- good source coverage

8. Select the best AsOfDate

Choose the best snapshot for Confluence / Power BI review.

Explain why it was selected.

Example rationale:

- contains all three risk bands
- contains several real rollover-positive accounts
- contains rollover-positive High Risk accounts
- contains varied FUM / age / tenure / contribution behaviour

9. Final output columns

Keep the current final output and ensure these are present:

- account_id
- member_id
- fundJoinDate
- fundID
- MonthKey
- ml_scoring_date
- age_years
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

Rollover fields

- external_rollover_flag
- latest_rollover_destination_type
- latest_rollover_destination_name
- external_rollover_count_12m
- external_rollover_count_6m
- external_rollover_amount_12m
- external_rollover_amount_6m
- partial_rollover_count_12m
- partial_rollover_amount_12m
- days_since_last_partial_rollover
- recent_partial_rollover_count_90d
- recent_partial_rollover_amount_90d

Reporting / validation fields

- risk_rank
- risk_percentile
- driver_count
- scoring_run_timestamp
- data_quality_flag
- model_top_shap_driver
- model_top_shap_value

10. Regenerate 15-row sample for selected AsOfDate

Create:

"member_retention_ml_scoring_sample_15.csv"

Preferred mix:

- 5 High
- 5 Medium
- 5 Low

Within the 15 rows, where real data allows, include:

- at least 2 High Risk accounts with external rollover amount > 0
- at least 1 High Risk account with partial rollover amount > 0
- rollover Yes / No variety
- different rollover amounts
- different age_years
- different FUM
- different primary drivers
- different additional drivers
- different tenure
- different days since last contribution

Do not manually alter values.

11. Validation

For the selected snapshot confirm:

- duplicate account_id + ml_scoring_date = 0
- churn_probability between 0 and 1
- risk thresholds correct
- rollover amount 6M <= rollover amount 12M
- rollover count 6M <= rollover count 12M
- age_years populated correctly
- model_version populated
- sample rows exist unchanged in full output

12. Final result

At the end provide:

A. AsOfDate comparison table

B. Selected AsOfDate and reason

C. Risk distribution

D. Rollover coverage summary

E. Count of High Risk accounts with rollover activity

F. Final 15-row sample

G. Validation PASS / FAIL summary

Important:
The goal is to find a naturally useful real-data snapshot for business review, not to manipulate the model or thresholds to create rollover-driven High Risk accounts.
