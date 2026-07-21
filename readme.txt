Create a new Python file named:

extract_logistic_churn_drivers.py

Do not retrain the model.

Use the existing saved model:

logistic_regression_pipeline.joblib

Create a beginner-friendly Python script that:

1. Loads the saved pipeline using joblib.


2. Extracts the fitted preprocessing step and Logistic Regression model.


3. Gets the final transformed feature names, including one-hot encoded PRODUCT_ID and SCHEME_ID values.


4. Extracts the Logistic Regression coefficients.


5. Creates a dataframe containing:

feature_name

coefficient

absolute_coefficient

direction



6. Set direction as:

Increases churn risk when coefficient is positive

Reduces churn risk when coefficient is negative



7. Sort features by absolute_coefficient in descending order.


8. Print:

top 15 features increasing churn risk

top 15 features reducing churn risk



9. Save the complete result as:



logistic_regression_churn_drivers.csv

10. Also save the top 30 drivers as:



logistic_regression_top_churn_drivers.csv

11. Add a warning that Logistic Regression coefficients show model association, not necessarily business causation.


12. Add clear comments and error handling for:



missing model file

invalid pipeline structure

failure while extracting feature names

failure while saving output files


13. At the end, explain how to run:



python extract_logistic_churn_drivers.py
