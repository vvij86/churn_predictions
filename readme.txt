Update the existing file:
preprocess_and_split_model_dataset.py
The script currently fails with:
Missing required categorical columns after constant removal: ['account_type_code']
Fix the logic as follows:
Keep these as candidate categorical columns:
account_type_code
product_id
scheme_id
Detect and remove constant columns first.
After constant-column removal, automatically keep only the categorical columns that still exist.
Do not raise an error when a candidate categorical column was removed because it was constant.
Print:
Categorical columns retained
Categorical columns removed as constants
Continue preprocessing and stratified train-test splitting using the remaining columns.
Keep all existing no-history indicator logic, recency replacement logic, traceability checks and output file creation unchanged.
Do not train any model yet.
Run the corrected script using:
python preprocess_and_split_model_dataset.py
