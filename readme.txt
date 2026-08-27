Copilot Prompt — Step 1: Create MLOps POC Notebook and Verify Setup

Create a new Databricks/Jupyter notebook named:

"databricks_mlops_poc_step_by_step.ipynb"

For now, create only Step 1. Do not create any later MLOps steps yet.

Step 1 — Imports and Basic MLOps Configuration

Create a Markdown cell with the heading:

"# Step 1 - Import Libraries and Configure MLflow"

Explain briefly that this step prepares the libraries and configuration required for the MLOps POC.

Then create a Python code cell that:

1. Imports:
   
   - pandas
   - numpy
   - joblib
   - mlflow
   - mlflow.sklearn
   - MlflowClient from "mlflow.tracking"
   - datetime

2. Prints the installed MLflow version.

3. Defines these configuration variables:

CATALOG_NAME = "superdata_au_dev"
SCHEMA_NAME = "mlops"
REGISTERED_MODEL_NAME = "superdata_au_dev.mlops.superannuation_churn_model"

4. Configure MLflow to use the Unity Catalog Model Registry:

mlflow.set_registry_uri("databricks-uc")

5. Create an MLflow client:

client = MlflowClient()

6. Print:
   - Catalog name
   - Schema name
   - Registered model name
   - Current MLflow registry URI

Add comments in the code explaining each important line.

At the end print:

"Step 1 completed successfully."

Do not load datasets.
Do not load any ".joblib" models.
Do not train or register any model.
Do not create an MLflow experiment yet.
Do not implement any other MLOps functionality.

This step should only verify that the required Python/MLflow setup is available and configure the Unity Catalog registry.
