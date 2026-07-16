The profiling results confirm:

1. ACCOUNT_GENERAL_BALANCE contains zero rows in DEV.
2. ACCOUNT_STATEMENT does not provide usable coverage for the selected dates.
3. ACCOUNT_FUND_BALANCE has data, but UPDATE_DATETIME is not a reliable historical snapshot date.
4. Therefore, historical FUM or account balance cannot currently be safely included in Version 1.

Please revise the Version 1 SonataODS training-dataset specification as follows:

- Remove ACCOUNT_GENERAL_BALANCE and ACCOUNT_STATEMENT.
- Exclude all FUM, balance and valuation features from Version 1.
- Do not use ACCOUNT_FUND_BALANCE.DOLLAR_BALANCE as a historical feature.
- Keep ACCOUNT_FUND_BALANCE only as a future investigation item.
- Use only ACCOUNT, ACCOUNT_TRANSACTION, CONTRIBUTION_TRANSACTION, ROLLOVER and EXIT_TYPE.
- Retain one row per account_id per as_of_date.
- Use a 12-month feature window.
- Use 2024-12-31 as the first as_of_date and 2025-01-01 to 2025-03-31 as the outcome window.
- Death exits must be excluded.
- Do not distinguish partial and full rollover because PARTIAL_FULL_FLAG is unpopulated.
- Rollover count and amount may be included only as general historical behaviour features before as_of_date.
- Exit date, external rollover during outcome window, account closure status and exit type must remain target-supporting fields and not ML features.

Do not generate the final SQL yet.

Provide:
1. The revised final Version 1 column list.
2. Source table and calculation for each column.
3. Which fields are ML features versus target-supporting fields.
4. Remaining business rules required before target_churn can be generated.
