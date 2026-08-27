Copilot Prompt — Step 7: Batch Scoring Using Champion Alias

Create a new Databricks notebook named:

"07_batch_scoring_using_champion_alias.ipynb"

This notebook should continue from the existing MLOps POC.

Current State

The registered model already exists in Unity Catalog as:

"superdata_au_dev.mlops.superannuation_churn_model"

Current aliases:

- Version 1 → "Champion"
- Version 2 → "Candidate"

The purpose of this notebook is to demonstrate batch scoring using the "Champion" alias.

Do not hardcode Version 1 for scoring.

Purpose

Demonstrate how a production-style batch scoring process can:

1. Load the currently approved model using the "Champion" alias
2. Load scoring/test data
3. Generate churn predictions and probabilities
4. Create business-friendly scoring output
5. Capture model/version metadata with every prediction
6. Prepare the result for later persistence to a Gold/output table

Do not create a Databricks Job yet.
Do not implement monitoring yet.

Step 7 - Batch Scoring Using Champion Model

Create a Markdown heading:

"# Step 7 - Batch Scoring Using Champion Alias"

Explain that downstream scoring should use:

"@Champion"

instead of a hardcoded version such as Version 1.

Explain that if the Champion alias later moves to another version, the scoring code does not need to change.

1. Import Required Libraries

Import:

import pandas as pd
import numpy as np
import mlflow
from datetime import datetime, timezone
from mlflow.tracking import MlflowClient

Configure:

mlflow.set_registry_uri("databricks-uc")

REGISTERED_MODEL_NAME = "superdata_au_dev.mlops.superannuation_churn_model"
CHAMPION_ALIAS = "Champion"

client = MlflowClient()

2. Verify Current Champion Version

Retrieve:

champion_version_details = client.get_model_version_by_alias(
    REGISTERED_MODEL_NAME,
    CHAMPION_ALIAS
)

Print:

- registered model name
- alias
- actual version currently behind Champion
- run ID
- status

Store the actual Champion version dynamically:

champion_version = champion_version_details.version

Do not assume it is always Version 1.

Add Markdown explaining that the alias resolves dynamically to the approved model version.

3. Create Champion Model URI

Create:

champion_model_uri = f"models:/{REGISTERED_MODEL_NAME}@Champion"

Print the URI.

4. Load Champion Model from Unity Catalog

Load using MLflow:

champion_model = mlflow.sklearn.load_model(champion_model_uri)

Print the loaded model type.

Confirm that the model supports:

- "predict()"
- "predict_proba()"

5. Load Batch Scoring Dataset

For this POC, use:

"Test_ds/churn_X_test.csv"

as the batch scoring input.

Also load:

"Test_ds/churn_test_account_ids.csv"

for account identifiers.

Store as:

- "X_score"
- "account_ids"

Print:

- X_score shape
- account_ids shape

Validate that the row counts match.

If they do not match, stop with a clear error message.

Add Markdown explaining:

POC Note: The existing test dataset is being reused as scoring input only to demonstrate the batch scoring workflow. In production, scoring data would normally be the latest unlabeled feature dataset.

6. Generate Predictions

Generate:

predicted_churn = champion_model.predict(X_score)

Generate churn probabilities:

churn_probability = champion_model.predict_proba(X_score)[:, 1]

Explain:

- "predicted_churn" is the binary model decision
- "churn_probability" is the probability/risk score produced by the model

7. Create Churn Risk Score

Create:

churn_risk_score = churn_probability

Keep the risk score in the 0 to 1 range.

Optionally also create a percentage version:

churn_risk_score_pct = churn_probability * 100

Explain that the 0–1 probability is the primary ML score.

8. Create POC Risk Bands

Use these example thresholds:

- Low: probability < 0.30
- Medium: probability >= 0.30 and < 0.60
- High: probability >= 0.60

Create a function or "np.select()" logic to produce:

"churn_risk_band"

Add this Markdown note:

POC Note: These risk-band thresholds are examples only. Final thresholds must be agreed during actual development based on business requirements and model performance.

9. Create Scoring Output DataFrame

Create a dataframe named:

"scoring_output"

Include:

- account_id
- predicted_churn
- churn_probability
- churn_risk_score
- churn_risk_score_pct
- churn_risk_band
- model_name
- model_alias
- model_version
- model_run_id
- scoring_timestamp

Use:

model_name = REGISTERED_MODEL_NAME
model_alias = "Champion"
model_version = champion_version
model_run_id = champion_version_details.run_id

Use a UTC timestamp:

datetime.now(timezone.utc)

Do not include target/y_test in the scoring output.

10. Display Sample Scoring Output

Display:

- first 20 rows
- total number of scored accounts

Print counts for:

- predicted churn = 1
- predicted churn = 0

Also display counts by:

- Low
- Medium
- High risk

11. Basic Scoring Summary

Calculate:

- total scored records
- average churn probability
- predicted churn rate
- minimum probability
- maximum probability
- Low-risk count
- Medium-risk count
- High-risk count

Display these values clearly.

Explain that these summary statistics can later be used for prediction monitoring.

Do not implement formal monitoring yet.

12. Validate Output Schema

Print:

scoring_output.dtypes

Also display the columns in order.

Check for:

- duplicate account IDs
- missing churn probabilities
- missing risk bands
- missing model metadata

Print clear validation results.

13. Demonstrate Gold Table Target

Add a Markdown section:

"## Future Production Output"

Explain that in the production design, this scoring output could be written to a Gold/output table for Power BI or downstream business consumption.

Use an example target table name:

"superdata_au_dev.mlops.churn_scoring_output_poc"

Do not write to the table automatically.

Show a commented example only, such as:

# spark.createDataFrame(scoring_output).write \
#     .mode("append") \
#     .saveAsTable("superdata_au_dev.mlops.churn_scoring_output_poc")

Explain that append/overwrite strategy should be decided during actual development.

14. Optional CSV POC Output

For easier inspection during the POC, optionally save:

"Output_Metrics/champion_batch_scoring_output.csv"

Do not overwrite unrelated files.

If the directory/path is not available, show a friendly warning rather than failing the notebook.

15. Final Summary

Print:

- Model name
- Alias used
- Actual Champion version
- Total scored records
- Predicted churn count
- Average churn probability
- High-risk account count

Print:

"Step 7 completed successfully. Batch scoring using the Champion alias has been demonstrated."

Important Requirements

- Load the model from Unity Catalog using "@Champion".
- Do not hardcode Version 1 for scoring.
- Do not use the Candidate model for production-style scoring in this notebook.
- Do not retrain any model.
- Do not create a new model version.
- Do not change Champion/Candidate aliases.
- Do not create a Databricks Job yet.
- Do not implement drift/performance monitoring yet.
- Do not include actual target labels in the scoring output.
- Keep each major section explained with simple Markdown.
