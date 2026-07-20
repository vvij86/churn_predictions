I have exported the corrected churn modelling dataset as dataset.csv with column headers.
The file should contain approximately 793,990 rows, one row per ACCOUNT_ID, historical feature columns, and target_churn.
Create a beginner-friendly Python validation script using pandas.
The script must:
Read:
csv_file = r"dataset.csv"
Print:
row count
column count
all column names
first five rows
data types
Validate:
ACCOUNT_ID has no null values
ACCOUNT_ID has no duplicates
target_churn has no null values
target_churn contains only 0 and 1
row count is approximately 793,990
Show:
target class counts and percentages
null count and null percentage for every column
unique count for every column
constant columns
columns with more than 80% null values
infinite values in numeric columns
total dataframe memory usage
Check that no target-leakage columns are present, including:
account exit date
account status
account closure outcome
external rollover outcome fields
death outcome flag
exclude-from-training flag
exit type
exit reason
Save the validation summary as:
churn_model_dataset_validation_summary.csv
Do not preprocess the data and do not train any ML model yet.
Add clear comments and explain how to run the script in VS Code.
