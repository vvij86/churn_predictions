Update only:

"notebook/ml_mscs_mrt_consolidated_features.py"

Follow ".github/copilot-instructions.md" strictly.

Do NOT change:

- feature business logic
- joins
- source mappings
- feature calculations
- snapshot logic
- validation rules
- execution order
- persistence behaviour

The purpose of this change is ONLY to add a concise final validation summary at the very end of the consolidated pipeline so important results are easy to see even when Databricks truncates earlier logs.

Add one clearly labelled final summary block, for example:

"FINAL CONSOLIDATED VALIDATION SUMMARY"

Reuse validation metrics that have already been computed wherever possible.

Do NOT trigger unnecessary additional Spark actions just to print the summary.

The final summary should show:

- controlled as_of_date
- base population row count
- final consolidated row count
- distinct account_id + as_of_date count
- duplicate account_id + as_of_date count
- null account_id count
- null as_of_date count
- distinct as_of_date count
- future leakage result/count
- total final column count
- total feature column count
- web engagement source availability status
- web feature NULL/unavailable status
- total consolidated runtime in seconds
- total consolidated runtime in minutes

Also print a simple overall status:

"VALIDATION STATUS: PASS"

only when all critical validations have passed.

Otherwise print:

"VALIDATION STATUS: FAIL"

and clearly identify the failed checks.

Keep the summary concise and grouped together at the END of execution.

Do not display large DataFrames or full schemas in this summary.

Do not add new expensive count/distinct/groupBy actions if those metrics are already available from existing validation logic.

After making the change, tell me:

1. what was added
2. whether any additional Spark actions were introduced
3. whether a full rerun is required to populate the summary
