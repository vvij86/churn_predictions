Copilot Prompt — Create Business-Readable Word Document for Databricks MLOps POC

Create a Word document named:

"Databricks_MLOps_POC_Documentation.docx"

The document should explain the Databricks MLOps POC in a clear, self-explanatory way so that both technical team members and business SMEs can understand what was implemented, why it was implemented, and how the overall model lifecycle works.

Do not structure the document as a notebook-by-notebook checklist.

Do not use headings such as:

- Step 1
- Step 2
- Step 3
- POC Achievements
- Completed Steps
- Notebook Execution Summary

The notebooks should be used only as the source of truth for the content.

The final document should read like a clear end-to-end MLOps story.

---

Source Notebooks — Use Only These Files

Use only the following existing ".ipynb" notebooks as the source of truth for this Word document:

- "01_mlflow_setup.ipynb"
- "02_verify_unity_catalog_access.ipynb"
- "03_load_existing_model_and_test_data.ipynb"
- "04_evaluate_model_and_log_mlflow.ipynb"
- "05_register_model_unity_catalog.ipynb"
- "06_tune_candidate_register_version2_and_aliases.ipynb"
- "07_batch_scoring_using_champion_alias.ipynb"
- "08_model_output_schema_and_save_to_uc.ipynb"
- "09_schedule_batch_scoring_poc.ipynb"
- "10_prediction_monitoring_poc.ipynb"
- "11_feature_drift_monitoring_poc.ipynb"
- "12_model_performance_monitoring_poc.ipynb"
- "13_retraining_strategy_poc.ipynb"
- "14_model_rollback_demo_with_failure.ipynb"

Before writing each section:

1. Read the relevant notebook.

2. Use the actual implementation from that notebook.

3. Use actual model names, versions, metrics, thresholds, paths and outputs where available.

4. Include only important code snippets taken from the notebooks.

5. Do not fabricate or assume values.

6. If an exact value is unavailable, write:
   
   "Not captured in the POC notebook"
   
   rather than guessing.

7. If the actual notebook filename differs slightly, use the actual existing file rather than inventing a new one.

8. Do not create a separate document section for every notebook.

9. Combine related notebook content into business-readable sections.

10. Do not invent additional POC functionality that is not present in these notebooks.

---

Document Title

Databricks MLOps POC – Superannuation Churn Model

Subtitle:

Model Management, Scoring, Monitoring and Lifecycle Management

Near the beginning of the document, add:

Note: This is a Proof of Concept only. Model selection, thresholds, monitoring rules, scheduling frequency, retraining strategy and production architecture are not final and will be confirmed during actual implementation.

---

Executive Summary

Write a short executive summary in simple language.

Explain that this POC demonstrates how a churn prediction model can be managed after model development using Databricks, MLflow and Unity Catalog.

Explain that the POC demonstrates capabilities such as:

- centrally managing models
- tracking model runs and metrics
- managing multiple model versions
- identifying Champion and Candidate models
- performing scheduled batch scoring
- generating account-level churn risk outputs
- monitoring predictions
- monitoring input-data drift
- monitoring actual model performance
- deciding when retraining may be required
- rolling back to a previous model version if required

Keep this section suitable for business SMEs.

Avoid unnecessary technical details.

---

Business Context

Explain the churn use case in simple terms.

The model predicts the likelihood that an account/member may churn.

Explain that the output can support:

- retention analysis
- identifying higher-risk accounts
- downstream reporting
- potential retention interventions

Keep the explanation business-friendly.

---

MLOps Concept and Why It Is Needed

Explain briefly that creating an ML model is not the end of the process.

Once a model is created, the team also needs a controlled way to:

- track it
- register it
- version it
- use it for scoring
- monitor it
- retrain it when necessary
- roll back if a newer model causes issues

Explain that this lifecycle management is the purpose of MLOps.

---

Model Tracking with MLflow

Explain that MLflow was used to track important information about model runs.

Mention:

- parameters
- evaluation metrics
- artifacts
- run history

Explain why this is useful:

It provides traceability and makes it easier to compare model runs.

Include only a short important code snippet taken from the actual notebook, similar to:

with mlflow.start_run():
    mlflow.log_metric("f1_score", f1)
    mlflow.log_metric("roc_auc", roc_auc)

Use the actual code from the notebook if it differs.

Do not include full logging blocks.

---

Model Evaluation

Explain that the model was evaluated using metrics such as:

- Accuracy
- Precision
- Recall
- F1 Score
- ROC AUC
- Confusion Matrix

Explain each one briefly in plain English.

Give particular attention to Recall.

Explain:

A False Negative means an account that actually churned was predicted as non-churn.

For a churn use case, missed churners can be important because they may not receive timely retention attention.

Include only one short prediction example from the notebook, such as:

y_pred = model.predict(X_test)
y_prob = model.predict_proba(X_test)[:, 1]

Use actual notebook code.

If actual metric values are available in the notebooks, create a small readable table.

Do not invent metric values.

---

Model Signature

Explain model signature in simple language.

A model signature describes the expected structure of the model input and output.

Mention that it helps capture:

- expected columns
- expected data types
- expected output structure

Explain that this improves validation and makes scoring safer.

Include only the important code snippet from the notebook, similar to:

signature = infer_signature(
    input_example,
    model.predict(input_example)
)

---

Central Model Registration in Unity Catalog

Explain that the model was centrally registered in Databricks Unity Catalog.

Use the actual registered model name:

"superdata_au_dev.mlops.superannuation_churn_model"

Explain the difference in simple language:

- Trained model — model created by the ML code
- Registered model — centrally managed model entry
- Model version — a particular version of that registered model

Explain that registering a new model artifact under the same registered-model name creates a new version.

Include only the key model registration code from the notebook, for example:

registered_model = mlflow.register_model(
    model_uri=model_info.model_uri,
    name=REGISTERED_MODEL_NAME
)

---

Baseline and Tuned Candidate Model

Explain that the existing Logistic Regression model was treated as the baseline.

A second candidate model was then created by tuning model parameters.

Explain that Hyperopt was not available in the environment, so scikit-learn "GridSearchCV" was used for the POC.

Explain "GridSearchCV" in simple terms:

It tests a small set of parameter combinations and identifies the combination that performs best according to a chosen evaluation metric.

Mention the actual tuned parameters from the notebook where available, such as:

- C
- class_weight
- max_iter

Include only a short important tuning snippet, for example:

grid_search = GridSearchCV(
    estimator=candidate_pipeline,
    param_grid=param_grid,
    scoring="f1",
    cv=3
)

Use actual notebook code.

---

Baseline vs Candidate Comparison

Explain that the baseline and tuned candidate were compared using common model metrics.

Create a clean table using the actual values available in the notebooks.

Suggested format:

Metric| Version 1 – Baseline| Version 2 – Tuned Candidate
Accuracy| | 
Precision| | 
Recall| | 
F1| | 
ROC AUC| | 

Do not invent missing values.

Explain that model selection should not rely on one metric alone.

Mention that in churn, Recall and False Negatives may be particularly important.

---

Model Versioning and Champion / Candidate

Explain that multiple versions of the model can be retained in Unity Catalog.

Document the actual POC concept:

- Version 1 = baseline
- Version 2 = tuned candidate

Explain aliases:

- "Champion" = currently preferred model
- "Candidate" = model being assessed as a possible replacement

Explain why aliases are useful.

Downstream scoring does not need to hardcode a specific version.

It can use:

"models:/superdata_au_dev.mlops.superannuation_churn_model@Champion"

Explain that the model version behind "Champion" can later change without changing the scoring code.

Include only the important alias code, such as:

client.set_registered_model_alias(
    name=REGISTERED_MODEL_NAME,
    alias="Champion",
    version="1"
)

Use actual notebook code and actual alias mapping.

---

Batch Scoring

Explain batch scoring in layman terms.

Instead of scoring one account at a time, many accounts are processed together through the model.

Create a simple flow:

"Account Feature Data"

→ "Champion Model"

→ "Churn Prediction"

→ "Risk Score"

→ "Risk Band"

Explain that the POC processed the actual number of accounts shown in the notebook.

If the notebook shows "158,783", use that exact value.

Explain the outputs:

- predicted churn
- churn probability
- churn risk score
- churn risk band

Explain Low, Medium and High risk bands.

Clearly state that the thresholds used in the POC are examples and are not final business thresholds.

Include only the key Champion loading and scoring code:

champion_model = mlflow.sklearn.load_model(
    f"models:/{REGISTERED_MODEL_NAME}@Champion"
)

predicted_churn = champion_model.predict(X_score)
churn_probability = champion_model.predict_proba(X_score)[:, 1]

Use the actual notebook snippet.

---

Churn Scoring Output

Explain that scoring results are generated at account level.

Create a readable table with the important business-facing output fields.

Suggested format:

Field| Meaning
account_id| Account being scored
predicted_churn| Model prediction of churn/non-churn
churn_probability| Probability of churn
churn_risk_score| Model-generated churn risk score
churn_risk_band| Low / Medium / High risk
model_version| Model version used for scoring
scoring_timestamp| Time the score was generated

Mention the actual Unity Catalog output table:

"superdata_au_dev.mlops.churn_scoring_output_poc"

Explain that this output can later support Power BI or other downstream consumers.

Include only the important write-to-table snippet from the notebook:

scoring_spark_df.write \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable(
        "superdata_au_dev.mlops.churn_scoring_output_poc"
    )

Explain that overwrite was used for the POC only.

---

Scheduled Batch Scoring

Explain that Databricks Jobs was used to demonstrate automated scoring.

Explain in business language:

Instead of manually running the scoring notebook, a Databricks Job can run it on a defined schedule.

Create the flow:

"Scheduled Databricks Job"

→ "Load Current Champion"

→ "Score Accounts"

→ "Generate Updated Output"

Mention the actual Job/task names if present in the notebook.

Do not include detailed Databricks UI instructions.

Explain that the final scoring frequency can be daily, weekly, monthly or another agreed cadence.

---

Date-Stamped Scoring Outputs

Explain that scoring CSV files were updated to include the scoring date.

Example:

"champion_batch_scoring_output_20260831.csv"

Explain the benefit:

Previous scoring outputs can be retained and compared rather than always replacing the previous CSV.

Include only the small date-generation code snippet:

scoring_date = datetime.now(
    timezone.utc
).strftime("%Y%m%d")

Use the actual notebook implementation.

---

Prediction Monitoring

Explain prediction monitoring in simple terms.

It checks whether the model's output behaviour changes significantly between scoring runs.

Examples include:

- predicted churn rate
- average churn probability
- High-risk percentage
- scoring population size

Clearly explain:

Prediction monitoring compares outputs from different scoring runs.

It does not compare Version 1 against Version 2.

Create a simple table structure using actual values if available:

Measure| Previous Run| Current Run| Change| Status
Predicted churn rate| | | | 
Average churn probability| | | | 
High-risk percentage| | | | 
Total scored accounts| | | | 

If actual monitoring values are unavailable, leave them out rather than inventing them.

Explain that thresholds used were POC thresholds only.

---

Feature Drift Monitoring

Explain feature drift in plain language.

The model learned from a particular pattern of data during training.

Over time, the characteristics of incoming data can change.

Feature drift monitoring checks whether current input data looks materially different from the original/reference data.

Give a simple example:

If the average withdrawal count was around 2 during training but later becomes 8, that feature may have drifted.

Document the actual POC result from the notebook.

If available, include:

- 27 numeric features checked
- 0 Warning-level drift
- 0 High Drift
- 0 categorical features with new categories

Explain that these results are based on simple POC thresholds.

Create a small sample structure such as:

Feature| Reference Mean| Current Mean| Change| Drift Status

Use actual top drifted features only if available in the notebook.

Do not invent feature results.

---

Model Performance Monitoring

Explain that prediction monitoring only tells us whether outputs changed.

Performance monitoring tells us whether the model is still making accurate predictions once actual churn outcomes become available.

Create the flow:

"Model Prediction"

→ "Actual Churn Outcome Available Later"

→ "Compare Prediction with Actual"

→ "Recalculate Metrics"

Explain that performance monitoring may track:

- Precision
- Recall
- F1
- ROC AUC
- False Positives
- False Negatives

Explain that actual outcomes may only be available after the agreed outcome window.

If baseline vs current performance values are present in the notebook, include a small comparison table.

Do not invent missing values.

---

Retraining Strategy

Explain that the model should not automatically be retrained after every scoring run.

Retraining may be considered when:

- model performance deteriorates
- Recall or F1 drops
- important features drift
- prediction behaviour changes sharply
- new labelled data becomes available
- business rules or source systems change

Explain that the POC combines monitoring outputs to produce a recommendation such as:

- NOT REQUIRED
- INVESTIGATE
- RECOMMENDED

Explain that this is decision support only.

It does not automatically retrain the model or automatically promote a new version.

Include actual decision logic or thresholds only if they are present in the notebook.

Clearly label them as POC thresholds.

---

Model Rollback

Explain rollback using a simple business scenario.

Use this sequence:

1. Version 1 is the known-good Champion.
2. Version 2 is promoted after validation.
3. Monitoring later identifies a significant issue.
4. The team decides to roll back.
5. The "Champion" alias is switched back to the previous version.

Explain that the scoring application continues to use:

"@Champion"

so no scoring-code change is needed.

Include only the important rollback code snippet:

client.set_registered_model_alias(
    name=REGISTERED_MODEL_NAME,
    alias="Champion",
    version=previous_version
)

Use actual notebook code.

Clearly state:

For the POC, performance degradation used in the rollback demonstration was simulated only to demonstrate the rollback mechanism. It does not mean Version 2 actually failed.

Explain that a manual approval gate was used in the POC before rollback.

---

End-to-End MLOps Flow

End the main document with a clear self-explanatory flow:

"Account / Feature Data"

→ "Model Training and Evaluation"

→ "MLflow Tracking"

→ "Unity Catalog Model Registry"

→ "Champion / Candidate"

→ "Scheduled Batch Scoring"

→ "Churn Risk Output"

→ "Prediction Monitoring"

→ "Feature Drift Monitoring"

→ "Performance Monitoring"

→ "Retraining Decision"

→ "New Candidate / Promotion / Rollback"

Add a short paragraph explaining that this creates a controlled model lifecycle rather than treating model development as a one-time activity.

---

Production Considerations

Keep this section short.

Mention only that production implementation will require agreement on areas such as:

- scoring frequency
- final churn/risk thresholds
- monitoring thresholds
- alerting and notifications
- model approval/governance
- retraining rules
- production data availability
- DEV / TEST / PROD deployment approach
- output history retention
- downstream Power BI integration

Do not create a long checklist.

---

Important Code Snippet Rules

The document must contain important technical evidence, but it should not become a developer code dump.

Use the actual code from the notebooks.

Include code only where it helps explain an important concept.

Important code snippets may include:

- MLflow metric logging
- model prediction and probability
- model signature
- GridSearchCV tuning
- model registration
- Champion/Candidate alias assignment
- loading "@Champion"
- batch scoring
- saving the scoring table
- date-stamped output naming
- rollback alias switch

Do not include:

- full notebook cells
- long import blocks
- repetitive validation code
- large configuration blocks
- full exception handling
- debugging code
- verbose print statements

Keep most code snippets around 3–10 lines.

Use monospace formatting for code.

---

Document Formatting Requirements

The document must be readable by business SMEs.

Use:

- clear section headings
- short paragraphs
- simple terminology
- business-oriented explanations
- tables where useful
- limited technical jargon
- concise code snippets only

When using technical terms such as:

- MLflow
- Unity Catalog
- model version
- Champion
- Candidate
- model signature
- batch scoring
- feature drift
- rollback

explain each term the first time it appears.

Do not include:

- notebook execution instructions
- notebook-by-notebook summaries
- POC achievement checklists
- unnecessary setup details
- implementation logs
- repeated "Step completed successfully" messages
- unnecessary technical troubleshooting
- invented results

The final document should feel like a concise technical-business explanation of the implemented MLOps lifecycle that a business SME can read from beginning to end and understand what was done and why.
