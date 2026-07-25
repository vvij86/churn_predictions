Here’s a simple demo flow you can use. The key is: don’t open every file. Walk them through the process in order and open only the important files.

1. Start with the business objective

Say:

> “The objective was to build a proof-of-concept model that predicts which active accounts may churn in the next three months, using their previous 12 months of behaviour.”



Then explain the timeline:

> “I used one year of historical behaviour to create features, and the following three months to create the actual churn outcome.”




---

2. Show the original SQL dataset creation

Open:

Full_Dataset_Query.sql

or the final version you actually used, such as:

Full_Dataset_Query_3.sql

Say:

> “This query creates the full account-level modelling dataset. It produces one row per account and initially returns 41 columns.”



Explain the 41 columns in three groups:

Account identifiers and behavioural features

Examples:

account_id

as_of_date

account_tenure_days

transaction counts and recency

contribution counts and amounts

rollover behaviour

partial-withdrawal behaviour

product and scheme


Outcome and audit fields

Examples:

account exit date

closure flag

external rollover outcome

death outcome flag

exclusion flag


Target

target_churn

Say:

> “The 41-column dataset is useful for validation and target creation, but not all 41 columns are given to the model.”




---

3. Show the raw exported dataset

Open briefly:

model_dataset.csv

or:

dataset.csv

Say:

> “This is the SQL output exported into CSV. It contains the account features, outcome fields and target.”



Do not scroll through thousands of rows. Just show the header and a few records.


---

4. Show dataset validation

Open:

validate_churn_dataset.py

Then show:

churn_model_dataset_validation_summary.csv

Say:

> “Before modelling, I validated the dataset for row count, duplicate account IDs, missing values, target distribution and data quality.”



Mention your key checks:

one row per account;

no duplicate ACCOUNT_ID;

no missing account IDs;

churn and non-churn distribution;

excluded records removed;

feature columns checked.


You can say:

> “After exclusions, the trainable dataset had approximately 794,000 accounts, with around 13.6% churn.”




---

5. Show preprocessing and train/test split

Open:

preprocess_and_split_model_dataset.py

or:

prepare_model_dataset.py

Say:

> “This script separates model-safe features from target-building fields and removes leakage.”



Explain simply:

Outcome columns removed.

target_churn separated as the label.

ACCOUNT_ID retained separately.

Constant fields such as account_type_code removed.

Data split into training and test sets.

Same stratified split used for all models.


Then show these output files:

churn_X_train.csv
churn_X_test.csv
churn_y_train.csv
churn_y_test.csv
churn_train_account_ids.csv
churn_test_account_ids.csv

Explain:

> “X contains the behavioural input fields. Y contains the actual churn result. Account ID files allow predictions to be mapped back to the correct accounts.”



Also mention:

> “The test accounts were not used to train the model.”




---

6. Show the model training scripts

You have separate scripts for each model:

train_logistic_regression.py
train_decision_tree.py
train_random_forest.py
train_xgboost.py
train_hist_gradient_boosting.py

Say:

> “I trained five different classification algorithms using the same training and test datasets. This made the comparison fair.”



Briefly explain each:

Logistic Regression: simple and explainable baseline.

Decision Tree: rule-based model.

Random Forest: many trees combined.

XGBoost: sequential boosting model.

HistGradientBoosting: efficient gradient boosting model.


Do not explain every code line. Show the same main pattern in one script:

model.fit(X_train, y_train)

Then:

predict_proba(X_test)

Say:

> “The model is trained on the training set, then generates a churn probability for each account in the test set.”




---

7. Show the saved model pipelines

Examples:

logistic_regression_pipeline.joblib
decision_tree_pipeline.joblib
random_forest_pipeline.joblib
xgboost_pipeline.joblib
hist_gradient_boosting_pipeline.joblib

Say:

> “Each joblib file contains the trained preprocessing and model pipeline. These saved pipelines can later be reused to score new account datasets without retraining.”



This is important for explaining the scoring process.


---

8. Show one prediction output

Open one selected model prediction file, preferably XGBoost or Random Forest:

xgboost_test_predictions.csv

or:

random_forest_test_predictions.csv

Explain the columns:

ACCOUNT_ID
actual_target
predicted_target
churn_probability

Say:

> “This is the account-level result. It shows the actual outcome, the model prediction and the predicted churn probability.”



Example explanation:

> “A probability of 0.82 means the model estimated an 82% churn risk. At the current 0.5 threshold, that account is classified as predicted churn.”




---

9. Show model metrics

Open examples such as:

logistic_regression_metrics.csv
random_forest_metrics.csv
xgboost_metrics.csv
hist_gradient_boosting_metrics.csv
decision_tree_metrics.csv

Say:

> “Each model was evaluated using the same metrics: ROC-AUC, PR-AUC, precision, recall, F1-score and confusion matrix.”



Explain quickly:

Precision: of accounts flagged, how many actually churned?

Recall: of actual churners, how many were found?

F1: balance of precision and recall.

ROC-AUC: how well churners are ranked above non-churners.

PR-AUC: performance focused on the churn class.


You can use the Logistic Regression example:

> “The Logistic Regression correctly identified 18,548 churners, produced 689 false alerts and missed 3,000 churners.”




---

10. Show the full model comparison

Open:

model_comparison_all_models.csv

This should be one of the main files in the demo.

Say:

> “This file compares all five models side by side using the same test dataset.”



Then explain your recommendation:

> “Random Forest gave the strongest overall ROC-AUC and F1 result. XGBoost gave the strongest PR-AUC and recall and may offer a better production balance. For the POC, both are strong candidates, with the final choice depending on whether the business prioritises maximum detection, fewer false alerts or operational speed.”



Keep the recommendation aligned with what is written in your documentation.


---

11. Show churn drivers

Open one or two files:

xgboost_top_churn_drivers.csv
xgboost_behavioural_top_churn_drivers.csv
random_forest_top_churn_drivers.csv
logistic_regression_top_churn_drivers.csv

Say:

> “These files show which features had the strongest influence on the prediction.”



Examples could include:

transaction inactivity;

days since last contribution;

rollover activity;

partial withdrawals;

account tenure;

product and scheme.


Add this disclaimer:

> “These are predictive relationships. They do not prove that a behaviour directly causes churn.”




---

12. Show visuals

Open the folder:

model_visuals

Or show visuals created by:

create_logistic_model_visuals.py

Useful visuals include:

ROC curve;

precision-recall curve;

confusion matrix;

feature importance chart;

model comparison chart.


Say:

> “The visuals provide a more understandable representation of model performance and the main drivers.”




---

13. Show the documentation

Open:

Churn_Model_Evaluation_and_Recommendation.docx

or:

Churn_Model_Evaluation_Comparison_and_Recommendation...

Say:

> “This document records the dataset design, feature logic, models tested, evaluation results, assumptions, recommendation and POC limitations.”



You can mention the supporting scripts:

create_churn_model_documentation.py
create_churn_model_evaluation_document.py


---

14. Show the scoring query as the next step

Open:

Scoring_Dataset.sql

Say:

> “This is the scoring version of the dataset query. It uses the same feature calculations but removes target and future-outcome columns.”



Explain the process:

1. Change the feature start and as-of dates.


2. Generate the latest account-level features.


3. Pass the output through the saved pipeline.


4. Produce churn probability and predicted churn.


5. Later compare with actual three-month outcomes.




---

Simple end-to-end summary to say

> “First, I created a 41-column account-level dataset using SQL. Then I validated the data, removed leakage and separated the behavioural features from the churn target. I created a fixed training and test split and used the same split to train five algorithms. Each model generated account-level churn probabilities, which I evaluated using precision, recall, F1, ROC-AUC, PR-AUC and confusion matrices. I then compared the models, reviewed the churn drivers, saved the trained pipelines and created a separate scoring query for future predictions.”



Recommended file-opening order

Use only these during the main demo:

1. Full_Dataset_Query.sql


2. churn_model_dataset_validation_summary.csv


3. preprocess_and_split_model_dataset.py


4. churn_X_train.csv


5. One training script, preferably train_xgboost.py


6. xgboost_test_predictions.csv


7. model_comparison_all_models.csv


8. xgboost_top_churn_drivers.csv


9. Churn_Model_Evaluation_and_Recommendation.docx


10. Scoring_Dataset.sql



That gives a clear story without getting buried in files.
