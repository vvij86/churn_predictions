Create a new Python file named:

split_churn_dataset.py

Do not modify the existing files:

validate_churn_dataset.py
preprocess_churn_dataset.py

Use churn_prepared_dataset.csv as the input file.

Create a beginner-friendly Python script using pandas and scikit-learn to split the prepared churn dataset into training and testing datasets.

Requirements:

1. Read:



csv_file = r"churn_prepared_dataset.csv"

2. Validate that these columns exist:



ACCOUNT_ID
PRODUCT_ID
SCHEME_ID
target_churn

3. Keep ACCOUNT_ID separately for traceability and do not use it as a model feature.


4. Separate:



X = all model feature columns
y = target_churn
account_ids = ACCOUNT_ID

5. Treat PRODUCT_ID and SCHEME_ID as categorical columns, not continuous numeric variables.


6. Create a stratified 80/20 train-test split using:



test_size=0.20
random_state=42
stratify=y

7. Split account_ids using the same train-test indices so account traceability is preserved.


8. Print:



total dataset shape

X_train shape

X_test shape

y_train shape

y_test shape

train target counts and percentages

test target counts and percentages

train and test account ID counts

confirmation that no ACCOUNT_ID appears in both train and test


9. Save these four files with headers:



churn_X_train.csv
churn_X_test.csv
churn_y_train.csv
churn_y_test.csv

10. Also save traceability files:



churn_train_account_ids.csv
churn_test_account_ids.csv

11. Do not encode categorical columns yet.


12. Do not scale numeric columns yet.


13. Do not train or evaluate any ML model yet.


14. Add clear comments and basic error handling for:



missing input file

missing required columns

invalid target values

failure while saving output files


15. At the end, explain how to run the file from the VS Code terminal:



python split_churn_dataset.py
