The profiling is now complete and the findings are validated.

Please use the validated profiling results to redesign:

build_merceredge_base_historical_dataset.sql

Important rules:

1. Do not treat edgeSource.accountSummary as a historical snapshot table.
2. Do not use reportingDate as the model as_of_date.
3. @AsOfDate must remain a manually supplied modelling cutoff.
4. accountSummary should be used only for:
   - account universe / identifiers
   - target/outcome support using exitDate
   - death exclusion
   - internal-transfer support
   - safe static/reference fields only where justified
5. Do not use current/latest mutable fields such as current balance, FUM, latest status, current age band, current salary, etc. as historical point-in-time features.
6. Create target_churn separately using:
   exitDate > @AsOfDate
   AND exitDate <= @OutcomeEndDate
   with internal transfer and death exclusions.
7. Use the validated historical event/transaction tables only as historical source inputs.
8. Use partial effective-dated sources only where point-in-time state can be reconstructed safely.
9. Do not perform full feature engineering yet.
10. Keep the final grain:
    one row per account_id + as_of_date.
11. Add clear comments identifying:
    - current/static source
    - target source
    - historical event source
    - partial point-in-time source
12. Handle known sentinel/future dates such as 3999-12-13 explicitly.
13. Remove any logic that assumes accountSummary has multiple historical snapshots.
14. Do not use ROW_NUMBER over accountSummary for historical snapshot selection if accountID is already unique.

Before modifying the file, first show me the proposed revised SQL structure/steps only.

Do not write the SQL yet.
