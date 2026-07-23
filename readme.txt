Create a detailed Word document named:

Churn_Model_Evaluation_and_Recommendation.docx

Use the existing project files and generated model outputs in the current workspace. Do not retrain any model and do not modify the existing Python scripts or CSV files.

Use the available outputs for these models:

- Logistic Regression
- Decision Tree
- Random Forest
- XGBoost
- HistGradientBoosting

Use the latest values from:

- logistic_regression_metrics.csv
- decision_tree_metrics.csv
- random_forest_metrics.csv
- xgboost_metrics.csv
- hist_gradient_boosting_metrics.csv
- model_comparison_all_models.csv
- logistic_regression_top_churn_drivers.csv
- decision_tree_top_churn_drivers.csv
- random_forest_top_churn_drivers.csv
- xgboost_top_churn_drivers.csv
- hist_gradient_boosting_top_churn_drivers.csv
- hist_gradient_boosting_top_behavioural_churn_drivers.csv
- any available feature-importance or permutation-importance files
- any existing charts in the model_visuals folder

Create the Word document using Python and save the Python script as:

create_churn_model_documentation.py

Use python-docx to generate the .docx file.

The document should be professional, business-friendly and understandable to both technical and non-technical readers.

Include the following sections.

1. Title Page

Title:
Churn Model Evaluation and Recommendation

Include:

- POC name
- Prepared date
- Author placeholder
- Dataset scope
- Account-level churn prediction
- Model evaluation summary

2. Executive Summary

Explain in plain English:

- The objective of the churn model
- That the model predicts account-level churn risk
- That the output includes churn probability, risk band and major churn drivers
- Models evaluated
- Current recommended model
- Important limitations and assumptions
- That model drivers show association, not confirmed business causation

3. Business Objective

Explain:

- Why churn prediction is useful
- How the output may support retention activity
- That the model is intended to identify accounts likely to churn within the defined future outcome window
- That recommendations should be based on business-approved retention actions

4. Dataset Design

Document the dataset grain:

- One row per ACCOUNT_ID per as-of date

Explain the current POC date windows:

- Feature start date: 2024-01-01
- As-of date: 2024-12-31
- Outcome start date: 2025-01-01
- Outcome end date: 2025-03-31

Explain in layman terms:

- The model studies account behaviour during the 12-month feature window
- Only accounts active as of the as-of date are included
- Churn is observed during the following three-month outcome window
- Accounts already exited before or on the as-of date are excluded from the cohort

Include the target definition:

- target_churn = 1 when the account closes during the outcome window or has a qualifying external rollover during the outcome window
- target_churn = 0 otherwise
- Death exits are excluded from model training

Document the dataset size and target distribution from the actual files.

Expected approximate values:

- Total training-eligible accounts: 793,915
- Non-churn: 686,176
- Churn: 107,739
- Churn rate: approximately 13.57%

Use the actual latest values from the files if they differ.

5. Feature Categories

Group and explain the features in business language.

Include:

Account characteristics:
- account tenure
- account type
- product ID
- scheme ID

Transaction behaviour:
- transaction count
- distinct transaction types
- reversal count
- days since last account transaction

Contribution behaviour:
- contribution transaction count
- contribution amount
- active contribution months
- days since last contribution

Rollover behaviour:
- rollover count
- rollover amount
- days since last rollover

Partial-withdrawal behaviour:
- partial-withdrawal count
- partial-withdrawal amount
- days since last partial withdrawal
- significant partial-withdrawal count
- significant partial-withdrawal amount
- significant partial-withdrawal flag
- days since last significant partial withdrawal

Explain that the current significant partial-withdrawal threshold is a POC threshold and requires business confirmation.

Explain that product_id and scheme_id are categorical account-context variables, not numerical amounts.

6. Leakage Prevention

Explain clearly that the following outcome or audit fields were excluded from model training:

- account status after the outcome period
- account exit date
- account closed outcome flag
- external rollover outcome flag
- external rollover outcome count
- external rollover outcome amount
- external exit type and reason fields
- death outcome flag
- training exclusion flag
- feature and outcome date fields
- ACCOUNT_ID

Explain why these columns cannot be model features:

- They describe or directly reveal the future outcome
- Including them would cause target leakage
- Leakage would create unrealistically high model performance

7. Algorithm Definitions

Create a separate subsection for each algorithm.

For each algorithm include:

- Plain-English definition
- How it works
- Main advantages
- Main disadvantages
- Interpretability
- Suitability for this churn dataset
- Typical production considerations

Algorithms:

A. Logistic Regression

Explain:

- Linear probabilistic classification model
- Coefficients indicate positive or negative association
- Easy to explain
- Strong baseline
- May miss complex nonlinear patterns

B. Decision Tree

Explain:

- Uses rule-based splits
- Easy to visualize and explain
- Can model nonlinear relationships
- May overfit and be unstable

C. Random Forest

Explain:

- Ensemble of many decision trees
- Reduces overfitting compared with one tree
- Strong performance on tabular data
- Less directly interpretable than one decision tree
- Slower than Logistic Regression and Decision Tree

D. XGBoost

Explain:

- Sequentially builds trees to correct previous errors
- Strong predictive performance
- Handles nonlinear relationships and feature interactions
- Requires tuning
- Explainability normally uses feature importance or SHAP

E. HistGradientBoosting

Explain:

- Histogram-based gradient-boosting algorithm
- Efficient for large tabular datasets
- Can handle complex nonlinear relationships
- Does not provide standard feature importance directly
- Permutation importance is used for interpretation

8. Evaluation Metrics

Define each metric in simple language and include its formula where appropriate.

Include:

- Accuracy
- Precision for churn
- Recall for churn
- F1-score
- ROC-AUC
- PR-AUC / Average Precision
- Confusion Matrix
- Training time
- Prediction time

Explain why PR-AUC is important for this dataset:

- Churn is the minority class
- Approximately 13.57% of accounts churn
- Accuracy alone can be misleading
- PR-AUC focuses more directly on churn detection quality

Explain the business interpretation of precision and recall:

- High precision means fewer false churn alerts
- High recall means fewer actual churn accounts are missed

9. Model Performance Comparison

Read the latest model metrics from model_comparison_all_models.csv.

Create a formatted comparison table with:

- Model
- ROC-AUC
- PR-AUC
- Accuracy
- Precision for churn
- Recall for churn
- F1-score for churn
- Training time
- Prediction time

Highlight:

- Best ROC-AUC
- Best PR-AUC
- Best recall
- Best F1-score
- Fastest prediction
- Best overall balanced model

Use conditional formatting or bold text in the Word table to identify the winners.

Based on the latest results currently available, explain that:

- Random Forest has the best ROC-AUC and F1-score
- XGBoost has the best PR-AUC and recall
- Logistic Regression has the fastest prediction
- The current production-balanced recommendation may favour XGBoost
- Random Forest remains a strong candidate when maximum F1 and ROC-AUC are prioritised
- Final selection must be based on business priority, threshold performance, stability and explainability

Do not hard-code these conclusions if the actual CSV values differ. Derive them from the files.

10. Detailed Model Interpretation

For each model, include:

- Main performance strengths
- Main performance weaknesses
- Whether it is suitable as:
  - baseline model
  - explainable model
  - production candidate
  - challenger model

11. Important Churn Drivers

Read the latest churn-driver files.

Separate the driver discussion into:

A. Behavioural churn drivers

Examples may include:

- transaction frequency
- account tenure
- partial-withdrawal activity
- days since last partial withdrawal
- contribution activity
- rollover activity
- reversal transaction count
- no-history indicators

B. Product and scheme associations

Examples may include:

- product_id categories
- scheme_id categories

State clearly:

- Product and scheme results are associations
- They may reflect product design, customer mix, business process or data distribution
- They should not automatically be interpreted as causes of churn
- Categories with low account counts should be treated cautiously

Create a table with:

- Rank
- Feature
- Importance or coefficient
- Direction, where available
- Feature group
- Plain-English interpretation
- Business validation required

Use only actual available drivers from the generated CSV files.

12. Partial-Withdrawal Interpretation

Explain:

- Partial withdrawal is currently treated as a behavioural feature
- It does not automatically set target_churn to 1
- Raw partial-withdrawal features capture all qualifying events
- Significant partial-withdrawal features apply the POC amount threshold
- The current threshold should be confirmed with business
- A percentage-of-account-balance threshold would be preferable if validated historical fund-balance data becomes available

13. Model Recommendation

Create a clear recommendation section.

Include:

Recommended primary model:
- Derive from actual metrics and comparison results

Recommended baseline/challenger:
- Logistic Regression as explainable baseline
- Random Forest or XGBoost as primary/challenger depending on actual metrics

Explain the recommendation based on:

- PR-AUC
- Recall
- F1-score
- Runtime
- Explainability
- Model stability
- Operational complexity

Include a recommendation such as:

- XGBoost may be preferred for production balance if it has the best PR-AUC and recall while maintaining similar F1
- Random Forest may be preferred if maximum ROC-AUC and F1 are the main priorities
- Logistic Regression should remain as a transparent benchmark

Do not state that any model is production-ready without additional validation.

14. Risk Threshold and Risk Bands

Explain that the default 0.50 probability threshold may not be the final business threshold.

Describe possible risk bands, for example:

- Low risk: probability below 0.30
- Medium risk: probability from 0.30 to below 0.70
- High risk: probability 0.70 or above

Clearly mark these as examples requiring business approval.

Explain that the final threshold should be chosen based on:

- Retention-team capacity
- Cost of false positives
- Cost of missed churn accounts
- Desired recall
- Desired precision
- Number of accounts that can be contacted

15. Account-Level Model Output

Describe the expected account-level output:

- ACCOUNT_ID
- churn_probability
- predicted_churn
- risk_band
- top churn drivers
- model version
- scoring date

Explain that the LLM recommendation layer may consume this output.

16. LLM Recommendation Layer

Explain that the LLM does not calculate the churn risk score.

The ML model provides:

- churn probability
- churn prediction
- risk band
- churn drivers

The LLM recommendation layer may then:

- Select or phrase business-approved retention actions
- Generate a short account-level explanation
- Provide an account-level recommended next action
- Produce output suitable for Power BI, CRM or adviser workflows

List LLM prerequisites:

- Final ML output
- Business-approved recommendation catalogue
- Mapping between churn drivers, risk bands and approved actions
- Eligibility and exclusion rules
- Approved wording and disclaimers
- Azure OpenAI or LLM access
- Expected output format
- Business reviewers

17. LLM Evaluation Metrics

Include recommended LLM evaluation criteria:

- Recommendation relevance
- Groundedness
- Consistency
- Factual correctness
- Compliance with approved action list
- Hallucination rate
- Business-user acceptance rate
- Recommendation coverage
- Human-review pass rate
- Response time
- Cost per recommendation

Explain that these are different from ML evaluation metrics.

18. Limitations and Assumptions

Document the known POC limitations:

- Only one as-of-date cohort is currently used
- A random stratified split is weaker than a true future-time validation
- Recent historical data coverage is limited
- Historical balance/FUM data is not currently reliable enough for V1
- Full versus partial rollover is not completely validated
- Partial-withdrawal threshold requires business confirmation
- Product and scheme effects may be influenced by customer mix
- Model drivers show association, not causation
- Model performance may change in future time periods
- Business thresholds and risk bands are not yet final

19. Recommended Next Steps

Include:

1. Complete XGBoost and HistGradientBoosting comparison
2. Confirm the final candidate model
3. Perform probability calibration
4. Select business probability threshold
5. Define approved risk bands
6. Validate performance by product and scheme
7. Validate performance across different account groups
8. Build additional monthly historical cohorts
9. Perform out-of-time validation
10. Complete business review of churn drivers
11. Confirm partial-withdrawal logic and threshold
12. Confirm full versus partial rollover logic
13. Define model monitoring metrics
14. Define model refresh frequency
15. Build account-level scoring output
16. Develop LLM recommendation POC after prerequisites are available

20. Appendix

Include:

- Confusion matrices if available
- ROC curve and Precision-Recall curve images
- Feature-importance charts
- Behavioural churn-driver chart
- Churn-probability distribution
- Threshold precision/recall/F1 chart
- Full model comparison table
- File inventory
- Glossary of technical terms

Document formatting requirements:

- Use professional headings and subheadings
- Add page numbers
- Add a table of contents
- Use readable tables
- Use landscape orientation for wide model comparison tables if needed
- Use captions below charts
- Add a document version section
- Add a footer stating:
  “POC results – subject to business validation and out-of-time testing”
- Do not use overly technical language without explanation
- Add plain-English callout boxes for important findings
- Make the recommendation section visually prominent

If some files are missing:

- Continue using the available files
- Add a note in the document stating which inputs were unavailable
- Do not invent metric values or churn drivers

After generating the document:

1. Save it as Churn_Model_Evaluation_and_Recommendation.docx
2. Print the complete file path
3. Print the list of data files and charts used
4. Print any missing inputs
5. Confirm the Word file was created successfully
6. Do not retrain any model
