Create a new Python file named:

preprocess_churn_dataset.py

Do not modify the existing validate_churn_dataset.py file.

The validation of dataset.csv has passed. It contains 793,990 unique account rows, 17 columns, no nulls, no duplicates, valid binary target values, and no target-leakage columns.

In the new preprocess_churn_dataset.py file, create a beginner-friendly pandas preprocessing script.

Requirements:

1. Read:



csv_file = r"dataset.csv"

2. Remove ACCOUNT_TYPE_CODE because it is a constant column.


3. Keep ACCOUNT_ID separately for traceability, but do not include it as a model feature.


4. For these recency columns:



txn_days_since_last_12m

contrib_days_since_last_12m

rollover_days_since_last_12m


Create corresponding no-history indicator columns:

no_txn_history_12m

no_contrib_history_12m

no_rollover_history_12m


5. Determine no-history using the related event count:



txn_count_12m = 0

contrib_count_12m = 0

rollover_count_12m = 0


Do not determine no-history only from the recency value.

6. When the related event count is zero, replace its recency value with 366, representing no event during the 12-month observation window.


7. Keep PRODUCT_ID and SCHEME_ID as categorical features.


8. Separate:



X for model features

y for target_churn

account_ids for traceability


9. Print:



input dataset shape

prepared dataset shape

final feature names

X shape

y shape

account_ids shape

counts for each newly created no-history indicator


10. Save the prepared output with headers as:



churn_prepared_dataset.csv

The saved file should contain:

ACCOUNT_ID

all prepared model features

target_churn


11. Add clear comments and basic error handling for:



missing dataset.csv

missing required columns

failure while saving the output


12. Do not split the dataset and do not train or evaluate any model yet.


13. At the end, explain how to run the new file from the VS Code terminal using:



python preprocess_churn_dataset.py
