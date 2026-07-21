Create a new Python file named:

validate_churn_dataset.py

The workspace currently contains only the latest revised dataset.csv with column headers. All previous Python files and generated CSV files were deleted.

Create a beginner-friendly pandas validation script for the latest churn modelling dataset.

Requirements:

1. Read:



csv_file = r"dataset.csv"

2. Print:



row count

column count

all column names

first five rows

data types


3. Validate:



ACCOUNT_ID has no null values

ACCOUNT_ID has no duplicates

target_churn has no null values

target_churn contains only 0 and 1

row count is approximately 793915

distinct account count equals row count


4. Confirm these raw partial-withdrawal columns are present:



partial_withdrawal_count_12m
partial_withdrawal_amount_12m
days_since_last_partial_withdrawal_12m
partial_withdrawal_flag_12m

5. Confirm these threshold-based partial-withdrawal columns are present:



significant_partial_withdrawal_count_12m
significant_partial_withdrawal_amount_12m
days_since_last_significant_partial_withdrawal_12m
significant_partial_withdrawal_flag_12m

6. Validate the threshold logic:



significant_partial_withdrawal_count_12m must never be greater than partial_withdrawal_count_12m

significant_partial_withdrawal_amount_12m must never be greater than partial_withdrawal_amount_12m

whenever significant_partial_withdrawal_flag_12m = 1, partial_withdrawal_flag_12m must also be 1

whenever significant_partial_withdrawal_count_12m = 0, significant_partial_withdrawal_flag_12m must be 0

whenever significant_partial_withdrawal_count_12m > 0, significant_partial_withdrawal_flag_12m must be 1


7. Show counts for:



raw partial-withdrawal accounts

significant partial-withdrawal accounts

accounts with raw withdrawals only below the threshold

accounts having both raw and significant withdrawals


8. Show:



target class counts and percentages

null count and null percentage for every column

unique count for every column

constant columns

columns with more than 80% null values

infinite values in numeric columns

total dataframe memory usage


9. Check that no target-leakage columns are present, including names containing:



account_exit_date
account_status
account_closed_outcome
outcome_external_rollover
death_exit_outcome
exclude_from_training
exit_type
exit_reason

10. Save the validation summary as:



churn_model_dataset_validation_summary.csv

11. Add clear comments and basic error handling for:



missing dataset.csv

missing required columns

invalid target values

validation failures

failure while saving the output file


12. Do not preprocess the data and do not train any model yet.


13. At the end, explain how to run:



python validate_churn_dataset.py
