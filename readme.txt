Create a new Python file named:
train_logistic_regression.py
Use these input files:
churn_X_train.csv
churn_X_test.csv
churn_y_train.csv
churn_y_test.csv
churn_test_account_ids.csv
Create a beginner-friendly Python script using pandas and scikit-learn to train and evaluate a Logistic Regression churn model.
Requirements:
Read all five input files.
Treat these columns as categorical:
product_id
scheme_id
Treat all other feature columns as numeric.
Build a preprocessing pipeline using:
OneHotEncoder(handle_unknown="ignore") for categorical columns
StandardScaler() for numeric columns
Build the model using:
LogisticRegression(
    max_iter=1000,
    class_weight="balanced",
    random_state=42
)
Combine preprocessing and model training using a single scikit-learn Pipeline.
Train only on the training dataset.
Generate test predictions and churn probabilities.
Evaluate using the default threshold of 0.50.
Calculate and print:
ROC-AUC
PR-AUC / Average Precision
Accuracy
Precision for churn class
Recall for churn class
F1-score for churn class
Confusion matrix
Classification report
training time
prediction time
Save evaluation metrics as:
logistic_regression_metrics.csv
Save test predictions as:
logistic_regression_test_predictions.csv
The prediction file must contain:
ACCOUNT_ID
actual_target
predicted_target
churn_probability
Save the fitted pipeline as:
logistic_regression_pipeline.joblib
Add clear comments and error handling.
Do not train any other model yet.
Run using:
python train_logistic_regression.py
