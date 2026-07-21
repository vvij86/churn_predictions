Create a new Python file named:

train_logistic_regression.py

Use these input files:

churn_X_train.csv
churn_X_test.csv
churn_y_train.csv
churn_y_test.csv
churn_test_account_ids.csv

Create a beginner-friendly Python script using pandas, scikit-learn and joblib to train, evaluate and interpret a Logistic Regression churn model.

Requirements:

1. Read all five input files.


2. Validate that the train and test feature files have matching columns.


3. Validate that the target files contain only 0 and 1.


4. Validate that the number of rows matches correctly between:



churn_X_train.csv
churn_y_train.csv

and between:

churn_X_test.csv
churn_y_test.csv
churn_test_account_ids.csv

5. Treat these columns as categorical features:



product_id
scheme_id

6. Treat all remaining feature columns as numeric.


7. Do not use ACCOUNT_ID as a model feature.


8. Build a scikit-learn preprocessing pipeline using:



OneHotEncoder(handle_unknown="ignore")

for categorical columns and:

StandardScaler()

for numeric columns.

9. Build the Logistic Regression model using:



LogisticRegression(
    max_iter=1000,
    class_weight="balanced",
    random_state=42
)

10. Combine preprocessing and Logistic Regression using a single scikit-learn Pipeline.


11. Train the pipeline only on the training dataset.


12. Generate predictions and churn probabilities for the test dataset.


13. Use the default classification threshold of 0.50.


14. Calculate and print:



ROC-AUC

PR-AUC / Average Precision

Accuracy

Precision for churn class

Recall for churn class

F1-score for churn class

Confusion matrix

Classification report

training row count

test row count

numeric feature count

categorical feature count

training time

prediction time


15. Save the evaluation metrics as:



logistic_regression_metrics.csv

16. Save the test predictions as:



logistic_regression_test_predictions.csv

The prediction file must contain:

ACCOUNT_ID
actual_target
predicted_target
churn_probability

17. Save the complete fitted preprocessing and Logistic Regression pipeline as:



logistic_regression_pipeline.joblib

18. After training, extract the final transformed feature names from the fitted preprocessing pipeline, including one-hot encoded product_id and scheme_id values.


19. Extract the Logistic Regression coefficients and create a dataframe with:



feature_name
coefficient
absolute_coefficient
direction
driver_group

20. Set direction as:



Increases churn risk

when the coefficient is positive, and:

Reduces churn risk

when the coefficient is negative.

21. Set driver_group as:



Product/Scheme association

for one-hot encoded product_id and scheme_id features, and:

Behavioural driver

for all other features.

22. Sort the coefficient dataframe by absolute_coefficient in descending order.


23. Save all coefficients as:



logistic_regression_churn_drivers.csv

24. Save the top 30 drivers as:



logistic_regression_top_churn_drivers.csv

25. Print:



top 15 features increasing churn risk

top 15 features reducing churn risk

top 10 behavioural drivers by absolute coefficient

top 10 product/scheme associations by absolute coefficient


26. Add a warning that Logistic Regression coefficients show model association and not confirmed business causation.


27. Add clear comments and error handling for:



missing input files

missing required columns

mismatched row counts

invalid target values

preprocessing failure

model training failure

feature-name extraction failure

output save failure


28. Do not train Random Forest, XGBoost or any other model yet.


29. At the end, explain how to run:



python train_logistic_regression.py
