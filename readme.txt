Update ONLY the Partial Rollover / Withdrawal Behaviour section in behavioural_features_business_review.sql.

Objective:
Add percentage-based partial rollover features because the business review comment indicates that partial rollover outflow amounts and percentages are useful.

Important rules:
- Do not change any other feature block.
- Keep the modelling grain at one row per accountID per AsOfDate.
- Preserve all existing partial rollover features and existing business rules.
- Do not introduce post-AsOfDate leakage.
- Do not use future AccountInvestment records.
- Do not invent a denominator.
- Use the existing AccountInvestment logic / source only if it can provide a valid account-level FUM value as of @AsOfDate.

Existing partial rollover features that must remain:
- partial_rollover_count_12m
- partial_rollover_amount_12m
- days_since_last_partial_rollover
- recent_partial_rollover_count_90d
- recent_partial_rollover_amount_90d

New features to add:
1. partial_rollover_pct_12m
2. recent_partial_rollover_pct_90d

Denominator:
Use the account-level current FUM derived from:
edgeSource.accountInvestment.total_investment_value_asof

But first validate the AccountInvestment logic:
- identify the appropriate date/snapshot column in AccountInvestment
- for each eligible account, select the latest valid investment/FUM record ON OR BEFORE @AsOfDate
- never use a record after @AsOfDate
- ensure only one FUM value per account is joined into the partial rollover feature calculation
- if multiple investment rows exist for the same account/snapshot, determine whether total_investment_value_asof is already account-total or requires aggregation; do not double count
- preserve NULL when no valid as-of FUM is available
- do not replace missing FUM with 0

Calculate:

partial_rollover_pct_12m =
    partial_rollover_amount_12m / current_account_fum_amount

recent_partial_rollover_pct_90d =
    recent_partial_rollover_amount_90d / current_account_fum_amount

Use safe SQL such as:
CASE
    WHEN current_account_fum_amount > 0
    THEN CAST(partial_rollover_amount_12m AS DECIMAL(18,6))
         / current_account_fum_amount
    ELSE NULL
END

and equivalent logic for the recent 90-day amount.

Return the ratio as a decimal, for example:
0.25 = 25%

Do not multiply by 100 unless the existing feature convention explicitly stores percentage values as 0-100.

Business meaning:
- partial_rollover_pct_12m = proportion of account FUM rolled out partially during the previous 12 months
- recent_partial_rollover_pct_90d = proportion of account FUM rolled out partially during the previous 90 days

This should allow the model to distinguish, for example:
- $5,000 rollover from a $20,000 account = materially large outflow
- $5,000 rollover from a $500,000 account = relatively small outflow

Also expose or reuse:
current_account_fum_amount

Validation required after the change:
1. Confirm no AccountInvestment record after @AsOfDate enters the calculation.
2. Confirm final duplicate accountID count = 0.
3. Confirm final grain remains one row per accountID.
4. Confirm current_account_fum_amount is NULL when no valid as-of investment record exists.
5. Confirm partial_rollover_pct_12m and recent_partial_rollover_pct_90d are NULL when FUM is NULL or <= 0.
6. Show min, median, average, max and non-null account count for both percentage features.
7. Show 10 sample accounts containing:
   accountID,
   current_account_fum_amount,
   partial_rollover_amount_12m,
   partial_rollover_pct_12m,
   recent_partial_rollover_amount_90d,
   recent_partial_rollover_pct_90d.
8. Check whether any percentage is > 1.0. Do NOT automatically cap it; report the cases because multiple partial rollovers during the window could legitimately exceed the AsOfDate FUM.
9. Confirm all five existing partial rollover features are unchanged.

Before editing SQL, show:
- AccountInvestment date column being used
- how the as-of FUM record is selected
- whether total_investment_value_asof is already account-level or needs aggregation

Then make the minimal SQL change and provide a short PASS / REVIEW / FAIL summary.
