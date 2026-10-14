Before proceeding to Step 2, review the current Step 1 SQL:

build_merceredge_feature_dataset_step1.sql

I noticed that target_churn is not present in the final Step 1 dataset output.

Please correct this carefully.

IMPORTANT:
- Do not redesign or recalculate the churn target logic.
- Reuse the already approved target logic from the base historical dataset.
- Keep target_churn separate from predictive feature columns.
- target_churn is the ML label only and must never be used as an input feature.
- Keep the current eligibility, death exclusion, internal-transfer exclusion, AsOfDate and outcome-window logic unchanged.

Please add the following fields to the final Step 1 dataset where available:
- target_churn
- retained_flag
- future_exit_in_outcome_window_flag
- internal_transfer_exclusion_flag
- death_exclusion_flag
- historical_eligibility_status
- is_eligible_for_modelling

VALIDATION REQUIRED

After adding target_churn, validate:

1. Count of target_churn = 1
2. Count of target_churn = 0
3. Count of target_churn IS NULL
4. Confirm all target_churn = 1 rows:
   - are eligible for modelling
   - have exit_date > @AsOfDate
   - have exit_date <= @OutcomeEndDate
   - are not internal transfers
   - are not death exclusions
5. Confirm all eligible accounts without qualifying churn in the outcome window have target_churn = 0
6. Confirm ineligible accounts have target_churn = NULL, if that is how the approved base logic is designed
7. Confirm no future-join account has target_churn = 0 or 1
8. Confirm no account exited on/before @AsOfDate is assigned target_churn = 1
9. Confirm no death-excluded account is assigned target_churn = 1
10. Confirm no internal-transfer account is assigned target_churn = 1
11. Confirm one row per account_id + as_of_date is still preserved
12. Confirm row counts are not duplicated after adding the target fields

At the end, show a summary with:

- total eligible rows
- churn rows
- retained rows
- null target rows
- churn rate
- duplicate count
- any invalid target assignments
- confirmation that target_churn is a label only and not part of the predictive feature list

Do not start Step 2 yet.
Stop after adding and validating the target fields.
