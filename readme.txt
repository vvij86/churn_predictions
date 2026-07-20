The validation shows that dataset.csv contains 793,915 unique account rows, but it has only 12 columns and mostly contains target-supporting/outcome columns.
The file currently includes columns such as:
account_status_code
account_exit_date
account_closed_outcome
outcome_external_rollover fields
death_exit_outcome_flag
exclude_from_training_flag
target_churn
These outcome columns must not be used as ML features because they would cause target leakage.
Review my final SQL churn dataset query and modify only its final export SELECT.
Create a modelling export containing:
account_id
all valid historical feature columns calculated using data on or before as_of_date
target_churn
Exclude all outcome-window and target-supporting columns, including:
account exit date
current account status
account closure outcome flags
outcome external rollover flags, counts and amounts
death outcome flags
exclude-from-training flag
exit type and exit reason
Keep the existing CTE and target logic unchanged.
Return only the corrected final SELECT and WHERE section.
Do not generate Python or train a model yet.
