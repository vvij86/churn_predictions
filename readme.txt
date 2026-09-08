
For the first ML build by the first week of October, you can estimate the stories like this, assuming 1 day = 6 hours:

Story	Estimate

Data Exploration & Churn Driver Identification	12 hrs / 2 days
Churn Target & Modelling Dataset Definition	12 hrs / 2 days
Feature Engineering & Model Dataset Preparation	24 hrs / 4 days
Data Validation & Train/Test Preparation	12 hrs / 2 days
Baseline & Candidate Model Development	18 hrs / 3 days
Model Evaluation & First Model Selection	12 hrs / 2 days
First Scoring Output / Churn Prediction Build	12 hrs / 2 days


Total: 102 hours = 17 working days

This is a reasonable estimate for a first ML build, assuming MercerEdgeDB access is ready and the churn definition/business rules do not require major rework.

For planning, I would keep hyperparameter tuning, explainability, MLflow registration, production deployment, API endpoint, monitoring, and retraining as later stories rather than including them in the October first-build scope.
