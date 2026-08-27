Copilot Prompt — Step 6: Tune Candidate Model, Compare, Register Version 2, and Assign Aliases

Create a new Databricks notebook named:

"06_tune_candidate_register_version2_and_aliases.ipynb"

This notebook should continue from the already completed MLOps POC.

Current State

The following steps are already completed:

- Unity Catalog access verification
- Existing Logistic Regression model loaded
- Model evaluated and logged to MLflow
- Baseline model registered in Unity Catalog

The registered model already exists as:

"superdata_au_dev.mlops.superannuation_churn_model"

and currently has:

"Version 1"

Do not recreate Version 1.

Purpose

Create a meaningful Version 2 by:

1. Loading the existing baseline model
2. Loading training and test datasets
3. Tuning a new Logistic Regression candidate using GridSearchCV
4. Comparing baseline vs tuned candidate
5. Logging the candidate to MLflow
6. Registering the candidate under the same Unity Catalog model name
7. Creating a new model version
8. Assigning Champion/Candidate aliases

Hyperopt is not installed.

Do not use Hyperopt or SparkTrials.

Use scikit-learn "GridSearchCV".

---

Step 6 - Tune Candidate and Create Model Version 2

Add a Markdown heading:

"# Step 6 - Tune Candidate Model and Create Version 2"

Explain that Version 1 represents the existing baseline model and this notebook creates a genuinely different candidate model through hyperparameter tuning.

Also explain that registering the candidate under the same Unity Catalog model name creates a new model version automatically.

1. Import Required Libraries

Import:

import pandas as pd
import numpy as np
import joblib
import mlflow
import mlflow.sklearn

from sklearn.base import clone
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix
)

from mlflow.models import infer_signature
from mlflow.tracking import MlflowClient

Configure:

mlflow.set_registry_uri("databricks-uc")

REGISTERED_MODEL_NAME = "superdata_au_dev.mlops.superannuation_churn_model"

client = MlflowClient()

2. Verify Existing Version 1

Retrieve existing model versions from:

"superdata_au_dev.mlops.superannuation_churn_model"

Display:

- version
- run_id
- status
- creation timestamp
- aliases if available

Confirm that Version 1 exists.

Print:

"Baseline Unity Catalog model version found: Version 1"

Do not recreate Version 1.

3. Load Existing Data

Load:

Training:

"Training_ds/churn_X_train.csv"

"Training_ds/churn_y_train.csv"

Test:

"Test_ds/churn_X_test.csv"

"Test_ds/churn_y_test.csv"

Store as:

- "X_train"
- "y_train"
- "X_test"
- "y_test"

Convert y_train and y_test to one-dimensional Series/arrays if required.

Print dataset shapes.

Validate that:

- X_train rows match y_train
- X_test rows match y_test

4. Load Existing Baseline Model

Load:

"Models/logistic_regression_pipeline.joblib"

into:

"baseline_model"

Print:

- model type
- pipeline steps

Do not retrain the baseline model.

5. Evaluate Baseline Model

Run:

baseline_pred = baseline_model.predict(X_test)
baseline_prob = baseline_model.predict_proba(X_test)[:, 1]

Calculate:

- Accuracy
- Precision
- Recall
- F1
- ROC AUC
- Confusion Matrix

Store metrics in:

"baseline_metrics"

Display them clearly.

6. Clone Existing Pipeline

Use:

candidate_pipeline = clone(baseline_model)

Explain that this allows the candidate to reuse exactly the same preprocessing pipeline while changing Logistic Regression hyperparameters.

Inspect the pipeline steps and dynamically identify the Logistic Regression step name.

Do not assume the estimator step is called "classifier".

7. Define Small Hyperparameter Grid

Create a small POC grid for Logistic Regression.

Use values similar to:

C = [0.1, 0.5, 1.0, 2.0]

class_weight = [None, "balanced"]

max_iter = [500, 1000]

Build the parameter names dynamically using the detected Logistic Regression pipeline step.

For example:

"<step_name>__C"

"<step_name>__class_weight"

"<step_name>__max_iter"

Print the generated parameter grid.

8. Run GridSearchCV

Configure:

GridSearchCV(
    estimator=candidate_pipeline,
    param_grid=param_grid,
    scoring="f1",
    cv=3,
    n_jobs=-1,
    verbose=1
)

If "n_jobs=-1" fails in Databricks/serverless, automatically retry with:

"n_jobs=1"

Fit using:

"X_train" and "y_train"

Store:

candidate_model = grid_search.best_estimator_

Print:

- best parameters
- best cross-validation F1 score

Add Markdown explaining that Hyperopt is not required for this small POC because GridSearchCV is enough to demonstrate model tuning.

9. Evaluate Tuned Candidate

Run predictions on X_test.

Calculate the same metrics:

- Accuracy
- Precision
- Recall
- F1
- ROC AUC
- Confusion Matrix

Store in:

"candidate_metrics"

10. Compare Baseline vs Candidate

Create a dataframe:

Model| Accuracy| Precision| Recall| F1| ROC AUC
Version 1 Baseline| ...| ...| ...| ...| ...
Tuned Candidate| ...| ...| ...| ...| ...

Display it.

Also print:

- Baseline F1
- Candidate F1
- Baseline ROC AUC
- Candidate ROC AUC

Do not automatically claim a production winner.

Add this Markdown note:

POC Note: Model selection in this notebook is only for demonstrating MLOps lifecycle management. Final production model selection must follow agreed business and ML evaluation criteria.

11. Save Tuned Candidate Model

Save:

"candidate_model"

as:

"Models/logistic_regression_tuned_candidate_pipeline.joblib"

Do not overwrite:

"Models/logistic_regression_pipeline.joblib"

Print the candidate model path.

12. Create Model Signature

Create:

input_example = X_test.head(5)

sample_predictions = candidate_model.predict(input_example)

signature = infer_signature(
    input_example,
    sample_predictions
)

Explain briefly what the model signature represents.

13. Log Candidate to MLflow

Use the existing experiment:

"/Shared/MLOps_POC_Superannuation_Churn"

Create a new run named:

"logistic_regression_tuned_candidate"

Log:

- best GridSearchCV parameters
- tuning_method = GridSearchCV
- cv_folds = 3
- optimization_metric = F1
- model_role = candidate
- environment = dev
- poc_stage = model_versioning

Log candidate metrics:

- accuracy
- precision
- recall
- f1_score
- roc_auc

Log the candidate model using:

model_info = mlflow.sklearn.log_model(
    sk_model=candidate_model,
    name="model",
    signature=signature,
    input_example=input_example
)

14. Register Candidate in Unity Catalog

Register the logged candidate using:

registered_candidate = mlflow.register_model(
    model_uri=model_info.model_uri,
    name=REGISTERED_MODEL_NAME
)

Do not hardcode Version 2.

Capture the actual returned version:

candidate_version = registered_candidate.version

Wait for the version to become READY if necessary.

Print:

- Registered model name
- Candidate version
- Run ID
- Status

Because Version 1 already exists, the expected result is normally Version 2, but use the actual returned version dynamically.

15. Assign Model Aliases

For this POC:

Assign Version 1 as:

"Champion"

Assign the newly registered candidate version as:

"Candidate"

Use:

client.set_registered_model_alias(
    name=REGISTERED_MODEL_NAME,
    alias="Champion",
    version="1"
)

and:

client.set_registered_model_alias(
    name=REGISTERED_MODEL_NAME,
    alias="Candidate",
    version=candidate_version
)

16. Verify Champion and Candidate

Retrieve both aliases:

champion = client.get_model_version_by_alias(
    REGISTERED_MODEL_NAME,
    "Champion"
)

candidate = client.get_model_version_by_alias(
    REGISTERED_MODEL_NAME,
    "Candidate"
)

Print:

Champion -> Version X
Candidate -> Version Y

Display:

- Alias
- Version
- Run ID
- Status

17. Show Alias-Based Model URIs

Create:

champion_uri = f"models:/{REGISTERED_MODEL_NAME}@Champion"
candidate_uri = f"models:/{REGISTERED_MODEL_NAME}@Candidate"

Print both.

Explain that downstream scoring can use "@Champion" instead of hardcoding a version number.

18. Final Summary

Print:

- Version 1 baseline metrics
- Candidate metrics
- Best candidate hyperparameters
- Best cross-validation F1
- Registered candidate version
- Champion version
- Candidate version

Print:

"Step 6 completed successfully. Tuned candidate model created, registered as a new Unity Catalog version, and Champion/Candidate aliases assigned."

Important Requirements

- Do not recreate Version 1.
- Do not delete existing model versions.
- Do not overwrite the baseline joblib model.
- Do not use Hyperopt.
- Do not use SparkTrials.
- Keep the tuning grid intentionally small.
- Reuse the existing preprocessing pipeline.
- Do not create batch scoring yet.
- Do not implement monitoring yet.
- Use Unity Catalog aliases instead of deprecated Staging/Production stages.
- Add simple Markdown explanations before each major section.
