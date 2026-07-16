The profiling results show:

1. ROLLOVER.PARTIAL_FULL_FLAG is NULL for every row.
2. No EXIT_TYPE values explicitly contain FULL or PARTIAL.
3. EXIT_TYPE distinguishes external rollover from internal rollover.
4. EXIT_TYPE.IS_INTERNAL_FLAG = 'Y' can identify internal transfers.
5. EXIT_TYPE.IS_DEATH_FLAG = 'Y' identifies death-related exits.
6. 1,532,061 rollover rows covering 1,091,893 accounts have
   EXIT_TYPE_ID = NULL.
7. Query 8 returned no rows, so all populated EXIT_TYPE_ID values have
   valid EXIT_TYPE mappings.
8. No EXIT_TYPE values matched closure or withdrawal keywords.

Therefore, do not treat every external rollover as churn because it may
include partial rollovers.

Please generate read-only SQL profiling queries to investigate how a
complete account exit can be identified using SonataODS account and
balance/FUM fields.

The queries should investigate:

1. Distinct ACCOUNT.STATUS_CODE values and counts.
2. Status-code descriptions from the relevant status reference table.
3. Counts and date ranges for ACCOUNT.EXIT_DATE.
4. Relationship between ACCOUNT.EXIT_DATE and external rollover events.
5. Account status after an external rollover.
6. Whether an external rollover account has remaining FUM/balance at the
   end of the proposed outcome window.
7. Which balance or valuation table provides account-level FUM as of a
   given date.
8. Counts of accounts with:
   - external rollover and account closed
   - external rollover and account still active
   - external rollover and zero FUM
   - external rollover and positive FUM
9. Accounts with EXIT_TYPE_ID NULL, grouped by account status, exit date,
   transaction category and balance/FUM position.
10. Death-related accounts must be shown separately.

Use the proposed POC dates:
- feature window: 2025-01-01 to 2025-12-31
- as_of_date: 2025-12-31
- outcome window: 2026-01-01 to 2026-03-31

Do not create the final target label yet.
Do not generate Python code.
Clearly identify which results require BA/SME confirmation.
