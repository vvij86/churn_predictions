You can share a high-level ML build flow like this:

1. Data Exploration
Understand MercerEdgeDB tables, relationships, data quality, history, and identify potential churn-driver columns.


2. Churn Target & Modelling Dataset Definition
Finalise what counts as churn, feature window, future outcome window, exclusions, account grain, and required source fields.


3. Data Preparation
Join the required source tables, clean the data, apply business rules, and create the account-level modelling dataset.


4. Feature Engineering
Create meaningful ML features such as tenure, transaction activity, contributions, rollover behaviour, withdrawals, engagement, etc.


5. Feature Validation & Selection
Check missing values, leakage, duplicates, low-value/constant fields, and select useful model features.


6. Train / Test Preparation
Prepare categorical/numeric fields and split the dataset into training and testing sets.


7. Model Development
Train baseline and candidate models such as Logistic Regression, Decision Tree, Random Forest, XGBoost, etc.


8. Hyperparameter Tuning
Test different model configurations to improve performance.


9. Model Evaluation & Selection
Compare ROC-AUC, PR-AUC, precision, recall, F1, confusion matrix, and scalability, then select the preferred model.


10. Model Explainability
Identify important churn drivers and explain why customers/accounts receive higher risk scores.


11. Model Registration / MLOps
Track experiments and register the approved model in MLflow.


12. Scoring Pipeline
Use latest account data and the approved model to generate churn probability, predicted churn, and risk bands.


13. Validation / Backtesting
Compare predictions with actual later outcomes and confirm model performance.


14. Deployment / Integration
Publish model outputs to downstream consumers such as Power BI, Salesforce, tables, or an API endpoint.



For Teams, you can send a shorter version:

> Hi Sai, the high-level ML build steps I’m planning are:
Data Exploration → Churn Target & Dataset Definition → Data Preparation → Feature Engineering → Feature Validation/Selection → Train/Test Preparation → Model Development → Hyperparameter Tuning → Model Evaluation & Selection → Explainability → MLflow Registration → Scoring Pipeline → Backtesting/Validation → Deployment/Integration.

I’ll also break these down into stories/tasks with estimates for the first ML build.
