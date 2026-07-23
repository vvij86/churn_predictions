Create a concise Word document named:

Churn_Model_Evaluation_and_Recommendation.docx

Also create the Python script:

create_churn_model_documentation.py

Use python-docx.

Do not scan the entire workspace.
Do not retrain any model.
Do not modify any existing files.

Read only these files:

1. model_comparison_all_models.csv
2. logistic_regression_top_churn_drivers.csv
3. decision_tree_top_churn_drivers.csv
4. random_forest_top_churn_drivers.csv
5. xgboost_top_churn_drivers.csv
6. xgboost_behavioural_top_churn_drivers.csv
7. hist_gradient_boosting_top_churn_drivers.csv
8. hist_gradient_boosting_top_behavioural_churn_drivers.csv

If one of the driver files is missing, skip it and continue. Do not search other folders for replacement files.

Create a professional and easy-to-understand Word document with only the following sections:

1. Executive Summary

Explain:

- The objective is account-level churn prediction
- Models evaluated:
  - Logistic Regression
  - Decision Tree
  - Random Forest
  - XGBoost
  - HistGradientBoosting
- The model output is a churn probability and predicted churn class
- Model drivers represent predictive association, not confirmed causation

2. Model Definitions

For each model, provide a short plain-English definition, main advantage and main limitation.

Include:

- Logistic Regression
- Decision Tree
- Random Forest
- XGBoost
- HistGradientBoosting

Keep each model definition to one short paragraph.

3. Evaluation Metrics

Explain these metrics in simple language:

- ROC-AUC
- PR-AUC / Average Precision
- Accuracy
- Precision for churn
- Recall for churn
- F1-score
- Training time
- Prediction time

Mention that PR-AUC, recall and F1 are especially important because churn is the minority class.

4. Model Comparison

Read all values directly from:

model_comparison_all_models.csv

Create a formatted Word table containing:

- Model
- ROC-AUC
- PR-AUC
- Accuracy
- Precision
- Recall
- F1-score
- Training time
- Prediction time

Bold the best value for each metric.

Below the table, automatically identify:

- Best model by ROC-AUC
- Best model by PR-AUC
- Best model by recall
- Best model by F1-score
- Fastest prediction model

Do not hard-code the winner. Derive it from the CSV values.

5. Important Churn Drivers

Read the available churn-driver CSV files listed above.

Create two sections:

A. Behavioural churn drivers

Exclude product_id and scheme_id features.

Show the most important available behavioural drivers across the models, such as:

- transaction activity
- account tenure
- contribution behaviour
- rollover behaviour
- partial-withdrawal behaviour
- recency and no-history indicators

Create a table with:

- Rank
- Feature
- Model
- Importance or coefficient
- Plain-English meaning

B. Product and scheme associations

Show important product_id and scheme_id categories separately.

State clearly that these are associations and may reflect customer mix, product design or data distribution.

Do not describe product or scheme IDs as direct causes of churn.

6. Recommendation

Use the values from model_comparison_all_models.csv to recommend the most suitable model.

Base the recommendation on:

- PR-AUC
- Recall
- F1-score
- ROC-AUC
- Training and prediction time
- Explainability

Include:

- Recommended primary model
- Recommended explainable baseline
- Recommended challenger model
- One short reason for each recommendation

Do not state that the selected model is fully production-ready.

Add this note:

“Final model selection is subject to business threshold selection, out-of-time validation, stability testing and business review of churn drivers.”

Formatting requirements:

- Professional title
- Clear headings
- Simple business language
- Tables with borders
- Page numbers
- Footer:
  “POC results – subject to business validation”
- Keep the document concise, approximately 8 to 12 pages
- Do not add dataset design, LLM recommendation, deployment architecture or unrelated technical sections

After generating the document:

1. Save it as Churn_Model_Evaluation_and_Recommendation.docx
2. Print the exact output path
3. Print which input files were used
4. Print which listed files were missing
5. Confirm that no model was retrained
