The revised SonataODS-only specification is accepted as a draft.

Before generating the training dataset SQL, help me resolve the remaining
items one by one.

For the initial Version 1 POC, simplify the dataset as follows:

1. Keep one row per account_id.
2. Temporarily exclude all CLIENT-level features because the rule for
   selecting the correct client for an account is not yet confirmed.
3. Keep only account, account transaction, contribution transaction and
   rollover-related features.
4. Keep full rollover, full-exit closure, exit date, exit type, exit reason
   and post-exit account status as target-supporting only.
5. Keep partial rollover only when it occurred on or before as_of_date.
6. Do not use account_txn_gross_amt_sum_12m or
   account_txn_net_effect_sum_12m until transaction sign and
   BALANCE_EFFECT_INDICATOR meanings are confirmed.
7. Continue excluding all death-related exits.
8. Do not generate the final SQL yet.

Please provide:

A. The simplified and confirmed candidate feature list.
B. A list of SQL profiling queries I should run to determine:
   - minimum and maximum transaction dates
   - minimum and maximum contribution dates
   - minimum and maximum rollover dates
   - account counts by year
   - full rollover counts by year
   - partial rollover counts by year
   - death-related exit counts by year
   - retained and not-retained account counts by year
C. Based on those profiling results, explain how to select:
   - the 12-month feature window
   - the as_of_date
   - the 3-month outcome window

Generate only read-only profiling SELECT queries.
Do not generate the final training dataset query yet.
