The model comparison is now complete.

Current comparison result:

- Baseline / tuned Random Forest did not naturally produce High Risk rows under the fixed thresholds.
- XGBoost produced a natural spread of High / Medium / Low risk bands.
- XGBoost validation performance is comparable/slightly better and gives better probability separation.

For this LOCAL TECHNICAL SAMPLE, use XGBoost as the selected model for the final scoring export.

Do NOT change the approved feature engineering logic.

Do NOT change the risk thresholds:

- High Risk: churn_probability >= 0.70
- Medium Risk: 0.40 <= churn_probability < 0.70
- Low Risk: churn_probability < 0.40

Do NOT fabricate or manually edit any values.

1. Use the cached real feature dataset

Use the same deterministic real-data feature sample used in the model comparison.

Do not rerun the full SQL unless absolutely required.

Use the same:

- feature columns
- preprocessing
- target definition
- account population
- AsOfDate
- validation logic

2. Score using selected XGBoost model

Use the selected validated XGBClassifier configuration from the comparison run.

Generate churn probability using:

"predict_proba(... )[:, 1]"

Then derive risk_band using the fixed thresholds.

3. Final mandatory ML output columns

Generate the final scoring output with:

1. account_id
2. member_id
3. fundJoinDate
4. fundID
5. MonthKey
6. ml_scoring_date
7. churn_probability
8. risk_band
9. primary_churn_driver
10. additional_churn_drivers
11. retention_category
12. current_account_fum_amount
13. model_version
14. risk_trend
15. risk_change
16. tenure_years
17. days_since_last_contribution
18. net_flow_12m
19. previous_churn_probability
20. external_rollover_flag
21. latest_rollover_destination_type
22. latest_rollover_destination_name
23. external_rollover_count_12m
24. external_rollover_count_6m
25. risk_rank
26. risk_percentile
27. driver_count
28. scoring_run_timestamp
29. data_quality_flag

Do NOT add priority_segment for now.

Set model_version clearly, for example:

"XGB_local_v1"

4. Churn drivers

Generate account-level churn drivers from actual model explainability / feature contributions.

Preferred:

- SHAP for XGBoost

Rules:

- primary_churn_driver = strongest strategically significant positive churn-risk driver
- additional_churn_drivers = other significant drivers, comma separated
- do not force a fixed number
- driver_count = number of significant retained drivers

Do not use global feature importance as account-level churn drivers.

Use business-friendly labels.

Only use drivers supported by actual account feature values.

5. Previous score / trend fields

If valid previous monthly score exists:

"previous_churn_probability = previous snapshot churn probability"

"risk_change = current churn_probability - previous_churn_probability"

Use:

- «= +0.03 → Increasing»
- <= -0.03 → Decreasing
- otherwise → Stable

If previous score is unavailable:

- previous_churn_probability = NULL
- risk_change = NULL
- risk_trend = 'New / No Previous Score'

Do not fabricate previous scores.

6. Rollover fields

Use actual source-derived values only.

Do not invent destination names/types.

Validate:

- external_rollover_count_6m <= external_rollover_count_12m
- if rollover count > 0, external_rollover_flag should be Yes
- internal transfers must remain excluded

7. Generate final full scoring file

Create:

"member_retention_ml_scoring_output.csv"

This must now contain the XGBoost scoring results, replacing the earlier Random Forest sample output.

Before overwriting, confirm that the old file was generated from Random Forest and the new file is generated from XGBoost.

8. Generate 15-row Confluence sample

Create:

"member_retention_ml_scoring_sample_15.csv"

The 15 rows must come directly from the validated XGBoost scoring output.

Preferred composition:

- 5 High Risk
- 5 Medium Risk
- 5 Low Risk

Since XGBoost naturally produced all three bands, aim for exactly 5 / 5 / 5.

Do NOT simply take the first 15 rows.

Use deterministic sample selection.

Within the 15 rows, include useful variety where possible:

- different churn probabilities
- different FUM values
- different primary drivers
- different additional drivers
- external rollover Yes and No
- different rollover counts
- positive and negative net_flow_12m
- different tenure_years
- different days_since_last_contribution
- different risk trends where available

Do not manually edit values after selection.

9. Validate full XGBoost output

Run and report:

Grain

- total rows
- distinct account_id + ml_scoring_date
- duplicate count must be 0

Probability

- min
- mean
- P50
- P75
- P90
- P95
- P99
- max

All churn probabilities must be between 0 and 1.

Risk bands

Report:

- High count
- Medium count
- Low count
- percentages

Validate thresholds exactly.

FUM

Report:

- populated count
- NULL count
- zero count
- min / median / max

Do not replace genuine NULL FUM with 0.

Drivers

Report:

- primary driver NULL count
- driver_count distribution
- top primary driver categories

Ensure no leakage/outcome fields appear as drivers.

Rollover

Report:

- Yes / No counts
- 12M rollover count distribution
- 6M rollover count distribution
- count where 6M > 12M must be 0
- destination name populated count
- destination type populated count

Previous score

Report:

- previous score available count
- previous score unavailable count

10. Validate the 15-row sample separately

Print:

- High Risk rows = 5
- Medium Risk rows = 5
- Low Risk rows = 5
- Total rows = 15

If exact 5 / 5 / 5 cannot be produced from the real XGBoost output, do not fabricate rows. Report the actual available distribution.

Also confirm:

- all 15 sample rows exist in the full scoring output
- no manually edited values
- no duplicate account rows for the same scoring date

11. Generate validation report

Create/update:

"member_retention_ml_scoring_validation.md"

Include:

Model used

XGBoost

Why selected

State that XGBoost had comparable/slightly better validation performance and better natural probability separation than Random Forest under the unchanged thresholds.

Do NOT state that it was selected simply because it produced High Risk accounts.

Full risk distribution

Show High / Medium / Low counts.

15-row sample distribution

Show High / Medium / Low counts.

Validation checks

PASS / FAIL for:

- grain
- probability range
- risk thresholds
- FUM handling
- churn drivers
- rollover consistency
- previous-score handling
- 15-row sample composition

12. Final output to display

At the end show:

A. Selected model

XGBoost + model version

B. Full scoring distribution

High / Medium / Low counts

C. Probability statistics

P50 / P90 / P95 / P99 / max

D. 15-row sample

Display the complete 15 rows ready for copying into Confluence.

E. Sample validation

Confirm whether the sample is 5 High / 5 Medium / 5 Low.

F. Limitations

Clearly state:

- this is a local deterministic technical sample
- not production-ready model selection
- previous scoring history limitations if applicable
- rollover destination availability limitations
- explainability limitations if any

Important:
The final CSVs must contain REAL XGBoost scoring results from the validated feature dataset. Do not manufacture a desired business distribution.
