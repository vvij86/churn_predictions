Review "AccountEngagementWeb_Standalone.sql".

Keep the existing generic web features:

- "web_activity_count_12m"
- "web_active_days_12m"
- "days_since_last_web_activity"
- "recent_web_activity_count_90d"

Using only the "jobTypeDescription" values already selected in this SQL from the production Excel samples, add only a small number of strong grouped behavioural features.

Suggested groups:

- retirement/planning activity
- profile/detail update activity
- investment activity
- beneficiary/TFN/communication update activity, only if meaningful

Requirements:

- Do not create one feature per "jobTypeDescription".
- Do not introduce any new job types that are not already present in this SQL.
- Keep the existing eligible-account logic, 12-month window, 90-day logic and point-in-time rules unchanged.
- Keep one row per "accountID".
- Do not add training, target or scoring logic.
- Avoid weak or redundant features.

Update only "AccountEngagementWeb_Standalone.sql" and return the final revised standalone query.
