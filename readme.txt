Create a new Python file named:
prepare_model_dataset.py
Use the existing validated file:
dataset.csv
Create a beginner-friendly pandas script that produces a model-safe dataset by removing target-support and leakage columns.
Requirements:
Read:
csv_file = r"dataset.csv"
Keep ACCOUNT_ID for traceability.
Keep target_churn as the target column.
Keep all valid historical feature columns, including:
transaction features
contribution features
rollover features
raw partial-withdrawal features
significant partial-withdrawal features
PRODUCT_ID
SCHEME_ID
tenure and other pre-as_of_date features
Remove these leakage or target-support columns if present:
as_of_date
feature_start_date
outcome_start_date
outcome_end_date
account_status_code_outcome
account_exit_date
account_closed_outcome_flag
outcome_external_rollover_flag
outcome_external_rollover_count
outcome_external_rollover_amount
outcome_external_exit_type_id
outcome_external_exit_type_code
outcome_external_exit_reason_code
death_exit_outcome_flag
exclude_from_training_flag
Also remove any column whose name contains:
outcome_
exit_date
death_exit
exclude_from_training
account_closed
except target_churn.
Validate after removal that:
ACCOUNT_ID exists
target_churn exists
ACCOUNT_ID has no nulls
ACCOUNT_ID has no duplicates
target_churn contains only 0 and 1
no leakage columns remain
row count remains 793915
Print:
original shape
final shape
removed column names
remaining column names
target distribution
Save the model-safe output as:
model_dataset.csv
Do not preprocess, split, or train any model yet.
Add clear comments and error handling.
Run using:
python prepare_model_dataset.py
