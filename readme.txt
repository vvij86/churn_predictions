The revised design is approved.

Please now implement the agreed redesign in:

build_merceredge_base_historical_dataset.sql

Use the validated profiling findings and the updated structure from this conversation.

Important:

- Modify only the base historical dataset logic.
- Do NOT start feature engineering.
- Keep @AsOfDate manually supplied.
- Earliest in-scope historical source date = 2023-04-01.
- Feature window = 12 months.
- Outcome window = 3 months.
- Earliest valid full-history AsOfDate = 2024-03-31.
- Build one snapshot per execution.
- Keep the SQL compatible with repeated quarterly runs later.
- Do not hard-code all quarterly snapshots into this SQL.

Implement the agreed stages:

1. Parameter/date validation
2. Account universe
3. Historical eligibility as of @AsOfDate
4. Identity/reference resolution
5. Internal-transfer exclusion
6. Death exclusion
7. Future churn outcome block
8. Final one-row-per-account_id + as_of_date base dataset
9. Validation queries

Remove completely:

- accountSummary pseudo-historical snapshot logic
- ROW_NUMBER/ranking of accountSummary for snapshot selection
- reportingDate-as-as_of_date logic
- has_valid_accountsummary_snapshot
- accountsummary_snapshot_status
- current/latest mutable accountSummary/customerSummary fields that are not point-in-time safe

Use accountSummary only for defensible purposes such as:

- account universe
- account/member identifiers
- exitDate / exitType for outcome support
- death support
- limited genuinely static/reference attributes

Target logic must remain separate:

exitDate > @AsOfDate
AND exitDate <= @OutcomeEndDate

Then apply:
- internal-transfer exclusion
- death exclusion

Historical eligibility must ensure:

- account existed by @AsOfDate
- reliable commencement/join date, where available, is <= @AsOfDate
- exitDate is NULL or > @AsOfDate
- account was not deceased on or before @AsOfDate

Do not automatically exclude an account merely because customerMapping is unavailable.

Handle sentinel dates such as 3999-12-13 explicitly.

After updating the SQL:

1. Execute/read-only validate it for the first training snapshot:

FeatureStartDate = 2023-04-01
AsOfDate         = 2024-03-31
OutcomeStartDate = 2024-04-01
OutcomeEndDate   = 2024-06-30

2. Report:

- total account universe
- eligible accounts
- retained count
- churn count
- target NULL count
- internal-transfer exclusions
- death exclusions
- accounts exited on/before AsOfDate
- duplicate account_id + as_of_date count
- NULL account_id count
- NULL as_of_date count
- customer mapping coverage

3. Show a few sample rows for:
- retained
- churn
- internal transfer exclusion
- death exclusion
- already-exited-before-AsOfDate

Do not proceed to feature engineering after validation.
Stop and show me the results.
