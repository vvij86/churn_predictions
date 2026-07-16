I ran the initial SonataODS profiling queries.

The results are:

1. ROLLOVER.PARTIAL_FULL_FLAG values:
[paste results]

2. ACCOUNT_TRANSACTION date range:
[paste results]

3. CONTRIBUTION_TRANSACTION date range:
[paste results]

4. ROLLOVER date range:
[paste results]

Based only on these actual results:

1. Confirm the full and partial rollover flag mappings.
2. Identify which date field should be used for each feature.
3. Propose three possible as_of_date candidates.
4. For each candidate, show:
   - 12-month feature window
   - 3-month outcome window
5. Do not generate the final training dataset SQL yet.
6. Clearly flag any decision that still requires BA or SME confirmation.
