Create Databricks Python notebook cells to train a Random Forest churn prediction model using existing train/test CSV files from my workspace folder structure.

Context:
I do not have permission to create a Unity Catalog schema, so do not use Unity Catalog model registration.
Do not use mlflow.set_registry_uri("databricks-uc").
Do not register the model in Unity Catalog.
Focus on MLflow Experiment Tracking only.

Folder structure:
- Root folder: /Workspace/Users/vijay.vignesh@marsh.com/Model_Eval_Poc
- Training features: Training_ds/churn_X_train.csv
- Training target: Training_ds/churn_y_train.csv
- Test features: Test_ds/churn_X_test.csv
- Test target: Test_ds/churn_y_test.csv

Requirements:
1. Load churn_X_train.csv, churn_y_train.csv, churn_X_test.csv and churn_y_test.csv.
2. Do not split the dataset again because train/test files are already available.
3. Validate row counts between X_train and y_train, and X_test and y_test.
4. Convert all feature columns to float64 before training.
5. Train RandomForestClassifier using scikit-learn.
6. Enable mlflow.sklearn.autolog(log_models=True).
7. Set an MLflow experiment path under:
   /Users/vijay.vignesh@marsh.com/Model_Eval_Poc/mlflow_experiments
8. Start an MLflow run with run_name = "Random_Forest_Churn_Model".
9. Evaluate using Accuracy, Precision, Recall, F1 Score, ROC AUC, Classification Report and Confusion Matrix.
10. Manually log important custom metrics to MLflow also:
    - custom_accuracy
    - custom_precision
    - custom_recall
    - custom_f1_score
    - custom_roc_auc
11. Log the confusion matrix as an MLflow artifact.
12. Log feature importance as an MLflow artifact.
13. Log the trained Random Forest model as an MLflow model artifact, but do not register it.
14. Predict one sample customer and print stay/churn probability.
15. Do not save separate CSV files to Output_Metrics.
16. Do not use Hyperopt or XGBoost because they are not available in my Databricks environment.
17. Generate clean step-by-step Databricks notebook cells.
