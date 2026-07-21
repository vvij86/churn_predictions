Create a new Python file named:
preprocess_and_split_model_dataset.py
Use:
model_dataset.csv
Create a beginner-friendly Python script to preprocess and split the model-safe churn dataset.
Requirements:
Read model_dataset.csv.
Remove constant columns, including min_partial_withdrawal_amount. Also detect and remove any other column having only one unique value.
Keep ACCOUNT_ID separately for traceability and do not use it as a model feature.
Keep target_churn separately as the target.
Treat these as categorical features:
account_type_code
product_id
scheme_id
For these recency columns:
days_since_last_account_txn
days_since_last_contribution
days_since_last_rollover
days_since_last_partial_withdrawal_12m
days_since_last_significant_partial_withdrawal_12m
create corresponding no-history indicator columns based on their related count being zero.
When the related count is zero, replace the recency value with 366.
Use these count mappings:
account_txn_count_12m -> days_since_last_account_txn
contrib_txn_count_12m -> days_since_last_contribution
rollover_event_count_12m -> days_since_last_rollover
partial_withdrawal_count_12m -> days_since_last_partial_withdrawal_12m
significant_partial_withdrawal_count_12m -> days_since_last_significant_partial_withdrawal_12m
Create a stratified 80/20 train-test split using:
test_size=0.20
random_state=42
stratify=y
Ensure the same ACCOUNT_ID does not appear in both train and test sets.
Print:
original shape
final feature count
removed constant columns
train and test shapes
train and test target distributions
counts of newly created no-history indicators
account-ID overlap count
Save:
churn_X_train.csv
churn_X_test.csv
churn_y_train.csv
churn_y_test.csv
churn_train_account_ids.csv
churn_test_account_ids.csv
Do not one-hot encode or scale the data yet.
Do not train or evaluate any model yet.
Add clear comments and error handling.
Run using:
python preprocess_and_split_model_dataset.py
