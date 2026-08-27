Copilot Prompt — Step 5: Register Model in Unity Catalog

Create a new Databricks notebook named:

"05_register_model_unity_catalog.ipynb"

This notebook should contain only Step 5 of the MLOps POC.

Purpose

Register the existing Logistic Regression model in Unity Catalog under:

"superdata_au_dev.mlops.superannuation_churn_model"

This should create the first registered model version in Unity Catalog.

Do not create aliases yet.
Do not demonstrate version promotion yet.
Do not retrain the model.

Existing Inputs

Use these existing files:

Model:

"Models/logistic_regression_pipeline.joblib"

Test data:

"Test_ds/churn_X_test.csv"

"Test_ds/churn_y_test.csv"

Step 5 - Register Model in Unity Catalog

Create a Markdown heading:

"# Step 5 - Register Model in Unity Catalog"

Explain briefly that:

- Step 4 logged the model inside an MLflow experiment/run.
- Step 5 registers the model into Unity Catalog.
- Registration creates a centrally managed registered model and a model version.

1. Import Required Libraries

Import:

- pandas
- joblib
- mlflow
- mlflow.sklearn

Also import:

from mlflow.models import infer_signature
from mlflow.tracking import MlflowClient

2. Configure Unity Catalog Registry

Set:

mlflow.set_registry_uri("databricks-uc")

Define:

CATALOG_NAME = "superdata_au_dev"
SCHEMA_NAME = "mlops"
REGISTERED_MODEL_NAME = "superdata_au_dev.mlops.superannuation_churn_model"

Print the registry URI and registered model name.

3. Load Existing Model and Test Data

Load:

"Models/logistic_regression_pipeline.joblib"

into:

"model"

Load:

"Test_ds/churn_X_test.csv"

into:

"X_test"

Do not retrain the model.

4. Create Model Signature

Use a small sample of X_test as the input example.

For example:

input_example = X_test.head(5)

Generate sample predictions:

sample_predictions = model.predict(input_example)

Infer the model signature using:

signature = infer_signature(input_example, sample_predictions)

Explain in Markdown that the signature records the expected input/output schema of the model.

5. Log Model to a New MLflow Run

Create or use this experiment:

"/Shared/MLOps_POC_Superannuation_Churn"

Start a new MLflow run with a meaningful name such as:

"logistic_regression_uc_registration"

Log useful tags:

- business_use_case = superannuation_churn
- environment = dev
- poc_stage = model_registration
- model_source = existing_joblib

Log the model using:

model_info = mlflow.sklearn.log_model(
    sk_model=model,
    name="model",
    signature=signature,
    input_example=input_example
)

Use the current MLflow 3.x recommended "name" parameter rather than deprecated "artifact_path".

6. Register the Logged Model in Unity Catalog

Register the model using the logged model URI.

Use:

registered_model = mlflow.register_model(
    model_uri=model_info.model_uri,
    name=REGISTERED_MODEL_NAME
)

Wait until the registration completes if necessary.

Print:

- Registered model name
- Model version
- Run ID if available
- Registration status

7. Verify the Registered Model

Create an MLflow client:

client = MlflowClient()

Retrieve the registered model / model version information.

Display:

- model name
- version
- status
- source/run information if available

Also list the model versions for:

"superdata_au_dev.mlops.superannuation_churn_model"

8. Final Confirmation

Print a clear message such as:

"Step 5 completed successfully. Model registered in Unity Catalog."

Also print:

"Registered model: superdata_au_dev.mlops.superannuation_churn_model"

and the created version number.

Important Requirements

- Do not retrain the model.
- Do not create Champion/Candidate aliases yet.
- Do not create multiple versions intentionally.
- Do not create batch scoring yet.
- Use the existing Logistic Regression model only.
- Include model signature and input example.
- Use Unity Catalog registry with "databricks-uc".
- Add Markdown explanations before each major section so the notebook is easy to understand later.
