I currently have the SQL file:

"consolidated_behavioural_feature_dataset_review.sql"

This query generates the current approved account-level behavioural feature dataset.

Grain of the feature dataset:
one row per accountID + AsOfDate

I also have a local Python Random Forest sample implementation available.

I now need to generate a REAL sample ML scoring output using the actual feature dataset returned by the SQL query. Do not generate synthetic/random business data for the final output.

Please perform the work in clear stages and validate each stage.

1. Execute / use the current feature dataset

Use the output of "consolidated_behavioural_feature_dataset_review.sql" as the model input dataset.

Keep the existing account-level grain.

Do not change the feature engineering business logic unless technically required.

Do not use any data after "AsOfDate".

Verify before modelling:

- total row count
- distinct accountID count
- duplicate "accountID + AsOfDate" count
- missing accountID
- missing memberID
- missing AsOfDate
- target distribution if target_churn is available
- FUM NULL count
- feature column count

The duplicate "accountID + AsOfDate" count must be 0.

2. Prepare a simple local Random Forest model

Use a simple RandomForestClassifier for this technical/sample exercise.

If a historical target column such as "target_churn" already exists, use it.

Exclude identifier/reference/output-only columns from model training, including where applicable:

- accountID
- memberID / memberNumber
- AsOfDate
- fundID
- fundJoinDate
- MonthKey
- exitDateRecorded
- any target/outcome-window fields
- current output fields
- any future information

Avoid target leakage.

Handle:

- categorical columns
- missing numeric values
- missing categorical values

Keep the preprocessing reproducible.

If time-based training/validation data is available, use chronological splitting rather than random splitting.

For this task, the objective is to generate a technically valid sample scoring output, not extensive model tuning.

3. Generate churn probability

For every scored account generate:

"churn_probability"

using Random Forest "predict_proba".

Create risk bands using the current agreed initial thresholds:

- High: churn_probability >= 0.70
- Medium: 0.40 <= churn_probability < 0.70
- Low: churn_probability < 0.40

Generate:

"risk_band"

4. Generate churn drivers

For each scored account generate business-readable churn drivers from the actual feature values / explainability results.

Use the most appropriate explainability approach available locally.

If SHAP works for the Random Forest, use SHAP.

If SHAP is unavailable, use a technically reasonable per-account contribution approach and clearly document the limitation.

Do NOT simply use overall Random Forest feature importance as though it were an account-level driver.

Driver output rules:

- "primary_churn_driver" = strongest strategically significant positive churn-risk driver for the account.
- "additional_churn_drivers" = other strategically significant drivers, comma separated.
- Do not force a fixed number of additional drivers.
- Do not expose low-impact technical features merely to fill the field.
- "driver_count" = number of significant drivers retained.

Use business-friendly descriptions rather than raw technical feature names where practical.

Examples of meaningful driver themes already present in the feature dataset may include:

- Employer contribution cessation
- Employer SG contribution decline
- Salary sacrifice cessation
- Member voluntary contribution decline
- Reduced contribution frequency
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

Only use a driver when supported by the actual account feature values.

5. Mandatory ML output columns

The final output MUST contain these columns in this order where possible:

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

Also add these useful end-user / Power BI fields if they can be generated reliably:

25. "risk_rank"
26. "risk_percentile"
27. "priority_segment"
28. "driver_count"
29. "scoring_run_timestamp"
30. "data_quality_flag"

6. Column derivation rules

Use the following rules.

tenure_years

Calculate from:

"fundJoinDate" to "AsOfDate"

Use a reasonable year calculation such as days / 365.25.

current_account_fum_amount

Use the existing FUM feature already produced from "accountInvestments".

Do not replace genuine NULL FUM with zero.

days_since_last_contribution

Use the existing feature from "accountMoneyInflow".

NULL should mean no qualifying previous contribution was available in the applicable historical window.

Do not automatically convert NULL to 0.

net_flow_12m

Use the existing 12-month net money flow feature derived from "accountNetMoneyFlow".

Preserve positive and negative values.

previous_churn_probability

For each account, obtain the churn probability from the immediately preceding scoring snapshot.

Use:

"LAG(churn_probability) OVER (PARTITION BY account_id ORDER BY ml_scoring_date)"

or equivalent Pandas logic.

If there is no prior scoring snapshot, leave it NULL.

risk_change

Calculate:

"churn_probability - previous_churn_probability"

Example:

Current = 0.81
Previous = 0.69
Risk Change = +0.12

risk_trend

Derive from risk_change using a configurable threshold.

Suggested initial rule:

- risk_change >= +0.03 → Increasing
- risk_change <= -0.03 → Decreasing
- otherwise → Stable

Keep the threshold configurable.

If previous probability is NULL:
"risk_trend = 'New / No Previous Score'"

retention_category

Use a simple business-friendly mapping initially:

- High Risk → At Risk
- Medium Risk → Monitor
- Low Risk → Retained

Keep this mapping configurable because business may refine it later.

external_rollover_flag

Use only qualifying external rollover records that occurred on or before AsOfDate.

Exclude internal transfers.

Set:

- Yes when qualifying external rollover activity exists in the defined window.
- No otherwise.

latest_rollover_destination_type

Take the destination type/category from the latest valid qualifying external rollover record on or before AsOfDate.

latest_rollover_destination_name

Take the destination fund/provider name from the latest valid qualifying external rollover record on or before AsOfDate.

Do not invent destination names.

If source data does not contain a reliable destination name, leave NULL and report this explicitly.

external_rollover_count_12m

Count qualifying external rollover transactions during:

"AsOfDate - 12 months" through "AsOfDate"

excluding internal transfers.

external_rollover_count_6m

Count qualifying external rollover transactions during:

"AsOfDate - 6 months" through "AsOfDate"

excluding internal transfers.

risk_rank

Rank accounts within each scoring date by churn_probability descending.

Highest-risk account = 1.

risk_percentile

Calculate the relative churn-risk percentile within the same scoring snapshot.

Higher percentile should mean higher relative churn risk.

priority_segment

Create an initial reporting-only prioritisation using risk and FUM.

Do NOT treat this as a predictive model feature.

Use an explainable rule and clearly show it in the code.

For example:

- High Risk + high FUM → High Priority
- High Risk or Medium Risk + meaningful FUM → Medium Priority
- otherwise → Standard

Do not hard-code arbitrary FUM thresholds without first showing the proposed threshold.

Prefer deriving FUM thresholds from the scored population, such as median / percentile, or keep them configurable.

data_quality_flag

Create a simple output quality indicator.

Examples:

- OK
- MISSING_FUM
- NO_PREVIOUS_SCORE
- MISSING_ROLLOVER_DESTINATION
- MULTIPLE_ISSUES

This is for technical review and can later be hidden from business users.

7. Important rollover validation

Before including destination fields, inspect the actual columns available in "edgeSource.accountRolloverPayment".

Do not assume destination column names.

Identify which actual source columns can support:

- external rollover identification
- destination type
- destination name
- rollover date
- internalTransferFlag
- partial/full rollover distinction

Print the actual column mapping being used.

If the source cannot support a requested output field, leave it NULL and state why.

Do NOT populate fake external fund names.

8. Validate the final ML output

After generating the final output, perform all of the following checks and print PASS/FAIL results.

Grain validation

Confirm:

"COUNT(*) = COUNT(DISTINCT account_id + ml_scoring_date)"

There must be one row per account per scoring date.

Probability validation

Confirm:

"0 <= churn_probability <= 1"

and where populated:

"0 <= previous_churn_probability <= 1"

Risk band validation

Validate that:

- probability >= 0.70 → High
- 0.40–0.699999 → Medium
- probability < 0.40 → Low

Risk change validation

For rows with previous probability:

"risk_change = churn_probability - previous_churn_probability"

Risk trend validation

Validate that the risk trend corresponds to the risk_change rule.

FUM validation

Print:

- FUM populated count
- FUM NULL count
- FUM zero count
- FUM min / median / max

Do not force missing FUM to zero.

Driver validation

Check:

- primary driver NULL count
- additional driver NULL count
- driver_count distribution
- examples of accounts and the underlying features supporting their drivers

Ensure no outcome/leakage features are shown as churn drivers.

Rollover validation

Print:

- external_rollover_flag Yes/No counts
- external_rollover_count_12m distribution
- external_rollover_count_6m distribution
- count where 6M > 12M — this MUST be 0
- destination name populated count
- destination type populated count

Where external_rollover_flag = No:

external rollover counts should normally be 0.

Where counts > 0:

external_rollover_flag should be Yes.

Previous score validation

Print count of accounts with:

- previous score available
- previous score unavailable

Do not fabricate previous probability when there is no earlier scoring snapshot.

9. Output sample for Confluence

After validation passes, display a clean sample of 15 real scored account rows.

Select a useful mix of:

- High Risk
- Medium Risk
- Low Risk
- Increasing risk
- Decreasing risk
- accounts with external rollover activity
- accounts without external rollover activity
- different FUM values

Do NOT manually edit the values after generation.

The 15 rows shown in Confluence must come directly from the generated output DataFrame/table.

Format churn probability to 4 decimal places for the sample.

Format monetary fields clearly.

Do not expose unnecessary sensitive personal fields.

10. Save outputs

Save:

1. Full ML scoring output as CSV.
2. 15-row validated sample as CSV.
3. Validation summary as TXT or Markdown.
4. Python script/notebook used to create the output.

Use clear filenames such as:

- "member_retention_ml_scoring_output.csv"
- "member_retention_ml_scoring_sample_15.csv"
- "member_retention_ml_scoring_validation.md"

At the end, provide:

A. Final column list

Column name + short business meaning + source/derivation.

B. Validation summary

PASS/FAIL for each validation.

C. 15-row sample

Ready for copying into Confluence.

D. Assumptions / limitations

Especially highlight:

- missing source fields
- rollover destination availability
- missing previous scoring snapshots
- any explainability limitations
- any fields that are reporting-derived rather than model-generated

Do not claim the output is production-ready. This is a validated local technical/sample ML output generated from the current feature dataset for business/Power BI review.
