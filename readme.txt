Create a professional Word document named:

Churn_Model_Evaluation_Comparison_and_Recommendation.docx

Also create the Python script:

create_churn_model_evaluation_document.py

Use python-docx.

Do not retrain any model.
Do not modify existing CSV, Python or SQL files.
Do not scan unrelated folders.

Use only these files where available:

1. model_comparison_all_models.csv
2. logistic_regression_top_churn_drivers.csv
3. decision_tree_top_churn_drivers.csv
4. random_forest_top_churn_drivers.csv
5. xgboost_top_churn_drivers.csv
6. xgboost_behavioural_top_churn_drivers.csv
7. hist_gradient_boosting_top_churn_drivers.csv
8. hist_gradient_boosting_top_behavioural_churn_drivers.csv
9. churn_model_dataset_validation_summary.csv
10. model_dataset.csv
11. POC_limitations.txt

If any listed file is missing, continue with the available files and mention the missing file in the appendix. Do not invent values.

The document must address this work-item objective:

“Compare all models using ROC-AUC, Precision, Recall, F1-score, confusion matrix and prediction probabilities. Select the best-performing model, explain the recommendation, and document the results, assumptions and POC limitations.”

Create the following sections.

1. Title Page

Title:
Churn Model Evaluation, Comparison and Recommendation

Include:

- Account-level churn prediction POC
- Prepared date
- Author placeholder
- Document version

2. Executive Summary

Explain in simple business language:

- The objective is to predict account-level churn risk
- The models evaluated are Logistic Regression, Decision Tree, Random Forest, XGBoost and HistGradientBoosting
- Each account receives a churn probability and predicted churn class
- The document compares model performance and recommends the best candidate
- Model drivers indicate association, not confirmed business causation

3. Dataset Overview

Read model_dataset.csv only for column names, row count and target distribution. Do not load unnecessary columns into memory if avoidable.

Document:

- Dataset grain: one row per ACCOUNT_ID
- Approximate row count from the actual file
- Number of input columns
- Churn and non-churn counts
- Churn percentage
- Target field: target_churn

Explain that:

- target_churn = 1 means the account churned during the defined future outcome window
- target_churn = 0 means no qualifying churn event occurred during that window

4. Input Date Definitions

Document these date concepts clearly with the current POC example:

- feature_start_date = 2024-01-01
- as_of_date = 2024-12-31
- outcome_start_date = 2025-01-01
- outcome_end_date = 2025-03-31

Use this plain-English explanation:

Feature start date:
The beginning of the historical period used to study account behaviour.

As-of date:
The snapshot or cutoff date. Only information known on or before this date can be used by the model.

Outcome start date:
The first date after the as-of date when churn is observed.

Outcome end date:
The final date of the future churn observation period.

Add a simple timeline:

01-Jan-2024 ---------------- 31-Dec-2024 | 01-Jan-2025 -------- 31-Mar-2025
Historical feature window                  Future outcome window

Explain why these dates are separated:

- To prevent future information from leaking into the model
- To simulate how the model would work in production
- To study past behaviour and predict future churn

5. Important Dataset Columns and Definitions

Use the columns from model_dataset.csv and create a business-friendly data dictionary.

Include only important modeling columns.

Create a table with:

- Column name
- Category
- Definition
- Data type
- Modeling purpose

Include definitions for the following where present:

Identifier:
- ACCOUNT_ID

Account profile:
- account_tenure_days
- account_type_code
- product_id
- scheme_id

Transaction behaviour:
- account_txn_count_12m
- account_txn_distinct_type_count_12m
- reversal_txn_count_12m
- days_since_last_account_txn

Contribution behaviour:
- contrib_txn_count_12m
- contrib_amount_sum_12m
- contrib_active_months_12m
- days_since_last_contribution

Rollover behaviour:
- rollover_event_count_12m
- rollover_amount_sum_12m
- days_since_last_rollover

Partial-withdrawal behaviour:
- partial_withdrawal_count_12m
- partial_withdrawal_amount_12m
- days_since_last_partial_withdrawal_12m
- partial_withdrawal_flag_12m
- significant_partial_withdrawal_count_12m
- significant_partial_withdrawal_amount_12m
- days_since_last_significant_partial_withdrawal_12m
- significant_partial_withdrawal_flag_12m
- min_partial_withdrawal_amount

Target:
- target_churn

Use these definitions:

ACCOUNT_ID:
Unique account identifier. Used only for traceability and not as a predictive feature.

account_tenure_days:
Number of days the account had been active as of the snapshot date.

account_type_code:
Category describing the account type.

product_id:
Product category associated with the account. Treated as categorical, not as a numerical amount.

scheme_id:
Scheme category associated with the account. Treated as categorical, not as a numerical amount.

account_txn_count_12m:
Total number of account transactions during the 12-month feature window.

account_txn_distinct_type_count_12m:
Number of different transaction types seen during the feature window.

reversal_txn_count_12m:
Number of reversed transactions during the feature window.

days_since_last_account_txn:
Number of days from the most recent account transaction to the as-of date.

contrib_txn_count_12m:
Number of contribution transactions during the feature window.

contrib_amount_sum_12m:
Total contribution amount during the feature window.

contrib_active_months_12m:
Number of months in which the account received at least one contribution.

days_since_last_contribution:
Number of days from the most recent contribution to the as-of date.

rollover_event_count_12m:
Number of rollover events during the feature window.

rollover_amount_sum_12m:
Total rollover amount during the feature window.

days_since_last_rollover:
Number of days from the most recent rollover to the as-of date.

partial_withdrawal_count_12m:
Number of partial-withdrawal transactions during the feature window.

partial_withdrawal_amount_12m:
Total partial-withdrawal amount during the feature window.

days_since_last_partial_withdrawal_12m:
Number of days from the most recent partial withdrawal to the as-of date.

partial_withdrawal_flag_12m:
Indicates whether at least one partial withdrawal occurred during the feature window.

significant_partial_withdrawal_count_12m:
Number of partial withdrawals meeting the configured POC threshold.

significant_partial_withdrawal_amount_12m:
Total amount of partial withdrawals meeting the configured POC threshold.

days_since_last_significant_partial_withdrawal_12m:
Number of days from the latest significant partial withdrawal to the as-of date.

significant_partial_withdrawal_flag_12m:
Indicates whether at least one significant partial withdrawal occurred.

min_partial_withdrawal_amount:
Configured POC threshold used to identify significant partial withdrawals. Requires business confirmation.

target_churn:
Ground-truth training label showing whether the account churned during the future outcome period.

6. Model Definitions

Provide one short business-friendly subsection for each:

- Logistic Regression
- Decision Tree
- Random Forest
- XGBoost
- HistGradientBoosting

For each include:

- What it is
- Main advantage
- Main limitation
- Explainability level

7. Evaluation Metrics

Explain:

- ROC-AUC
- PR-AUC / Average Precision
- Accuracy
- Precision
- Recall
- F1-score
- Confusion matrix
- Prediction probability
- Training time
- Prediction time

Use plain-English interpretations.

Explain that PR-AUC, recall and F1 are especially important because churn is the minority class.

Explain confusion-matrix terms:

- True Positive: churn correctly identified
- False Positive: non-churn incorrectly flagged as churn
- True Negative: non-churn correctly identified
- False Negative: churn account missed by the model

8. Model Comparison

Read the actual values from:

model_comparison_all_models.csv

Create a formatted table with:

- Model
- ROC-AUC
- PR-AUC
- Accuracy
- Precision
- Recall
- F1-score
- Training time
- Prediction time

Bold the best value in each metric column.

Automatically identify:

- Best ROC-AUC
- Best PR-AUC
- Best precision
- Best recall
- Best F1-score
- Fastest prediction
- Best overall balanced model

Do not hard-code winners.

9. Prediction Probabilities and Threshold

Explain:

- The model produces a probability between 0 and 1
- A higher score means higher predicted churn risk
- A threshold converts probability into predicted churn or non-churn
- A default threshold of 0.50 is not automatically the best business threshold

Explain that the final threshold should consider:

- Retention-team capacity
- Cost of missed churn
- Cost of false alerts
- Required recall
- Required precision

10. Important Churn Drivers

Read the available driver files listed above.

Create two subsections.

A. Behavioural churn drivers

Exclude product_id and scheme_id.

Show important drivers across the models in a table with:

- Rank
- Feature
- Model
- Importance or coefficient
- Direction, where available
- Plain-English interpretation

B. Product and scheme associations

Show product_id and scheme_id separately.

Add this caution:

“Product and scheme importance represents predictive association and may reflect customer mix, product design or data distribution. It does not prove that a specific product or scheme causes churn.”

11. Model Recommendation

Use the actual comparison results.

Include:

- Recommended primary model
- Recommended explainable baseline
- Recommended challenger model

Base the recommendation on:

- PR-AUC
- Recall
- F1-score
- ROC-AUC
- Runtime
- Explainability

Provide one short reason for each model recommendation.

Do not say the model is fully production-ready.

Add this statement:

“Final model selection is subject to business threshold selection, out-of-time validation, stability testing and business review of the identified churn drivers.”

12. Assumptions

Include:

- One account-level row is used for modeling
- Only information available on or before the as-of date is used as input
- Product ID and scheme ID are treated as categorical variables
- Partial withdrawal is a behavioural feature and does not directly define churn
- The significant partial-withdrawal threshold is a POC assumption requiring business confirmation
- Death outcomes are excluded from training
- Target-support and future-outcome fields are excluded from model features

13. POC Limitations

Read POC_limitations.txt if available and include its contents in a summarized format.

Also include:

- Only one as-of-date cohort is currently used
- Random stratified splitting is weaker than true future-time validation
- Recent historical data coverage is limited
- Historical FUM or balance data is not included in V1
- Full versus partial rollover logic needs further business validation
- Product and scheme effects may be influenced by account mix
- Model importance shows association, not causation
- Performance may change on future data

14. Conclusion

Summarize:

- Models were successfully compared
- The strongest candidate was selected based on multiple metrics
- The explainable baseline should be retained
- Business validation and out-of-time testing are required before production use

15. Appendix

Include:

- Input files used
- Missing input files
- Full model comparison table
- Top churn-driver tables
- Glossary

Formatting requirements:

- Professional title page
- Table of contents
- Clear headings
- Tables with borders
- Page numbers
- Footer:
  “POC results – subject to business validation”
- Use simple business language
- Keep the document approximately 10 to 15 pages
- Do not add LLM recommendation, deployment architecture or unrelated sections

After generating the document:

1. Save it as Churn_Model_Evaluation_Comparison_and_Recommendation.docx
2. Print the exact output path
3. Print the list of files used
4. Print the list of missing files
5. Confirm that no model was retrained
