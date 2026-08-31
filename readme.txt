Copilot Prompt — Step 14: Model Rollback Demo with Simulated Performance Failure

Create a new Databricks notebook named:

"14_model_rollback_demo_with_failure.ipynb"

This notebook should demonstrate a realistic rollback scenario for the existing churn MLOps POC.

Current State

Registered model:

"superdata_au_dev.mlops.superannuation_churn_model"

Existing versions:

- Version 1
- Version 2

Current aliases:

- Champion
- Candidate

Earlier POC steps already demonstrated:

- model registration
- versioning
- Champion/Candidate aliases
- batch scoring
- prediction monitoring
- feature drift monitoring
- model performance monitoring
- retraining decision strategy

Purpose

Demonstrate a realistic rollback scenario:

1. Start with the existing Champion
2. Temporarily promote the Candidate model to Champion
3. Simulate a performance problem after promotion
4. Show that monitoring would recommend rollback
5. Require an explicit POC/manual approval flag before rollback
6. Roll Champion back to the previous known-good version
7. Verify that downstream scoring code still uses "@Champion" and does not change

This is a POC demonstration only.

Do not retrain any model.

Step 14 - Model Rollback Demo

Create a Markdown heading:

"# Step 14 - Model Rollback After Performance Degradation"

Explain in simple terms:

A newly promoted model may later show poor production behaviour.

Examples:

- Recall drops significantly
- F1 deteriorates
- False Negatives increase
- prediction distribution becomes abnormal
- business validation fails

In those situations, the model may need to be rolled back to the previous known-good Champion.

1. Import and Configure MLflow

Import:

import pandas as pd
import mlflow
from datetime import datetime, timezone
from mlflow.tracking import MlflowClient

Configure:

mlflow.set_registry_uri("databricks-uc")

REGISTERED_MODEL_NAME = "superdata_au_dev.mlops.superannuation_churn_model"

client = MlflowClient()

2. Display Existing Model Versions and Aliases

Retrieve all model versions.

Display:

- version
- run_id
- status
- aliases
- creation timestamp

Retrieve:

current_champion = client.get_model_version_by_alias(
    REGISTERED_MODEL_NAME,
    "Champion"
)

current_candidate = client.get_model_version_by_alias(
    REGISTERED_MODEL_NAME,
    "Candidate"
)

Print:

"Current Champion -> Version X"

"Current Candidate -> Version Y"

Store the original Champion version:

original_champion_version = current_champion.version

Store the Candidate version:

candidate_version = current_candidate.version

3. Temporarily Promote Candidate to Champion

Add Markdown:

"## Simulate Candidate Promotion"

Explain:

For this POC, assume the Candidate has passed pre-production validation and is temporarily promoted to Champion.

Use:

client.set_registered_model_alias(
    name=REGISTERED_MODEL_NAME,
    alias="Champion",
    version=candidate_version
)

Verify the alias after promotion.

Print:

"POC Promotion completed: Champion -> Version X"

Clearly display:

POC Note: This is a temporary demonstration promotion only.

4. Simulate Post-Promotion Performance Monitoring

Create a Markdown section:

"## Simulate Performance Degradation"

Explain that production monitoring may detect degraded model performance after deployment.

For this POC, create clearly labelled simulated monitoring values.

Use example values such as:

baseline_recall = 0.86
current_recall = 0.70

baseline_f1 = 0.91
current_f1 = 0.78

baseline_roc_auc = 0.95
current_roc_auc = 0.90

Clearly state:

IMPORTANT: The following values are simulated only to demonstrate rollback logic. They are not actual measured results from Version 2.

Calculate percentage degradation for:

- Recall
- F1
- ROC AUC

5. Define POC Rollback Thresholds

Use example thresholds:

- Recall degradation > 10% → rollback warning
- F1 degradation > 10% → rollback warning
- ROC AUC degradation > 5% → rollback warning

Clearly label all thresholds as POC examples.

Create a dataframe:

"rollback_monitoring_summary"

with:

- metric
- baseline_value
- current_value
- degradation_pct
- threshold_pct
- status

Status:

- "OK"
- "ROLLBACK_WARNING"

Display it.

6. Determine Rollback Recommendation

Create logic:

If one or more critical metrics exceed the rollback threshold:

Rollback Recommendation: YES

Otherwise:

Rollback Recommendation: NO

Also calculate:

"rollback_reason"

Example:

"Recall and F1 degradation exceeded POC thresholds."

Print the reason clearly.

7. Add Manual Approval Gate

Do NOT perform rollback purely because the threshold fired.

Add:

APPROVE_ROLLBACK_FOR_POC = True

Add Markdown explaining:

In production, monitoring should raise an alert or recommendation, but rollback may require human approval/governance.

Only perform rollback when:

rollback_recommended == True
and APPROVE_ROLLBACK_FOR_POC == True

If approval is False, print:

"Rollback recommended, but not executed because approval was not provided."

8. Perform Rollback

When both recommendation and approval are True:

Move "Champion" back to:

"original_champion_version"

Use:

client.set_registered_model_alias(
    name=REGISTERED_MODEL_NAME,
    alias="Champion",
    version=original_champion_version
)

Print:

"Rollback executed successfully."

Print:

"Champion restored to Version X"

9. Verify Final Champion

Retrieve the Champion alias again.

Display:

- alias
- final version
- run ID
- status

Validate that:

final_champion.version == original_champion_version

Print:

"Rollback verification passed."

10. Demonstrate Scoring URI Does Not Change

Create:

champion_uri = f"models:/{REGISTERED_MODEL_NAME}@Champion"

Print the URI before and after rollback.

Explain:

The URI remains:

"models:/superdata_au_dev.mlops.superannuation_churn_model@Champion"

Only the model version behind the alias changes.

Therefore the batch-scoring notebook does not require code changes.

11. Create Rollback Audit Record

Create a dataframe named:

"rollback_audit"

containing:

- model_name
- original_champion_version
- promoted_candidate_version
- rollback_recommended
- rollback_approved
- rollback_executed
- final_champion_version
- rollback_reason
- rollback_timestamp

Use UTC timestamp.

Display it.

12. Save POC Rollback Evidence

Save:

"rollback_monitoring_summary"

to:

"Output_Metrics/model_rollback_monitoring_<date>.csv"

Save:

"rollback_audit"

to:

"Output_Metrics/model_rollback_audit_<date>.csv"

Use UTC date in "YYYYMMDD" format.

Print both paths.

13. Add Team Demo Narrative

Create a Markdown section named:

"## Suggested Demo Story"

Include this simple narrative:

1. Version 1 is the known-good Champion.
2. Version 2 is the tuned Candidate.
3. Version 2 is temporarily promoted to Champion.
4. Post-deployment monitoring identifies simulated Recall/F1 degradation.
5. Monitoring recommends rollback.
6. Manual approval is provided for the POC.
7. Champion alias is redirected back to Version 1.
8. Batch-scoring code continues using "@Champion" without modification.

14. Final Summary

Print:

- Original Champion version
- Temporarily promoted version
- Number of rollback warnings
- Rollback recommendation
- Approval status
- Final Champion version
- Rollback execution status

Print:

"Step 14 completed successfully. Promotion, simulated performance degradation, approval-based rollback, and recovery were demonstrated."

Important Requirements

- Clearly label simulated monitoring values as simulated.
- Do not claim Version 2 actually performed badly.
- Do not retrain any model.
- Do not delete any version.
- Restore the original Champion before the notebook finishes.
- Use an explicit manual approval flag before rollback.
- Do not permanently leave Version 2 as Champion.
- Keep all explanations simple enough for a team demo.
