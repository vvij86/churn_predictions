Yes. Here is the updated 15-step end-to-end ML model flow, adjusted so Step 2 and Step 4 are clearly different and aligned with your Databricks/medallion setup.

1. Confirm business problem and modelling rules
Define churn, retained, exclusions, eligibility, account-level grain, feature window, as-of date, outcome window, and leakage rules.


2. Identify source data and candidate feature columns
From the Databricks Silver/Gold tables, identify which tables and raw columns are relevant for churn modelling. Confirm joins, account/member mapping, date fields, and candidate churn-driver columns.


3. Prepare the base modelling population
Create the eligible account population at: one row per account_id per as_of_date
Retain member number only as a reference field and apply agreed eligibility rules.


4. Engineer model features
Convert raw source columns into model-ready features such as:

contribution_count_12m

contribution_amount_12m

months_since_last_contribution

web_activity_count_3m

helpline_contact_count_6m

rollover_out_amount_12m

net_money_flow_12m

tenure_months



5. Create the churn target
Using the agreed outcome window:

target_churn = 1 for qualifying churn

target_churn = 0 for retained
Exclude agreed cases such as death exits and ensure future information is not used as features.



6. Perform data-quality and modelling-dataset validation
Check:

duplicates

nulls

missing accounts

feature coverage

class distribution

invalid dates

leakage

one row per account + as-of date



7. Define train, validation and test periods
Use a time-based approach, not a random split.

Example:

older period → training

later period → validation

most recent complete period → final holdout test



8. Define time-based cross-validation folds
Example:

Fold 1
Train: Jan-Dec 2024
Validate: Jan-Mar 2025

Fold 2
Train: Jan 2024-Mar 2025
Validate: Apr-Jun 2025

Fold 3
Train: Jan 2024-Jun 2025
Validate: Jul-Sep 2025

If Jul-Sep 2025 is reserved as the final holdout, use earlier periods for the folds instead.


9. Iteration 1 – Compare algorithms
Train and compare models such as:

Logistic Regression

Decision Tree

Random Forest

HistGradientBoosting

XGBoost


Compare them using the same folds.


10. Iteration 2 – Improve shortlisted models
For the stronger models:

tune hyperparameters

refine features

handle class imbalance if required

tune probability threshold



11. Select and freeze the final model
Choose the final model based on:

performance

stability across time folds

precision/recall trade-off

explainability

business requirements



12. Final holdout testing
Evaluate the frozen model on the untouched final test period and calculate final metrics such as:

ROC AUC

PR AUC

Precision

Recall

F1

Confusion Matrix



13. Explainability and business validation
Review important churn drivers, reason codes, risk bands, and whether the model behaviour makes business sense.


14. Register, deploy and operationalize the model
In Databricks/MLflow:

track experiments

register/version the model

assign Champion/Candidate

create the scoring workflow

provide outputs to Power BI/downstream consumers



15. Monitor and retrain
Monitor:

data quality

feature drift

prediction distribution

model performance


Retrain when enough new labelled data becomes available, on an agreed schedule, or when performance degrades.



A short version for your lead is:

> Business rules → Source/feature identification → Base population → Feature engineering → Target creation → Dataset validation → Time-based train/validation/test → Cross-validation → Algorithm comparison → Tuning → Final model selection → Holdout test → Explainability → Deployment/scoring → Monitoring/retraining.
