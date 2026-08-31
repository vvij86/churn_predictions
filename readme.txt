Copilot Prompt — Step 12: Model Performance Monitoring POC

Create a new Databricks notebook named:

"12_model_performance_monitoring_poc.ipynb"

This notebook should continue from the existing MLOps POC.

Current State

Already completed:

- Model registration in Unity Catalog
- Version 1 = Champion
- Version 2 = Candidate
- Batch scoring using "@Champion"
- Model output schema
- Unity Catalog output table
- Databricks Job scheduling POC
- Prediction monitoring
- Data / feature drift monitoring

Existing datasets:

Test features:

"Test_ds/churn_X_test.csv"

Actual labels:

"Test_ds/churn_y_test.csv"

Existing Champion registered model:

"superdata_au_dev.mlops.superannuation_churn_model"

Use the "Champion" alias dynamically.

Purpose

Demonstrate model performance monitoring by comparing the Champion model predictions against actual known outcomes.

The goal is to calculate current model performance metrics and compare them against a reference/baseline performance level.

Do not retrain the model.
Do not change Champion/Candidate aliases.
Do not create another model version.

Step 12 - Model Performance Monitoring

Create a Markdown heading:

"# Step 12 - Model Performance Monitoring POC"

Explain in simple terms:

Prediction monitoring checks whether model outputs changed.

Feature drift monitoring checks whether input data changed.

Performance monitoring checks whether the model is still making accurate predictions when actual outcomes become available.

Explain that in a real churn use case, actual churn outcomes may only become available after the defined outcome window has completed.

1. Import Required Libraries

Import:

import pandas as pd
import numpy as np
import mlflow

from mlflow.tracking import MlflowClient

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix
)

Configure:

mlflow.set_registry_uri("databricks-uc")

REGISTERED_MODEL_NAME = "superdata_au_dev.mlops.superannuation_churn_model"
MODEL_ALIAS = "Champion"

client = MlflowClient()

2. Resolve Current Champion Model Version

Retrieve:

champion_details = client.get_model_version_by_alias(
    REGISTERED_MODEL_NAME,
    MODEL_ALIAS
)

Print:

- model name
- alias
- actual model version
- run ID
- status

Store:

champion_version = champion_details.version

Do not hardcode Version 1.

3. Load Champion Model

Create:

champion_uri = f"models:/{REGISTERED_MODEL_NAME}@Champion"

Load:

model = mlflow.sklearn.load_model(champion_uri)

Print the loaded model type.

4. Load Test Features and Actual Outcomes

Load:

"Test_ds/churn_X_test.csv"

into:

"X_test"

Load:

"Test_ds/churn_y_test.csv"

into:

"y_test"

Convert y_test to a 1-dimensional Series/array if necessary.

Validate that X_test and y_test row counts match.

Print:

- total records
- actual churn count
- actual non-churn count
- actual churn rate

5. Generate Current Champion Predictions

Generate:

y_pred = model.predict(X_test)

If supported:

y_prob = model.predict_proba(X_test)[:, 1]

Do not retrain the model.

6. Calculate Current Performance Metrics

Calculate:

- Accuracy
- Precision
- Recall
- F1 Score
- ROC AUC
- Confusion Matrix

Store results in:

current_metrics

Display clearly.

For confusion matrix, derive and print:

- True Negative
- False Positive
- False Negative
- True Positive

Add simple Markdown explanation of why False Negatives may be important for churn:

A False Negative means an account that actually churned was predicted as non-churn.

7. Obtain Baseline Performance

Try to retrieve the original baseline metrics from the MLflow run associated with the Champion version.

Use:

baseline_run_id = champion_details.run_id
baseline_run = client.get_run(baseline_run_id)

Read available metrics such as:

- accuracy
- precision
- recall
- f1_score
- roc_auc

If the expected metrics are not available in that registered model run, fall back to clearly defined POC baseline metrics calculated from the same existing baseline model evaluation workflow.

Do not fabricate values.

Clearly indicate whether baseline values came from MLflow or were recalculated.

Store baseline metrics in:

baseline_metrics

8. Compare Baseline vs Current Performance

Create a dataframe with:

- Metric
- Baseline Value
- Current Value
- Absolute Change
- Percentage Change

Include:

- Accuracy
- Precision
- Recall
- F1
- ROC AUC

Display the table.

9. Define POC Performance-Degradation Thresholds

Use example thresholds:

- Accuracy drop > 5% → WARNING
- Precision drop > 10% → WARNING
- Recall drop > 10% → WARNING
- F1 drop > 10% → WARNING
- ROC AUC drop > 5% → WARNING

Interpret these as relative percentage drops where practical.

Add this Markdown note:

POC Note: These thresholds are examples only. Final production thresholds must be agreed based on business impact, model behaviour, and risk tolerance.

10. Create Performance Monitoring Status

Create a dataframe:

"performance_monitoring_summary"

with columns:

- metric
- baseline_value
- current_value
- change
- percentage_change
- allowed_drop_threshold
- status

Status should be:

- "OK"
- "WARNING"

Display it with WARNING metrics first.

11. Confusion Matrix Monitoring

Create a small comparison or summary showing:

- TN
- FP
- FN
- TP
- False Negative Rate
- False Positive Rate

Explain:

For a churn model, increasing False Negatives may be particularly important because members likely to churn could be missed by retention intervention.

12. Overall Model Health Status

Define simple POC logic:

- No warnings → "HEALTHY"
- 1 or 2 warnings → "REVIEW"
- More than 2 warnings → "DEGRADED"

Print:

Overall model health: HEALTHY / REVIEW / DEGRADED

Clearly state this is POC logic only.

13. Save Monitoring Results

Use current UTC date in "YYYYMMDD" format.

Save:

"Output_Metrics/model_performance_monitoring_summary_<date>.csv"

Also optionally save:

"Output_Metrics/model_performance_confusion_matrix_<date>.csv"

Print the generated paths.

14. Explain Production Performance Monitoring

Add a Markdown section explaining that in production:

1. Batch scoring happens first.
2. Actual churn outcome may become available weeks/months later.
3. Predictions are joined with actual outcomes.
4. Model metrics are recalculated.
5. Performance degradation can trigger investigation or retraining.

Explain that performance monitoring therefore normally has a delay compared with prediction monitoring.

15. Relationship Between Monitoring Types

Add a simple Markdown table:

Monitoring Type| Main Question
Prediction Monitoring| Have model outputs changed?
Feature Drift Monitoring| Has input data changed?
Performance Monitoring| Is the model still accurate?

16. Final Summary

Print:

- Champion model version
- Baseline F1
- Current F1
- Baseline Recall
- Current Recall
- Baseline ROC AUC
- Current ROC AUC
- Number of WARNING metrics
- Overall model health

Print:

"Step 12 completed successfully. Model performance monitoring has been demonstrated."

Important Requirements

- Do not retrain the model.
- Do not create a new model version.
- Do not modify Champion/Candidate aliases.
- Use "@Champion" dynamically.
- Use actual y_test outcomes for the POC.
- Do not fabricate baseline metrics.
- Clearly distinguish POC thresholds from production thresholds.
- Add simple Markdown explanations before each major section.
