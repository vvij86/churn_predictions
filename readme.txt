Update only:

notebook/ml_mscs_mrt_web_engagement_features.py

Follow `.github/copilot-instructions.md` strictly.

Reference business logic from:

AccountEngagementWeb_Reviewed_Features.sql

The coverage audit found one remaining SQL-parity gap in the Leaving Service web feature logic.

Current PySpark implementation handles the `LEAVING_SERVICE` representation, but the reviewed SQL also handles the `LeavingService` representation.

TASK

1. Read the exact Leaving Service logic in `AccountEngagementWeb_Reviewed_Features.sql`.
2. Compare it with the existing Leaving Service parser/filter logic in `ml_mscs_mrt_web_engagement_features.py`.
3. Make the smallest possible correction so all reviewed Leaving Service variants handled by the SQL are handled equivalently in PySpark.
4. Do NOT change any other web feature logic.
5. Do NOT introduce new features.
6. Preserve current source-unavailable/UAT NULL behaviour.
7. Preserve controlled:
   as_of_date = "2024-03-31"
8. Preserve point-in-time filtering and leakage protection.
9. Preserve one row per account_id per as_of_date.

The affected reviewed features are:

- leaving_service_quote_count_12m
- recent_leaving_service_quote_count_90d
- days_since_last_leaving_service_quote

After the fix, validate and report:

- exact parser/filter change made
- confirmation that both reviewed Leaving Service representations are now covered
- output row count
- duplicate account_id + as_of_date count
- distinct as_of_date count
- future leakage count
- whether UAT remains source-unavailable for the snapshot window
- confirmation that NULL semantics are preserved when source data is unavailable

Do not modify any unrelated files.
