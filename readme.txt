Copilot Prompt — Step 4: Evaluate Existing Model and Log Metrics to MLflow

Create a new Databricks notebook named:

"04_evaluate_model_and_log_mlflow.ipynb"

This notebook should contain only Step 4 of the MLOps POC.

Purpose

Reuse the existing trained Logistic Regression model and test dataset to:

1. Generate predictions
2. Calculate evaluation metrics
3. Create an MLflow experiment
4. Log the evaluation metrics and model information into MLflow

Do not register the model in Unity Catalog yet.
Model registration will be done in the next step.

Existing Inputs

Use these existing files:

Model:

"Models/logistic_regression_pipeline.joblib"

Test data:

"Test_ds/churn_X_test.csv"

"Test_ds/churn_y_test.csv"

Step 4 - Evaluate Model and Log Metrics to MLflow

Create a Markdown section explaining that MLflow experiment tracking stores model runs, parameters, metrics and artifacts so different model runs can later be compared.

1. Import Required Libraries

Import:

- pandas
- numpy
- joblib
- mlflow
- mlflow.sklearn

From sklearn.metrics import:

- accuracy_score
- precision_score
- recall_score
- f1_score
- roc_auc_score
- confusion_matrix

2. Load Existing Test Dataset

Load:

"Test_ds/churn_X_test.csv"

into:

"X_test"

Load:

"Test_ds/churn_y_test.csv"

into:

"y_test"

Ensure y_test is converted to a 1-dimensional array/Series if required.

3. Load Existing Logistic Regression Model

Load:

"Models/logistic_regression_pipeline.joblib"

using joblib.

Store it in:

"model"

Do not retrain the model.

4. Generate Predictions

Generate:

y_pred = model.predict(X_test)

If "predict_proba()" is available, generate positive-class probabilities:

y_probability = model.predict_proba(X_test)[:, 1]

5. Calculate Evaluation Metrics

Calculate:

- Accuracy
- Precision
- Recall
- F1 Score
- ROC AUC
- Confusion Matrix

Use safe handling for divide-by-zero where appropriate.

Display all metrics clearly.

Also display the confusion matrix.

6. Explain Metrics

Add a Markdown section briefly explaining:

- Accuracy = overall percentage of correct predictions
- Precision = of members predicted as churn, how many actually churned
- Recall = of members who actually churned, how many the model identified
- F1 = balance between precision and recall
- ROC AUC = model's overall ability to distinguish churn vs non-churn
- Confusion Matrix = counts of TP, TN, FP and FN

7. Create MLflow Experiment

Create or use an MLflow experiment named:

"/Shared/MLOps_POC_Superannuation_Churn"

Use:

mlflow.set_experiment(...)

Do not fail if the experiment already exists.

8. Start an MLflow Run

Start a new MLflow run.

Use a meaningful run name such as:

"logistic_regression_existing_model_evaluation"

Log the following parameters:

- model_type = LogisticRegression
- model_source = existing_joblib
- poc_type = MLOps
- dataset = churn_test_dataset

Log these metrics:

- accuracy
- precision
- recall
- f1_score
- roc_auc

Also log useful tags:

- business_use_case = superannuation_churn
- environment = dev
- poc_stage = model_evaluation

9. Log Existing Model as MLflow Artifact

Log the loaded sklearn model using:

mlflow.sklearn.log_model(...)

Use an artifact path such as:

"model"

Do NOT register the model in Unity Catalog in this notebook.

10. Print MLflow Run Information

At the end print:

- Experiment name
- Run ID
- Model type
- Accuracy
- Precision
- Recall
- F1
- ROC AUC

Also print:

"Step 4 completed successfully. Model evaluation and MLflow experiment logging completed."

Important Requirements

- Do not retrain the model.
- Do not register the model in Unity Catalog yet.
- Do not create model versions yet.
- Do not create Champion/Candidate aliases yet.
- Keep the notebook focused only on evaluation and MLflow tracking.
- Add simple Markdown explanations before each major code section so the notebook is easy to understand later.
