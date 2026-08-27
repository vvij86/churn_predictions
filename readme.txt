Copilot Prompt — Create Separate Step 2 Notebook

Create a new Databricks notebook named:

"02_verify_unity_catalog_access.ipynb"

This notebook should contain only Step 2 of the MLOps POC.

Purpose

Verify that the current user can access:

"superdata_au_dev.mlops"

and confirm the permissions required for model registration.

Notebook Content

Create a Markdown section:

"# Step 2 - Verify Unity Catalog Schema Access"

Briefly explain what this step is checking and why it is required before registering MLflow models.

Then add code to:

1. Run:

USE CATALOG superdata_au_dev

2. Run:

USE SCHEMA mlops

3. Display:

SELECT current_catalog(), current_schema()

4. Run:

SHOW GRANTS ON SCHEMA superdata_au_dev.mlops

Display the grant results clearly.

If "SHOW GRANTS" is not permitted, catch the exception and display a friendly warning instead of failing the notebook.

Add a Markdown explanation of these permissions:

- "USE CATALOG"
- "USE SCHEMA"
- "CREATE MODEL"

Explain that "CREATE MODEL" is needed for registering a model in Unity Catalog.

Do not:

- load training/test datasets
- load joblib models
- train a model
- create an MLflow experiment
- register a model

At the end print:

"Step 2 completed successfully. Unity Catalog access verified."
