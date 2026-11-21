Create the next stage of the Member Retention ML pipeline: ground-truth / target-label generation.

Follow ".github/copilot-instructions.md" strictly.

Do NOT modify the already validated behavioural feature business logic.

Current validated consolidated feature pipeline:

"notebook/ml_mscs_mrt_consolidated_features.py"

Current grain:

"one row per account_id per as_of_date"

Current controlled development snapshot:

"as_of_date = "2024-03-31""

Create a separate target-generation module, for example:

"notebook/ml_mscs_mrt_target_labels.py"

Generate:

"target_churn"

at:

"account_id + as_of_date"

grain.

Use the reviewed churn business rules from the existing standalone SQL/reference logic.

Target should represent whether the account churns AFTER "as_of_date" and within the configured outcome window.

Approved churn concepts include:

- Full Withdrawal
- Account Closure due to full exit
- Full Rollover Out

Exclude:

- Internal Transfer
- partial rollover / partial withdrawal
- churn events on or before "as_of_date"
- deceased members according to existing reviewed eligibility rules

Do NOT use target/outcome-period fields as predictive features.

Keep feature time and target time clearly separated.

Use the centrally controlled snapshot/config logic from:

"ml_mscs_mrt_config.py"

Design for future multiple snapshots.

For each snapshot:

"outcome_end_date = as_of_date + configured outcome horizon"

Join target output back to the validated consolidated feature dataset using ONLY:

- account_id
- as_of_date

Create:

"ground_truth_df"

Final grain must remain:

"one row per account_id per as_of_date"

Add hard-fail validation for:

- final row count equals consolidated feature row count
- distinct account_id + as_of_date equals row count
- duplicate count = 0
- null account_id = 0
- null as_of_date = 0
- null target_churn = 0 for eligible rows
- target_churn only contains 0 or 1
- churn count
- retained count
- churn percentage
- no event <= as_of_date used as positive target
- no event after outcome_end_date used as positive target
- internal transfer leakage = 0
- deceased eligibility logic preserved

Print:

"GROUND TRUTH DATASET VALIDATION SUMMARY"

with snapshot date, outcome start/end date, total rows, churn rows, retained rows, churn percentage, duplicates, null/invalid target counts, leakage counts and final PASS/FAIL.

Persistence

Persist only the final validated ground-truth/modelling dataset.

Use this Unity Catalog location:

Catalog:
"mer_wealth_dev"

Schema:
"mer_wealth_mra_mlops"

Suggested Delta table:

"mer_wealth_dev.mer_wealth_mra_mlops.member_retention_ground_truth"

Also make the table name centrally configurable rather than hard-coding it throughout the code.

The table must support multiple historical "as_of_date" snapshots.

Do NOT blindly append.

Use an idempotent approach such as MERGE or controlled replace-by-snapshot so rerunning the same "as_of_date" does not create duplicate "account_id + as_of_date" rows.

Do not overwrite other historical snapshots.

Persistence must be configurable ON/OFF.

Default development behaviour should preferably allow validation without persistence.

Persist only after all critical validations PASS.

Do NOT persist intermediate feature DataFrames.

Performance

Reuse the already generated consolidated feature DataFrame where available.

Do NOT unnecessarily rebuild the behavioural feature pipeline.

Avoid repeated Spark actions.

Reuse computed metrics where possible.

Do not introduce parallel execution yet.

After implementation report:

1. files created/changed
2. exact target rule implemented
3. configured outcome horizon
4. validation checks
5. persistence default ON/OFF
6. exact Delta table name
7. rerun/idempotency approach
8. confirmation behavioural feature logic was unchanged
