Create a new Databricks notebook named:

"databricks_model_versioning_poc.ipynb"

Objective: Demonstrate a simple MLflow Model Registry / model versioning POC using the existing Random Forest churn model experiment.

Important current constraint:

- A dedicated schema such as "superdata_au_dev.ml_schema" does not currently exist.
- Do not make the notebook dependent on that schema.
- First identify whether there is any existing catalog/schema/model-registry location where I currently have permission to register a model.
- If an existing permitted location is available, use that for this POC.
- Keep catalog, schema and model name configurable through variables.
- If model registration is not possible because of permissions, do not fail the notebook. Show the intended registration/versioning code and clearly print the missing prerequisite.

Keep the notebook small, standalone and suitable for an MLOps demonstration.

Use clear Markdown before each code cell explaining what is being demonstrated.

Cell 1 – Import Libraries

Import:

- "mlflow"
- "MlflowClient"
- other required standard libraries

Display the installed MLflow version.

---

Cell 2 – Configure Model Registry Settings

Create configurable variables such as:

- "CATALOG_NAME"
- "SCHEMA_NAME"
- "MODEL_NAME"
- "FULL_MODEL_NAME"

Do not hard-code "superdata_au_dev.ml_schema" as an existing schema.

Use an existing catalog/schema only if it is accessible.

Add a Markdown note explaining:

«For the current POC, an existing permitted model registry location can be used.
For the future implementation, dedicated ML schemas are recommended, for example:

- "superdata_au_dev.ml_schema"
- "superdata_au_test.ml_schema"
- "superdata_au_prod.ml_schema"

These schemas need to be created by the appropriate Databricks/platform administration team and required permissions need to be provided.»

If Unity Catalog is being used, configure the appropriate MLflow registry URI.

---

Cell 3 – Identify Existing Random Forest Experiment

Use the existing Random Forest churn model MLflow experiment.

Retrieve the latest successful Random Forest run programmatically where possible.

Do not hard-code the run ID unless absolutely necessary.

Display:

- Experiment name
- Run ID
- Run status
- Model/artifact path
- Training timestamp

Also retrieve available evaluation metrics such as:

- Accuracy
- Precision
- Recall
- F1 Score
- ROC-AUC

Support both standard MLflow metric names and the custom metric names already logged in the POC, such as:

- "custom_accuracy"
- "custom_precision"
- "custom_recall"
- "custom_f1_score"
- "custom_roc_auc"

---

Cell 4 – Identify Model Artifact

Inspect the selected MLflow run and identify the trained model artifact path.

Build the model URI in the format:

"runs:/<run_id>/<model_artifact_path>"

Display:

- Source Run ID
- Model artifact path
- Model URI

Do not assume the model artifact path if it can be identified programmatically.

---

Cell 5 – Check Model Registration Capability

Before attempting registration, validate whether the configured catalog/schema/model registry location is accessible.

Check:

- Whether the catalog exists
- Whether the schema exists
- Whether the current user can register/create a model there

If access is available:

Print:

"Model registry location is available for POC."

If access is unavailable:

Print a clear message such as:

"Model registration could not be completed because a permitted Unity Catalog schema/model registry location is not currently available."

Also print:

"Recommended future prerequisite: create dedicated ML schemas in DEV, TEST and PROD and provide required model registration permissions."

Do not allow this permission issue to terminate the entire notebook.

---

Cell 6 – Register Existing Random Forest Model

If model registration access is available, register the existing Random Forest model from the selected MLflow run.

Do not retrain the model simply for registration.

Register it using the configurable model name.

Display:

- Registered model name
- Newly created version number
- Source Run ID
- Model URI

Add exception handling for permission/schema related errors.

---

Cell 7 – Display Registered Model Versions

Using "MlflowClient", retrieve all available versions of the registered model.

Display them in a table containing where available:

- Registered model name
- Version
- Run ID
- Creation timestamp
- Source
- Alias
- Description/status

Explain that registering a newer approved model run under the same registered model name creates another model version.

---

Cell 8 – Demonstrate Version 1 and Version 2

If two successful Random Forest MLflow runs are available, register two different model runs under the same registered model name.

For example:

- Version 1 – First approved Random Forest run
- Version 2 – Newer Random Forest run

Do not register the exact same run twice unless no alternative run exists and it is clearly labelled as a technical POC-only demonstration.

For both versions, display the source run metrics where possible:

- Precision
- Recall
- F1
- ROC-AUC

The objective is to show that each registered model version is traceable back to the MLflow run from which it was created.

---

Cell 9 – Demonstrate Candidate and Champion Aliases

If aliases are supported in the available registry configuration, demonstrate:

- Version 1 → "Champion"
- Version 2 → "Candidate"

Display the alias mapping.

Explain in Markdown that aliases allow downstream applications to reference a logical model such as:

"@Champion"

instead of hard-coding:

"Version 1"

or:

"Version 2"

If aliases cannot be demonstrated because registration access is unavailable, show the sample code as a future implementation example and clearly label it:

"Not executed – model registry prerequisite required."

---

Cell 10 – Demonstrate Model Promotion

Demonstrate the concept of promoting a Candidate model.

Before promotion:

- Version 1 = Champion
- Version 2 = Candidate

After approval:

- Version 2 = Champion

Print a simple message such as:

"Champion model changed from Version 1 to Version 2."

Explain that Version 1 remains registered and can still be used for traceability or rollback.

Do not delete previous versions.

---

Cell 11 – Load Model Using Champion Alias

If registration and aliases are available, demonstrate loading the model through:

"models:/<registered_model_name>@Champion"

rather than using a hard-coded model version.

Display:

- Registered model name
- Champion version
- Source Run ID

If practical, execute a very small sample prediction.

If the required feature structure for sample prediction is not easily available, skip the prediction and only demonstrate model loading.

---

Cell 12 – Rollback Demonstration

Provide sample code showing how the Champion alias could be moved back to the previous version.

For example:

Version 2 → current Champion

Then rollback:

Version 1 → Champion

Do not automatically execute the rollback unless appropriate for the POC.

Clearly label the code:

"Optional rollback demonstration"

Explain that rollback is achieved by changing the alias reference rather than deleting or rebuilding the old model.

---

Cell 13 – Explain DEV / TEST / PROD Future Design

Add a Markdown-only section explaining the recommended future model registry structure.

Suggested target structure:

DEV

"superdata_au_dev.ml_schema"

Used for:

- Development models
- Candidate models
- Experiment-based registration
- Initial validation

TEST

"superdata_au_test.ml_schema"

Used for:

- QA/testing
- Model validation
- Integration testing

PROD

"superdata_au_prod.ml_schema"

Used for:

- Approved production models
- Production scoring
- Controlled Champion versions

Clearly state:

"These schemas are recommendations from the POC and are not currently available."

---

Cell 14 – Model Versioning POC Summary

Print a summary.

If model registration was successful, show:

Model Versioning POC Summary

- Existing MLflow experiment run retrieved successfully
- Existing trained Random Forest model reused
- Model registration demonstrated
- Model version creation demonstrated
- Model version linked back to source MLflow run
- Candidate and Champion aliases demonstrated
- Model promotion concept demonstrated
- Rollback approach demonstrated
- Previous versions retained for traceability

If registration was not possible because of permissions/schema availability, show:

Model Versioning POC Summary

- Existing MLflow experiment tracking validated
- Existing Random Forest run successfully identified
- Model artifact URI successfully identified
- Model registration approach prepared
- Model versioning approach documented
- Candidate/Champion alias approach documented
- Current blocker: suitable Unity Catalog ML schema/model registration permission not available
- Recommended prerequisite: create dedicated ML schemas and provide model registry permissions

Finally show this simple flow:

"Model Training"
→ "MLflow Experiment"
→ "Successful Run"
→ "Register Model"
→ "Version 1 / Version 2"
→ "Candidate"
→ "Champion"
→ "Production Scoring"

Important Instructions

- Do not modify the existing Random Forest training notebook.
- Do not rebuild the full training pipeline.
- Reuse existing MLflow runs and model artifacts.
- Do not assume "superdata_au_dev.ml_schema" already exists.
- Do not create schemas automatically.
- Do not request elevated permissions programmatically.
- Handle missing permissions gracefully.
- Clearly distinguish between:
  - Validated in current POC
  - Demonstration code
  - Future recommended MLOps setup
- Keep the notebook concise and demo-friendly.
