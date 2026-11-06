The current validated local scoring run is working, but the current sample is producing mostly Medium-risk accounts. I need a REAL-data technical sample with a useful spread of High, Medium, and Low risk bands for business / Power BI review and for showing a 15-row sample in Confluence.

Do NOT fabricate, manually edit, or force churn probabilities, risk bands, feature values, rollover values, or churn drivers.

Use only real data produced from the approved feature dataset logic.

1. Source dataset

Use:

"consolidated_behavioural_feature_dataset_review.sql"

or the deterministic sampled version already created from the same approved feature logic.

Grain must remain:

one row per accountID + AsOfDate

Do not introduce synthetic rows.

Do not change the approved feature engineering logic except where needed to restrict execution to a deterministic real-account sample.

2. Deterministic real-data sample

Use the same deterministic account sampling approach already validated.

Preferred sample size:

- 10,000 real eligible accounts

Select the account subset early in the SQL logic so all feature calculations operate only on those accounts.

Do NOT apply "TOP 10000" only at the final SELECT.

Keep the selected account sample deterministic, for example ordered by "accountID", so repeated runs are reproducible.

3. Test multiple AsOfDates

The current AsOfDate does not provide sufficient risk-band variety.

Test the following historical AsOfDates using the same feature logic and same modelling approach:

- 2024-12-31
- 2025-01-31
- 2025-02-28
- 2025-03-31
- 2025-04-30
- 2025-05-31
- 2025-06-30

If any date cannot be processed because required historical data is unavailable, report it and continue with the remaining dates.

For every tested AsOfDate, generate the feature sample and model score distribution.

4. Keep the same Random Forest approach

Use the current local RandomForestClassifier pipeline.

Do not change model parameters or probability thresholds merely to create High-risk accounts.

Use the same preprocessing logic consistently across tested snapshots.

Avoid target leakage.

Exclude identifiers, dates, outcome fields, target fields, and future information from model training.

5. Risk-band thresholds

Keep the currently agreed thresholds unchanged:

- High Risk: "churn_probability >= 0.70"
- Medium Risk: "0.40 <= churn_probability < 0.70"
- Low Risk: "churn_probability < 0.40"

Do NOT lower the High-risk threshold just to generate High-risk rows.

6. Compare risk distributions across AsOfDates

For each tested AsOfDate report:

- row count
- distinct account count
- minimum churn probability
- maximum churn probability
- average churn probability
- median churn probability
- High Risk count
- High Risk %
- Medium Risk count
- Medium Risk %
- Low Risk count
- Low Risk %

Show a comparison table:

"AsOfDate | Rows | Min Prob | Max Prob | Avg Prob | High Count | Medium Count | Low Count"

Then identify the AsOfDate that naturally provides the best useful spread of High, Medium, and Low accounts.

Do not choose a date only because it has the most High-risk accounts. Prefer a snapshot that gives a meaningful overall distribution and has valid source coverage.

7. Mandatory final ML output columns

The final scoring output must contain these fields:

1. "account_id"
2. "member_id"
3. "fundJoinDate"
4. "fundID"
5. "MonthKey"
6. "ml_scoring_date"
7. "churn_probability"
8. "risk_band"
9. "primary_churn_driver"
10. "additional_churn_drivers"
11. "retention_category"
12. "current_account_fum_amount"
13. "model_version"
14. "risk_trend"
15. "risk_change"
16. "tenure_years"
17. "days_since_last_contribution"
18. "net_flow_12m"
19. "previous_churn_probability"
20. "external_rollover_flag"
21. "latest_rollover_destination_type"
22. "latest_rollover_destination_name"
23. "external_rollover_count_12m"
24. "external_rollover_count_6m"

Also include these useful reporting / review fields:

25. "risk_rank"
26. "risk_percentile"
27. "driver_count"
28. "scoring_run_timestamp"
29. "data_quality_flag"

Do NOT add "priority_segment" for now.

8. Churn driver generation

Generate account-level churn drivers from actual feature values / local explainability results.

Preferred approach:

- use SHAP if available for the Random Forest
- otherwise use a reasonable account-level contribution method and document the limitation

Do NOT use overall Random Forest feature importance as though it were an account-level driver.

Rules:

- "primary_churn_driver" = strongest strategically significant business-relevant churn driver
- "additional_churn_drivers" = other strategically significant drivers, comma separated
- do not force a fixed number
- "driver_count" = total significant drivers retained

Use business-friendly labels.

Examples of approved / useful driver themes include:

- Employer contribution cessation
- Employer SG contribution decline
- Salary sacrifice cessation
- Member voluntary contribution decline
- Reduced contribution activity
- Low contribution frequency
- Long gap since last contribution
- Negative net money flow
- Increased negative-flow months
- Partial rollover-out activity
- Rollover / consolidation enquiry
- Complaint / escalation activity
- Retirement / pension enquiry activity
- Investment switch activity
- Low web / digital engagement
- Long gap since last web activity
- Helpline engagement

Only output a driver when supported by the actual account feature values.

9. Previous score and risk trend

Do not fabricate previous scores.

If previous monthly scoring data exists:

"previous_churn_probability = previous snapshot churn probability"

Then:

"risk_change = current churn_probability - previous_churn_probability"

Suggested trend rule:

- "risk_change >= +0.03" → Increasing
- "risk_change <= -0.03" → Decreasing
- otherwise → Stable

Keep the threshold configurable.

If no valid previous scoring snapshot exists:

- "previous_churn_probability = NULL"
- "risk_change = NULL"
- "risk_trend = 'New / No Previous Score'"

If practical, generate the immediately previous monthly snapshot for the same account sample so these fields can be calculated correctly.

10. Rollover fields

Inspect actual source fields available in:

"edgeSource.accountRolloverPayment"

Do not assume or invent destination column names.

Use only actual available source fields to populate:

- external rollover flag
- latest rollover destination type
- latest rollover destination name
- external rollover count 12M
- external rollover count 6M

Exclude internal transfers.

Use only rollover activity on or before AsOfDate.

If destination name or type is not reliably available, leave NULL and document the limitation.

Do not populate fake fund/provider names.

11. Validation

Validate the selected final AsOfDate output.

Grain

Confirm:

- total rows
- distinct account_id + ml_scoring_date count
- duplicate count = 0

IDs

Confirm:

- missing account_id count = 0
- missing member_id count

Probability

Confirm:

- all churn probabilities are between 0 and 1
- previous probability values, where populated, are between 0 and 1

Risk bands

Confirm thresholds are applied correctly:

- «= 0.70 → High»
- «= 0.40 and < 0.70 → Medium»
- < 0.40 → Low

Risk change

Where previous probability exists:

"risk_change = churn_probability - previous_churn_probability"

Risk trend

Validate trend matches the agreed risk_change rule.

FUM

Report:

- populated count
- NULL count
- zero count
- min
- median
- max

Do not force missing FUM to zero.

Churn drivers

Report:

- primary driver NULL count
- driver_count distribution
- top primary driver categories
- sample accounts showing feature values supporting the driver

Ensure no target/outcome/leakage field appears as a churn driver.

Rollover

Validate:

- external rollover Yes count
- external rollover No count
- external_rollover_count_12m distribution
- external_rollover_count_6m distribution
- count where 6M > 12M = 0
- destination name populated count
- destination type populated count

Where rollover counts > 0, external_rollover_flag should be Yes.

Previous scoring

Report:

- previous score available count
- previous score unavailable count

12. Full output CSV

Generate the full scored output as:

"member_retention_ml_scoring_output.csv"

This should contain all scored accounts for the selected AsOfDate.

13. 15-row sample CSV MUST contain risk-band variety

Generate:

"member_retention_ml_scoring_sample_15.csv"

This file must contain a representative variety of actual generated results.

Target composition, where naturally available:

- 5 High Risk accounts
- 5 Medium Risk accounts
- 5 Low Risk accounts

Do NOT simply take the first 15 rows.

Select representative real rows after scoring.

Within each band, prefer variety in:

- different primary churn drivers
- different additional churn drivers
- different FUM values
- positive / negative net_flow_12m
- different tenure_years
- different days_since_last_contribution
- external rollover Yes / No
- different rollover counts
- increasing / stable / decreasing risk trend where previous scores exist

The sample must be created directly from the validated scored output.

Do not manually alter values.

If 5 rows are not available in a risk band

If the selected snapshot has fewer than 5 High Risk or Low Risk rows:

- include all available rows from that band
- fill the remaining sample rows from the other available bands
- clearly state the actual distribution of the 15-row sample

Example:

"High = 3, Medium = 7, Low = 5"

Do NOT fabricate rows to force 5/5/5.

14. Sample selection logic

Use a deterministic selection method so the 15-row sample can be regenerated.

For example:

1. Sort High Risk by churn_probability descending and select representative rows with different drivers.
2. Select Medium Risk across the probability range.
3. Select Low Risk across the probability range.
4. Where multiple equivalent rows exist, sort by account_id for reproducibility.

Document the exact sampling logic.

15. Confluence-ready sample

At the end display the complete 15-row sample with all relevant output columns.

The Confluence sample should visibly demonstrate:

- High / Medium / Low risk
- different churn probabilities
- different FUM values
- multiple churn-driver types
- rollover and non-rollover examples
- risk trend differences where available

Format probabilities to 4 decimal places.

Format monetary values clearly.

16. Files to create

Generate:

1. "member_retention_ml_scoring_output.csv"
2. "member_retention_ml_scoring_sample_15.csv"
3. "member_retention_ml_scoring_validation.md"

Also keep/update the Python scoring script used.

17. Final summary

At the end provide:

A. AsOfDate comparison

Show the distribution for every tested date.

B. Selected AsOfDate

Explain why it was selected.

C. Final output validation

PASS / FAIL for each validation check.

D. 15-row sample band distribution

Explicitly show:

- High Risk count
- Medium Risk count
- Low Risk count

for "member_retention_ml_scoring_sample_15.csv".

E. 15-row sample

Display the actual rows.

F. Limitations

Call out:

- this is a deterministic local technical sample
- not production-ready output
- missing previous-score history where applicable
- rollover destination source limitations
- explainability limitations
- any risk band not sufficiently represented

Important:
The objective is to create a real-data, validated, representative sample for business / Power BI review, not to manipulate the model to create a desired risk distribution.
