Update ONLY the Partial Rollover / Withdrawal Behaviour section in "behavioural_features_business_review.sql".

The current percentage calculation uses:

partial_rollover_amount / current_account_fum_amount

This can produce values greater than 100% because current FUM is the remaining balance after historical outflows.

Please change the percentage calculation to represent the proportion of funds rolled out relative to rolled-out amount plus remaining FUM.

Use:

partial_rollover_pct_12m =
partial_rollover_amount_12m /
(current_account_fum_amount + partial_rollover_amount_12m)

recent_partial_rollover_pct_90d =
recent_partial_rollover_amount_90d /
(current_account_fum_amount + recent_partial_rollover_amount_90d)

Requirements:

1. Keep these existing Partial Rollover features unchanged:
   
   - partial_rollover_count_12m
   - partial_rollover_amount_12m
   - days_since_last_partial_rollover
   - recent_partial_rollover_count_90d
   - recent_partial_rollover_amount_90d

2. Keep:
   
   - current_account_fum_amount
   - partial_rollover_pct_12m
   - recent_partial_rollover_pct_90d

3. Use point-in-time AccountInvestment data only:
   
   - investmentDate <= @AsOfDate
   - latest investment record per account/investment option
   - aggregate to account-level FUM
   - no future records

4. Handle denominator safely:
   
   - return NULL where denominator is NULL or <= 0
   - do not force NULL values to zero

5. Do not multiply by 100. Keep percentage values as decimal ratios between 0 and 1.

6. Run live validation and report:
   
   - total output rows
   - distinct accountID count
   - duplicate accountID count
   - accounts with positive / zero / NULL FUM
   - min / average / max for both percentage fields
   - count of percentage values > 1
   - count of percentage values < 0
   - post-AsOfDate records entering feature logic
   - PASS / REVIEW / FAIL

Expected:

- final grain = one row per accountID
- duplicate accountID count = 0
- no post-AsOfDate records used
- valid percentage values should normally be between 0 and 1

Do not modify any other feature block.

After validation, show the final active Partial Rollover feature list and the exact SQL lines changed.
