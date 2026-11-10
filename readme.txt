Update ONLY the Partial Rollover percentage logic in "behavioural_features_business_review.sql".

The latest live validation still shows a small number of percentage values > 1:

- partial_rollover_pct_12m > 1: 23 accounts
- recent_partial_rollover_pct_90d > 1: 5 accounts

This occurs because some accounts have zero or negative current FUM.

Please make the percentage denominator valid only when "current_account_fum_amount > 0".

Use:

partial_rollover_pct_12m =
partial_rollover_amount_12m /
(current_account_fum_amount + partial_rollover_amount_12m)

recent_partial_rollover_pct_90d =
recent_partial_rollover_amount_90d /
(current_account_fum_amount + recent_partial_rollover_amount_90d)

BUT return NULL when:

- current_account_fum_amount IS NULL
- current_account_fum_amount <= 0
- partial rollover amount is NULL
- resulting denominator <= 0

Do not cap percentages artificially at 1.

Do not multiply by 100.

Keep all existing Partial Rollover features unchanged.

After the change, run live validation and report only:

1. total output rows
2. distinct accountID count
3. duplicate accountID count
4. positive / zero / negative / NULL FUM counts
5. min / avg / max of partial_rollover_pct_12m
6. min / avg / max of recent_partial_rollover_pct_90d
7. count of each percentage > 1
8. count of each percentage < 0
9. post-AsOfDate rows entering the feature logic
10. PASS / REVIEW / FAIL

Expected:

- duplicate accountID = 0
- no future records used
- percentage < 0 = 0
- percentage > 1 = 0 for valid positive-FUM accounts

Do not modify any other feature section.
