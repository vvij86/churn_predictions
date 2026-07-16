The profiling results confirm:
ACCOUNT_GENERAL_BALANCE contains zero rows in DEV.
ACCOUNT_STATEMENT does not provide usable historical coverage for the selected dates.
ACCOUNT_FUND_BALANCE contains data, but UPDATE_DATETIME is not a reliable historical snapshot date.
Therefore, historical FUM, balance or valuation cannot currently be safely included in Version 1.
Please revise the Version 1 SonataODS training-dataset specification using the following rules:
Remove ACCOUNT_GENERAL_BALANCE and ACCOUNT_STATEMENT.
Exclude all FUM, balance and valuation features from Version 1.
Do not use ACCOUNT_FUND_BALANCE.DOLLAR_BALANCE as a historical ML feature.
Keep ACCOUNT_FUND_BALANCE only as a future investigation item.
Use only:
ACCOUNT
ACCOUNT_TRANSACTION
CONTRIBUTION_TRANSACTION
ROLLOVER
EXIT_TYPE
Maintain one row per account_id per as_of_date.
Use a 12-month historical feature window ending on as_of_date.
Use 2024-12-31 as the first as_of_date.
Use 2025-01-01 to 2025-03-31 as the outcome window.
All ML features must use data available on or before 2024-12-31.
Death-related exits must be excluded from the training population.
Do not distinguish partial and full rollover because PARTIAL_FULL_FLAG is unpopulated.
Historical rollover count and rollover amount may be included only as general behavioural features using records on or before as_of_date.
Use ROLLOVER.DATE_RECEIVED as the provisional rollover event date for Version 1 because EVENT_DATE is unreliable.
Exit date, external rollover during the outcome window, account closure status, exit type and exit reason must remain target-supporting fields only and must not be ML features.
Clearly flag any proposed column whose business meaning or calculation is still unconfirmed.
Do not generate the final SQL yet.
Please provide:
The revised final Version 1 column list.
Source table and source column or calculation for each proposed column.
Classification of every column as:
identifier
ML feature
target-supporting
exclusion
target
Historical window required for every ML feature.
Leakage risk for every proposed column.
Only the remaining business rules required before target_churn can be generated.
