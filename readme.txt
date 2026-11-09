Review only the Campaign / Event Behaviour section in "behavioural_features_business_review.sql".

Do NOT change the SQL yet.

Use the existing database connection pattern already available in "sample.py" and run live validation against the source tables:

- "edgeSource.campaignEventDetails"
- "edgeSource.campaignEvents"

Keep the review strictly account-level and respect the current feature window:

- one row per accountID
- use only source records on or before "@AsOfDate"
- use the existing 12-month / 90-day windows
- do not introduce post-AsOfDate leakage

Business has provided comments on this Campaign / Event section. Validate every comment below using live source data.

1. Generic campaign activity features

Review:

- "campaign_event_count_12m"
- "distinct_campaign_event_type_count_12m"
- "days_since_last_campaign_event"
- "recent_campaign_event_count_90d"

Business comment:
“These don’t really tell us anything important.”

Check:

- number of accounts with each feature > 0
- distribution of values
- exact eventName/eventID values contributing to them
- whether these are only generic activity-volume metrics
- whether they add any meaningful information beyond the more specific event categories below

Give each feature one recommendation:

- KEEP
- REVIEW
- CANDIDATE FOR REMOVAL

Do not remove anything yet.

2. Advice-event features

Review:

- "advice_event_count_12m"
- "recent_advice_event_count_90d"
- "days_since_last_advice_event"

Business comment:
“Potential duplication with Helpline, depends on logic used.”

Compare the Campaign/Event ADVICE classification with the already-reviewed Helpline ADVICE logic.

Show:

- exact Campaign eventName/eventID values classified as ADVICE
- number of accounts captured
- overlap account count with Helpline ADVICE
- Campaign-only account count
- Helpline-only account count
- examples of overlapping and non-overlapping records

Determine whether Campaign ADVICE provides an independent behavioural signal or mainly duplicates Helpline activity.

Do not automatically remove it just because overlap exists.

3. Website login features

Review:

- "website_login_count_12m"
- "website_login_count_90d"
- "website_login_count_30d"
- "days_since_last_website_login"

Show:

- exact eventName/eventID used for WEBSITE_LOGIN
- account coverage
- recency coverage
- example raw records
- whether this represents genuine digital engagement

Also clearly distinguish these Campaign/Event website-login features from "edge.accountEngagementWeb". Do not assume they are the same source.

4. Member Service features

Review:

- "member_service_event_count_12m"
- "recent_member_service_event_count_90d"

Business comment:
“I’m unclear on what Member Service entails.”

Show the exact:

- eventID
- eventName
- frequency
- distinct account count
- sample raw records

Explain in simple business language what events are currently being grouped into "MEMBER_SERVICE".

If the category contains multiple unrelated activities, flag that clearly.

Recommendation:
KEEP / REVIEW / CANDIDATE FOR REMOVAL.

5. Contribution-event features

Review:

- "contribution_event_count_12m"
- "recent_contribution_event_count_90d"

Business comment:
“Likely duplication with Contributions Table, depends on logic used.”

Show the exact Campaign event values classified as CONTRIBUTION.

Compare these Campaign/Event features with the existing contribution features derived from "Edge.accountMoneyInflow".

Report:

- Campaign contribution account count
- MoneyInflow contribution account count
- accounts present in both
- Campaign-only accounts
- MoneyInflow-only accounts

Explain whether the Campaign/Event feature represents:

A. actual contribution transaction activity already available in MoneyInflow,

or

B. a separate member behavioural interaction related to contributions.

Do not remove it without evidence.

6. Roll-in features

Review:

- "rollin_event_count_12m"
- "recent_rollin_event_count_90d"

Business comment:
“Likely duplication with Contributions Table, depends on logic used.”

Show:

- eventID/eventName used for ROLLIN
- account coverage
- example records
- overlap with MoneyInflow contribution/roll-in activity where possible

Determine whether this is an independent behavioural interaction or duplicate financial transaction information.

7. Retirement / Pension event features

Review:

- "retirement_pension_event_count_12m"
- "recent_retirement_pension_event_count_90d"

Business comment:
“What are you trying to measure here? Pension (EventID = 13) refers to Pension Creation.”

Specifically validate:

- whether EventID 13 maps to Pension Creation
- all eventID/eventName values currently classified under "RETIREMENT_PENSION"
- account coverage
- sample raw records

Explain exactly what the current feature measures.

Do not describe it generically as “retirement intent” if the source actually represents Pension Creation.

Check whether this overlaps with:

- Helpline "RETIREMENT_INQUIRY"
- Helpline "SUPER_TO_PENSION_TTR"

Report overlap separately.

8. Insurance opt-in

Review:

- "insurance_opt_in_12m_flag"

Show:

- exact eventName/eventID
- coverage
- sample records
- whether it clearly represents an insurance opt-in action

9. Beneficiary events

Review:

- "beneficiary_event_count_12m"

Show:

- exact beneficiary event values
- account coverage
- examples
- whether it represents a meaningful behavioural action rather than a generic event count

10. Duplication and semantic overlap summary

Create a final comparison showing possible overlap between Campaign/Event features and other already-existing feature families:

- Campaign ADVICE vs Helpline ADVICE
- Campaign CONTRIBUTION vs MoneyInflow contribution features
- Campaign ROLLIN vs MoneyInflow / contribution activity
- Campaign RETIREMENT_PENSION vs Helpline retirement / Super-to-Pension/TTR
- Campaign WEBSITE_LOGIN vs any other digital-engagement features

For each one classify:

- NO MATERIAL OVERLAP
- PARTIAL OVERLAP – BOTH MAY BE USEFUL
- HIGH DUPLICATION RISK
- NEEDS BUSINESS CONFIRMATION

11. Data-quality validation

Also validate:

- duplicate accountID rows in the final Campaign aggregation = 0
- no source record after "@AsOfDate"
- all 90-day features are within the intended 90-day window
- all 12-month features are within the intended 12-month window
- NULL handling remains unchanged

Required final output

Do not modify SQL.

Return a table with:

"Feature | Business Comment | Live Coverage | Exact Source Values | Overlap Finding | Recommendation | Reason"

Then provide a short section:

Changes recommended before modifying SQL

Split it into:

- SAFE TO CHANGE
- NEEDS BUSINESS CONFIRMATION
- KEEP AS-IS

Do not infer event meaning from the feature name alone. Base all conclusions on the actual "eventID", "eventName", source values and live database results.
