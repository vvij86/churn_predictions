Paste this into Copilot, then paste your complete original 41-column SQL query underneath it.


---

I have an existing SQL Server query used to create a churn model training dataset. The original query returns 41 columns.

I now need a separate scoring dataset query to generate new records for prediction using the already-trained model.

Scoring dates

Feature window start: 2025-04-01
As-of date:           2026-03-31
Prediction period:    2026-04-01 to 2026-06-30

The prediction period is for business interpretation only. Do not use any data after 2026-03-31 in the scoring dataset.

Main requirement

Create a scoring version of the original training query.

Reuse the original:

tables and joins;

account cohort logic;

feature definitions;

SQL data types;

column names;

transaction logic;

contribution logic;

rollover logic;

partial-withdrawal logic.


Do not redesign or simplify the feature calculations unless necessary.

Scoring query requirements

1. Set the dates once at the beginning, preferably using variables:



DECLARE @FeatureStartDate DATE = '2025-04-01';
DECLARE @AsOfDate DATE = '2026-03-31';

2. Produce one row per account_id, as of 2026-03-31.


3. Include only accounts that are active as of 2026-03-31, using the same active-account definition as the original training query.


4. Calculate all behavioural features using data from:



2025-04-01 through 2026-03-31

5. Do not use any event, transaction, account status or other information after 2026-03-31.


6. Preserve the original feature definitions exactly, including:



account tenure;

account transaction count;

distinct transaction-type count;

reversal transaction count;

transaction recency;

contribution count;

contribution amount;

active contribution months;

contribution recency;

rollover count;

rollover amount;

rollover recency;

partial-withdrawal count;

partial-withdrawal amount;

partial-withdrawal recency;

partial-withdrawal flags;

significant partial-withdrawal features;

product and scheme fields;

missing-history indicators, where present.


7. Preserve the original partial-withdrawal business rule:



Event type codes ETC, ETCV, FLCL and PFCO are closure-like events
and must have partialWithdrawalFlag = 0.

Other qualifying event types may have partialWithdrawalFlag = 1.

Retain the provisional significant partial-withdrawal threshold of 100, or use the existing SQL parameter if the original query already defines one.

8. Keep account_id in the final output as an identifier only.


9. Keep as_of_date as scoring metadata only.


10. Do not use account_id or as_of_date as model features.


11. The original SQL produces 41 columns. Remove all future-outcome, target, exclusion and target-audit fields from the scoring output.



The following original columns must not appear in the scoring dataset:

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
target_churn

12. Do not simply remove these fields from the final SELECT. Review the upstream CTEs and remove or adjust outcome-related CTEs that are no longer required.


13. Do not create an actual churn target for 2026-04-01 to 2026-06-30. Those outcomes will be created later in a separate evaluation query, after the outcome period is complete.


14. Preserve the original pre-outcome SQL output columns where appropriate. However, distinguish between:



identifier columns;

reporting metadata;

actual model-input columns.


15. Note that account_type_code was constant in the original model-development dataset and may have been removed before training. Flag this for verification rather than automatically using it as a model feature.


16. Add clear SQL comments for:



parameters;

active-account cohort;

feature window;

transaction features;

contribution features;

rollover features;

partial-withdrawal features;

final scoring output.


Required response

Please provide:

1. The complete scoring SQL query.


2. A list of CTEs removed or modified from the training query.


3. A list of columns removed because they relate to the future outcome, exclusion or target.


4. The final scoring SQL output column list.


5. A separate list of fields that should be passed to the trained Python pipeline.


6. Any assumptions or items requiring manual validation.


7. A validation checklist confirming:

one row per account;

no duplicate account IDs;

no information after 2026-03-31;

same feature definitions as training;

compatible column names and data types;

no target leakage;

no future-outcome fields.




Important Python compatibility point

The definitive model-input schema is the column list from the original Python X_train dataframe, not simply all 41 SQL columns or all retained scoring columns.

The scoring dataframe passed into the saved pipeline must match the original X_train columns exactly.

Original 41-column training SQL query

PASTE THE COMPLETE ORIGINAL SQL QUERY HERE


---
