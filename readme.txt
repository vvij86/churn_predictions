Create a SQL Server validation query for the Member Retention Analytics churn target.

Do NOT change any existing PySpark code or target logic.

Use these as the sources of truth:

1. ".github/copilot-instructions.md"
2. the reviewed churn/business-rule SQL already in the repository
3. "ml_mscs_mrt_target_labels.py"

Objective:

Create one SQL Server query that reproduces the exact "target_churn = 1" logic for a controlled snapshot so we can independently validate the Databricks ground-truth count.

Use this validation snapshot:

"AsOfDate = 2024-03-31"

Target outcome window:

"2024-04-01" through "2024-06-29"

The SQL must exactly match the approved business definition, including:

- eligible modelling population for the snapshot
- approved databaseCode scope
- "fundJoinDate <= AsOfDate"
- death/deceased exclusions
- AccountSummary churn-event logic
- AccountRolloverPayment full-rollover-out logic
- internal-transfer exclusion
- 90-day outcome-window logic
- any event-level precedence/deduplication used by "ml_mscs_mrt_target_labels.py"
- earliest qualifying churn event where applicable
- final output at one row per "accountID"

Do NOT simplify the rule to:

"exitType = 'Exit'"

unless that is explicitly the approved business definition.

Do NOT invent column names or event rules.

Use the exact SQL Server source table/column mappings already present in the reviewed SQL/reference files.

The final query should return:

1. "target_churn_1_count"
2. optionally the list of qualifying "accountID"
3. qualifying churn event date
4. churn source/reason if derivable from the approved logic

Also create a second small reconciliation query that compares the expected SQL Server count conceptually against the Databricks ground-truth count for:

"as_of_date = 2024-03-31"

Current Databricks result is:

"target_churn = 1 = 8,751"

Important:

Do not force the SQL Server query to return 8,751.

If the exact approved business rule returns a different count, report the difference clearly.

After creating the SQL, explain:

- exact churn definition implemented
- which source tables are used
- which exclusions are applied
- why this SQL is equivalent to the Databricks target logic
- any mismatch between reviewed business logic and current PySpark target code, if found
