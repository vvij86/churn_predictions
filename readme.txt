Update my existing "databricks_model_versioning_poc.ipynb" notebook so that model versioning actually creates a new registered model version.

Current behavior:

- Training notebook runs successfully.
- MLflow creates a new experiment run when I change parameters such as "max_depth".
- "mlflow.sklearn.autolog(log_models=True)" logs the trained model as an MLflow artifact.
- However, rerunning the training notebook does NOT automatically create a new model version.

I want the versioning notebook to clearly demonstrate the difference between:

MLflow Experiment Run
and
Registered Model Version

Please update the notebook with the following flow.

1. Retrieve latest successful Random Forest runs

Get the latest successful Random Forest MLflow runs from my existing experiment.

Display a table containing:

- Run ID
- Run name
- Start time
- "max_depth"
- "n_estimators"
- Accuracy
- Precision
- Recall
- F1
- ROC-AUC

Support the custom metrics already used in my POC, such as:

- "custom_accuracy"
- "custom_precision"
- "custom_recall"
- "custom_f1_score"
- "custom_roc_auc"

This should allow me to visually compare, for example:

- Run A with "max_depth=10"
- Run B with "max_depth=20"

---

2. Select a run for registration

Allow me to select the MLflow run that I want to register.

Prefer using a variable such as:

"SELECTED_RUN_ID"

If it is empty, automatically select the latest successful Random Forest run.

Print:

- Selected Run ID
- Model parameters
- Key metrics

---

3. Identify the logged model artifact

Identify the model artifact produced by:

"mlflow.sklearn.autolog(log_models=True)"

Build the model URI:

"runs:/<selected_run_id>/<model_artifact_path>"

Display the final model URI before registration.

---

4. Configure registered model name

Keep the registered model name configurable.

Do not assume "superdata_au_dev.ml_schema" exists.

Use variables such as:

- "CATALOG_NAME"
- "SCHEMA_NAME"
- "MODEL_NAME"
- "REGISTERED_MODEL_NAME"

If a Unity Catalog schema is available and accessible, use:

"<catalog>.<schema>.<model_name>"

Otherwise clearly explain that an accessible registry/schema is required.

Do not create a schema automatically.

---

5. Register the selected MLflow run as a model version

Explicitly call MLflow model registration.

Use the equivalent of:

"mlflow.register_model()"

with:

- selected run model URI
- same registered model name

The important behavior I want to demonstrate is:

Run A registered under the model name
→ Version 1

Run B registered later under the SAME model name
→ Version 2

Run C registered later
→ Version 3

Print clearly after successful registration:

"Registered Model: <name>"

"Source Run ID: <run_id>"

"Created Model Version: <version>"

---

6. Prevent accidental duplicate versions

Before registering the selected run, check whether the same MLflow Run ID is already registered under this registered model.

If the Run ID is already registered:

Do NOT create another model version.

Print:

"This MLflow run is already registered as Model Version X."

If the Run ID has not previously been registered:

Create a new model version.

This safeguard is important because I may rerun the notebook multiple times during the demo.

Expected behavior:

Same Run ID
→ reuse/show existing version

New Run ID
→ create next model version

---

7. Display all registered model versions

After registration, retrieve all versions of the same registered model.

Display a table with:

- Version
- Source Run ID
- Creation timestamp
- Model source URI
- Alias
- Run "max_depth"
- Accuracy
- Precision
- Recall
- F1
- ROC-AUC

This should make it easy to demonstrate that different experiment runs can become different registered model versions.

---

8. Candidate and Champion aliases

If model aliases are supported:

For the first approved model:

"Version 1 → Champion"

For a newly registered model:

"Version 2 → Candidate"

Display:

Version| Run ID| Alias
1| Run A| Champion
2| Run B| Candidate

Do not automatically promote Candidate to Champion unless explicitly controlled by a variable.

Create a variable such as:

"PROMOTE_CANDIDATE = False"

---

9. Optional promotion

If:

"PROMOTE_CANDIDATE = True"

move the "Champion" alias to the selected Candidate version.

Print:

"Champion changed from Version X to Version Y."

Do not delete the previous version.

---

10. Demonstrate rollback

Include an optional, non-executed example showing how Champion could be moved back to the previous version.

Clearly label this:

"Optional rollback example"

Explain that old versions remain available in the Model Registry.

---

11. Add explanatory Markdown

Add a simple explanation in the notebook:

Experiment Run vs Model Version

MLflow Experiment Run

Created every time the training notebook executes.

Example:

"max_depth=10"
→ Run A

"max_depth=20"
→ Run B

Experiment tracking stores:

- Parameters
- Metrics
- Model artifact
- Dataset information
- Other metadata

Registered Model Version

Created only when an MLflow run's model artifact is explicitly registered in Model Registry.

Example:

Run A
→ Register
→ Version 1

Run B
→ Register
→ Version 2

Therefore:

"mlflow.sklearn.autolog(log_models=True)"

logs the model artifact, but does NOT by itself create a registered model version.

---

12. Final POC summary

Print:

Model Versioning POC

"Training Run"
→ "MLflow Experiment"
→ "Compare Runs"
→ "Select Model"
→ "Register Model"
→ "Model Version"
→ "Candidate"
→ "Champion"

Also print an example based on the available runs:

"Random Forest Run A – max_depth=10 → Version 1"

"Random Forest Run B – max_depth=20 → Version 2"

Only show the Version numbers if registration actually succeeded.

If registration cannot be completed due to missing Unity Catalog schema or permissions, clearly state the prerequisite instead of reporting success.

Important:

- Update the existing versioning notebook only.
- Do not modify the Random Forest training notebook.
- Do not retrain models in this notebook.
- Reuse existing MLflow runs.
- Do not automatically create Unity Catalog schemas.
- Do not create duplicate model versions for the same Run ID.
- Keep the notebook simple and suitable for an MLOps POC demonstration.This will give you the behavior you expected: changing max_depth and rerunning training gives a new run, then running the versioning notebook against that new run gives a new model version.
