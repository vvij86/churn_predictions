Based on Query 1 and Query 2, shortlist only these tables:

1. ACCOUNT_FUND_BALANCE
2. ACCOUNT_GENERAL_BALANCE
3. ACCOUNT_STATEMENT

Exclude:
- ACCOUNT_CASH_BALANCE because it contains cash components only and must
  not be assumed to represent total FUM.
- ACCOUNT_FUND_PIE_BALANCE because it has no direct ACCOUNT_ID and appears
  to contain tax, fee and income component information.

Please generate simple read-only SQL profiling queries, without dynamic SQL,
for the three shortlisted tables.

Use:
- as_of_date = 2024-12-31
- outcome_end_date = 2025-03-31

For ACCOUNT_FUND_BALANCE, profile:
1. Minimum and maximum UPDATE_DATETIME.
2. Row count and distinct ACCOUNT_ID count.
3. Distinct BALANCE_TYPE and BALANCE_TYPE_CODE values with counts.
4. Number of rows per ACCOUNT_ID.
5. Number of FUND_ID values per ACCOUNT_ID.
6. Null, zero, positive and negative counts for DOLLAR_BALANCE.
7. Coverage near 2024-12-31 and 2025-03-31.
8. Whether summing DOLLAR_BALANCE by ACCOUNT_ID appears possible.
9. Do not assume UPDATE_DATETIME is a historical snapshot date until confirmed.

For ACCOUNT_GENERAL_BALANCE, profile:
1. Minimum and maximum BALANCE_DATE.
2. Row count and distinct ACCOUNT_ID count.
3. Distinct BALANCE_TYPE_CODE and DATE_TYPE_CODE values with counts.
4. Number of rows per ACCOUNT_ID and BALANCE_DATE.
5. Null, zero, positive and negative counts for AMOUNT.
6. Coverage on 2024-12-31 and 2025-03-31.
7. Identify which BALANCE_TYPE_CODE values may represent total account
   balance, but do not assume the meaning without confirmation.

For ACCOUNT_STATEMENT, profile:
1. Minimum and maximum START_DATE and END_DATE.
2. Row count and distinct ACCOUNT_ID count.
3. Distinct TYPE_CODE and TYPE_SHORT_DESC values with counts.
4. Null, zero, positive and negative counts for CLOSING_BALANCE.
5. Statements whose END_DATE is 2024-12-31 or 2025-03-31.
6. Latest statement available on or before each required date.
7. Whether multiple statements exist per account and period.

Also provide one separate query for each table to check how many ACCOUNT_ID
values successfully join to dbo.ACCOUNT.

Do not generate the final FUM logic or churn target yet.
