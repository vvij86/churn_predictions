Review these two production sample Excel files:

- AccountEngagementWeb_RandomSample_2026-10-29_NoSuperFacts.xlsx
- AccountEngagementWeb_RandomSample_2026-10-29_WithSuperFacts.xlsx

Excel password: "M4rsh_AiD4t4#"

Also use the existing "accountEngagementWeb" standalone feature query in "behavioural_features_business_review.sql" as the base.

Focus only on:

- jobSource
- jobTypeDescription
- requestDate
- requestParameters

Analyse MEMBERONLINE and SUPERFACTS separately and identify only meaningful member-driven web behaviour.

Then update/recreate only the standalone "accountEngagementWeb" feature query.

Requirements:

- Preserve the existing eligible account logic and fund/database scope.
- Preserve the 12-month feature window.
- Preserve useful 90-day recent behaviour and recency features.
- Use "requestDate" for point-in-time filtering and do not use any post-AsOfDate data.
- Exclude clearly backend/system-generated activity where identified from the samples.
- Include SUPERFACTS only where the sample data indicates meaningful member-driven behaviour.
- Use "jobTypeDescription" and, only where useful, "requestParameters" to create meaningful grouped web behaviour features.
- Avoid creating too many weak or highly specific features.
- Keep one row per "accountID".
- Do not modify any other standalone feature query.
- Do not create training, target, scoring or model logic.

Output only the final updated standalone SQL query for "accountEngagementWeb", ready to replace the existing web feature block in "behavioural_features_business_review.sql".
