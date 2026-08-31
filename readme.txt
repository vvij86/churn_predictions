Copilot Prompt — Step 13: Retraining Strategy POC

Create a new Databricks notebook named:

"13_retraining_strategy_poc.ipynb"

This notebook should continue from the existing MLOps POC.

Current State

Already completed:

- Model registration in Unity Catalog
- Version 1 = Champion
- Version 2 = Candidate
- Batch scoring using "@Champion"
- Model output schema
- Job scheduling POC
- Prediction monitoring
- Feature drift monitoring
- Model performance monitoring

Purpose

Demonstrate a simple retraining decision strategy.

This step should answer:

"When should the churn model be retrained?"

Do not actually retrain the model in this notebook.

Do not create a new model version.

Do not change Champion/Candidate aliases.

Step 13 - Retraining Strategy POC

Create a Markdown heading:

"# Step 13 - Retraining Strategy POC"

Explain in simple terms:

Retraining means rebuilding the model using newer labelled data so that the model can learn from more recent customer behaviour.

Retraining should not happen blindly after every scoring run.

Instead, retraining can be triggered when monitoring indicates that the model or input data has changed significantly.

1. Define Possible Retraining Triggers

Create a Markdown section listing these example triggers:

A. Scheduled Retraining

Example:

- Quarterly
- Half-yearly
- Annually

Explain that scheduled retraining is simple but may retrain even when the model is still healthy.

B. Performance Degradation

Examples:

- Recall drops significantly
- F1 drops significantly
- ROC AUC drops significantly
- False Negative Rate increases significantly

Explain that performance degradation is one of the strongest reasons to investigate retraining.

C. Feature Drift

Examples:

- Multiple important features show HIGH_DRIFT
- New categories appear
- Input distributions change significantly

D. Prediction Behaviour Change

Examples:

- Predicted churn rate changes sharply
- High-risk population changes significantly
- Average churn probability changes unexpectedly

E. Business/Data Changes

Examples:

- new products
- new business rules
- source-system changes
- new features become available
- major changes in member behaviour

2. Create POC Retraining Rules

Define example POC rules such as:

- Performance health = "DEGRADED" → Retraining recommended
- F1 drop > 10% → Retraining recommended
- Recall drop > 10% → Retraining recommended
- More than 3 HIGH_DRIFT features → Retraining investigation
- Prediction churn-rate change > 20% → Investigation
- No meaningful issues → No retraining required

Clearly state:

POC Note: These thresholds are illustrative only and must be finalized with the business and ML team during production implementation.

3. Read Existing Monitoring Results if Available

Look under:

"Output_Metrics/"

for the latest available files matching patterns such as:

- "model_performance_monitoring_summary_*.csv"
- "feature_drift_numeric_summary_*.csv"
- "prediction_monitoring_summary_*.csv"

Load the latest available monitoring files.

If one of the monitoring outputs does not exist, print a friendly warning and continue.

Do not fabricate monitoring results.

4. Create Retraining Decision Logic

Based on available monitoring results, determine:

- performance_trigger
- drift_trigger
- prediction_trigger
- scheduled_trigger

Create simple boolean flags.

Then calculate:

"retraining_recommended"

Use simple logic:

- If performance is DEGRADED → True
- OR if important degradation thresholds are breached → True
- OR if several HIGH_DRIFT features are found → True
- Otherwise → False

Do not automatically retrain.

5. Create Retraining Decision Summary

Create a dataframe:

"retraining_decision_summary"

with columns:

- trigger_type
- monitoring_result
- threshold
- trigger_status
- recommended_action

Example:

Trigger| Result| Status| Action
F1 degradation| 4%| OK| Continue monitoring
Recall degradation| 13%| TRIGGERED| Investigate retraining
High drift features| 0| OK| No action
Prediction-rate change| 6%| OK| Continue monitoring

Display clearly.

6. Produce Overall Decision

Print one of:

"Retraining Decision: NOT REQUIRED"

"Retraining Decision: INVESTIGATE"

"Retraining Decision: RECOMMENDED"

Explain why the decision was reached.

Example:

"Retraining recommended because Recall degradation exceeded the configured POC threshold."

7. Explain What Happens After a Retraining Trigger

Add Markdown explaining the future retraining flow:

"New labelled data"

→ "Rebuild training dataset"

→ "Feature engineering"

→ "Retrain model"

→ "Hyperparameter tuning"

→ "Evaluate against Champion"

→ "Register new candidate version"

→ "Validate"

→ "Promote Candidate to Champion if approved"

Explain that retraining does not automatically mean the new model should become Champion.

8. Explain Human Approval / Governance

Add Markdown explaining:

For production, retraining may be automated, but model promotion should follow agreed governance and approval rules.

A newly trained model should be compared against the existing Champion before promotion.

9. Scheduled vs Trigger-Based Retraining

Create a simple Markdown comparison table:

Approach| Description
Scheduled| Retrain at fixed intervals
Trigger-based| Retrain when monitoring thresholds are breached
Hybrid| Scheduled review plus drift/performance triggers

For this churn use case, describe a hybrid strategy as a sensible production consideration, but do not present it as a final approved design.

10. Save Retraining Decision

Save:

"retraining_decision_summary"

to:

"Output_Metrics/retraining_decision_<current_date>.csv"

Use UTC date in "YYYYMMDD" format.

Print the output path.

11. Final Summary

Print:

- Performance trigger status
- Drift trigger status
- Prediction trigger status
- Overall retraining recommendation

Print:

"Step 13 completed successfully. Retraining strategy and trigger logic have been demonstrated."

Important Requirements

- Do not retrain a model.
- Do not create a new model version.
- Do not modify aliases.
- Do not automatically promote a model.
- Use existing monitoring outputs where available.
- Do not fabricate monitoring results.
- Clearly identify all thresholds as POC examples.
- Keep explanations simple and learning-oriented.
