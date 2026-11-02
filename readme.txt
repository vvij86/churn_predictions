Rework only the standalone "accountEngagementWeb" feature query.

Important: do not use generic keyword assumptions or reuse workflow-style filters.

First inspect both Excel files and derive the logic only from the actual values present in:

- "jobSource"
- "jobTypeDescription"
- "requestDate"
- "requestParameters"

Files:

- AccountEngagementWeb_RandomSample_2026-10-29_NoSuperFacts.xlsx
- AccountEngagementWeb_RandomSample_2026-10-29_WithSuperFacts.xlsx

Before writing SQL:

1. Extract the distinct "jobTypeDescription" values separately for MEMBERONLINE and SUPERFACTS.
2. Inspect "requestParameters" patterns for those values.
3. Decide which actual values appear member-driven, system-generated, or unclear based only on the Excel samples.

Then recreate only the standalone "accountEngagementWeb" SQL using those observed values/patterns.

Do not introduce generic filters such as "%member%", "%account%", "%contact%", "%login%", "%profile%", "%portfolio%" unless those patterns are clearly supported by the Excel sample data.

Preserve:

- existing eligible account logic
- 12-month window
- recent 90-day feature
- days-since-last activity
- one row per accountID
- no post-AsOfDate data

Output only the final standalone "accountEngagementWeb" SQL query.
