Do NOT change any SQL.

I have already added the following Partial Rollover / Withdrawal features:

- current_account_fum_amount
- partial_rollover_pct_12m
- recent_partial_rollover_pct_90d

The SQL uses edgeSource.accountInvestment and selects the latest investment record per accountID + investmentCode on or before @AsOfDate, then sums the investment values to derive account-level FUM.

Now give me ONLY a standalone SQL validation script that I can copy and run directly in SSMS against the current logic.

Validate:

1. Final partial rollover grain:
   - total rows
   - distinct accountID
   - duplicate accountID count
   Expected duplicate count = 0.

2. FUM point-in-time integrity:
   - count of AccountInvestment records used with investmentDate > @AsOfDate
   Expected = 0.

3. FUM coverage:
   - accounts with current_account_fum_amount > 0
   - accounts with current_account_fum_amount = 0
   - accounts with current_account_fum_amount IS NULL.

4. Validate the two new percentage fields:
   partial_rollover_pct_12m =
       partial_rollover_amount_12m / current_account_fum_amount

   recent_partial_rollover_pct_90d =
       recent_partial_rollover_amount_90d / current_account_fum_amount

5. For each percentage feature show:
   - non-null account count
   - minimum
   - average
   - median
   - maximum.

6. Count accounts where:
   - partial_rollover_pct_12m > 1
   - recent_partial_rollover_pct_90d > 1

Do NOT cap these values. They may be valid where cumulative rollover during the window is greater than the FUM remaining at @AsOfDate.

7. Show 10 real sample accounts with:
   accountID,
   current_account_fum_amount,
   partial_rollover_count_12m,
   partial_rollover_amount_12m,
   partial_rollover_pct_12m,
   recent_partial_rollover_count_90d,
   recent_partial_rollover_amount_90d,
   recent_partial_rollover_pct_90d.

8. Verify that the original five partial rollover features are still present:
   - partial_rollover_count_12m
   - partial_rollover_amount_12m
   - days_since_last_partial_rollover
   - recent_partial_rollover_count_90d
   - recent_partial_rollover_amount_90d

Do not modify behavioural_features_business_review.sql.
Return only the validation SQL and a short explanation of expected PASS conditions.
