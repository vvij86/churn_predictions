The 2026-01-01 to 2026-03-31 rollover queries returned no data, but
2025-01-01 to 2025-03-31 returned usable results.

Therefore, revise the POC dates to:

- Feature window: 2024-01-01 to 2024-12-31
- as_of_date: 2024-12-31
- Outcome window: 2025-01-01 to 2025-03-31

The external rollover profiling found approximately:

- 102,371 accounts with EXIT_DATE on the same day as the first external rollover
- 2,675 accounts with no EXIT_DATE
- 605 accounts with EXIT_DATE after the external rollover
- 102,976 closed accounts with EXIT_DATE
- approximately 2,675 active accounts without EXIT_DATE

Do not create the final target yet.

The metadata search identified these possible balance/FUM tables:

- ACCOUNT_CASH_BALANCE
- ACCOUNT_FUND_BALANCE
- ACCOUNT_FUND_PIE_BALANCE
- ACCOUNT_GENERAL_BALANCE
- ACCOUNT_STATEMENT

Please generate read-only profiling queries to compare only these candidate tables.

For each table, show:

1. All column names and data types.
2. Whether ACCOUNT_ID exists directly or through a reliable join.
3. Minimum and maximum balance/snapshot dates.
4. Row count and distinct account count.
5. Whether multiple rows exist per account and date.
6. Which amount columns may represent total account FUM.
7. Coverage for 2024-12-31 and 2025-03-31.
8. Null, zero, positive and negative amount counts.
9. Do not assume cash balance alone equals total FUM.
10. Recommend which table is the strongest candidate, but clearly mark
    that the authoritative FUM source requires BA/SME or data-team confirmation.

Do not generate Python or final training-dataset SQL yet.
