Copilot Prompt — Step 3: Load Existing Model and Test Data

Create a new Databricks notebook named:

"03_load_existing_model_and_test_data.ipynb"

This notebook should contain only Step 3 of the MLOps POC.

Purpose

Load the already trained Logistic Regression model and the existing test dataset so they can be reused for MLflow model registration and scoring in later steps.

Do not retrain the model.

Existing Files

Model:

"Models/logistic_regression_pipeline.joblib"

Test files:

"Test_ds/churn_X_test.csv"

"Test_ds/churn_y_test.csv"

"Test_ds/churn_test_account_ids.csv"

Notebook Content

Create a Markdown heading:

"# Step 3 - Load Existing Model and Test Dataset"

Explain briefly that the model has already been trained previously and this POC will reuse it instead of training again.

1. Import Libraries

Import:

- pandas
- joblib
- os

2. Load Test Data

Load:

- "churn_X_test.csv" into "X_test"
- "churn_y_test.csv" into "y_test"
- "churn_test_account_ids.csv" into "test_account_ids"

Print the shape of each dataset.

Display the first 5 rows of each.

3. Validate Data

Print:

- number of rows in X_test
- number of rows in y_test
- number of account IDs

Confirm that all three row counts match.

If they do not match, print a warning.

4. Load Existing Logistic Regression Model

Load:

"Models/logistic_regression_pipeline.joblib"

using "joblib.load()".

Store it as:

"model"

Print:

- model type
- model object
- pipeline steps if it is an sklearn Pipeline

5. Basic Validation

Confirm that the model supports:

- "predict()"
- "predict_proba()"

Print a message indicating whether each method is available.

Do not run full model evaluation yet.

Do not register the model.

Do not create an MLflow experiment.

Do not create a model version.

At the end print:

"Step 3 completed successfully. Existing model and test dataset are ready for the MLOps POC."
