Paste this prompt into Copilot:
Create a new Python file named:
train_logistic_regression.py
Do not modify the existing validation, preprocessing, or split scripts.
Use these input files:
churn_X_train.csv
churn_X_test.csv
churn_y_train.csv
churn_y_test.csv
Create a beginner-friendly Python script using pandas and scikit-learn to train and evaluate a baseline Logistic Regression churn model.
Requirements:
Read all four CSV files.
Treat these columns as categorical:
PRODUCT_ID
SCHEME_ID
Treat all remaining feature columns as numeric.
Build a scikit-learn preprocessing pipeline using:
OneHotEncoder(handle_unknown="ignore") for categorical columns
StandardScaler() for numeric columns
Build a Logistic Regression model using:
LogisticRegression(
    max_iter=1000,
    class_weight="balanced",
    random_state=42
)
Combine preprocessing and model training using a single Pipeline.
Train the model only on the training dataset.
Generate predictions and churn probabilities for the test dataset.
Calculate and print:
ROC-AUC
PR-AUC / Average Precision
Accuracy
Precision for churn class
Recall for churn class
F1-score for churn class
Confusion matrix
Classification report
Use the default classification threshold of 0.50.
Also print:
training row count
testing row count
number of numeric features
number of categorical features
training time
prediction time
Save the evaluation metrics as:
logistic_regression_metrics.csv
Save the test predictions as:
logistic_regression_test_predictions.csv
The prediction output must contain:
actual_target
predicted_target
churn_probability
Save the complete fitted preprocessing and Logistic Regression pipeline as:
logistic_regression_pipeline.joblib
Add clear comments and basic error handling for missing files, missing columns, invalid target values, training failure, and save failure.
Do not train Random Forest, XGBoost, or any other model yet.
At the end, explain how to run:
python train_logistic_regression.py
