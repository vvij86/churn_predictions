Read member_retention_ml_copilot_instructions.md and continue from the existing behavioural_features_business_review.sql.

Do not restart from scratch and do not regenerate unrelated sections.

Correction to current scope:

- edgeSource.campaignEventDetails is in scope
- edgeSource.campaignEvents is in scope
- only campaign and campaignAccountMapping are deferred
- edgeSource.accountNetMoneyFlow is also in scope and must be actively reviewed for useful behavioural features

Please review the current SQL and identify why these in-scope sources are missing or underused:

- edgeSource.accountNetMoneyFlow
- edgeSource.campaignEventDetails
- edgeSource.campaignEvents

1. accountNetMoneyFlow

Use edgeSource.accountNetMoneyFlow to identify useful standalone behavioural / financial-flow features.

From the source, relevant columns include fields such as:

- accountID
- amount
- cashflowDescription
- cashFlowSign
- internalTransferFlag
- referenceDate
- cashflowtype

Use the actual DDL/reference files to confirm all column names and meanings.

Do not assume sign or direction semantics unless supported by the business reference SQL.

Review MemberRetention_03-MemberRetentionMetrics_v005.sql and reuse the approved cash-flow / direction / type logic where applicable.

Generate standalone queries for useful features such as:

- net_flow_12m
- total_positive_flow_12m
- total_negative_flow_12m
- negative_net_flow_count_12m
- negative_net_flow_months_12m
- avg_monthly_net_flow_12m
- recent_net_flow_90d
- prior_net_flow_90d
- net_flow_decline_flag
- days_since_last_negative_flow
- cashflow_active_months_12m
- contribution-related cash-flow patterns only where supported by the business mapping

Also inspect whether useful additional patterns can be derived from:

- cashflowDescription
- cashflowtype
- cashFlowSign
- internalTransferFlag

Do not create redundant features if the same business behaviour is already better represented by accountMoneyInflow or accountRolloverPayment.

Where two sources overlap, document which source is preferred and why.

Each accountNetMoneyFlow feature query must:

- declare its own @AsOfDate
- declare its own @FeatureStartDate
- declare recent/prior 90-day parameters if required
- apply the approved FundScope through accountSummary.databaseCode
- use fundJoinDate <= @AsOfDate
- use exitDateRecorded, not exitDate
- exclude already exited accounts as of AsOfDate
- apply death exclusion
- exclude internal transfers where appropriate
- use only referenceDate <= @AsOfDate
- remain independently runnable

Use point-in-time logic such as:

referenceDate >= @FeatureStartDate
AND referenceDate <= @AsOfDate

Do not use future rows.

Before each query add:

/*
Feature Name:
Feature Group:
Business Meaning:
Source Table(s):
Source Column(s):
Reference Mapping Used:
Included Types:
Excluded Types:
Feature Window:
Point-in-Time Rule:
Leakage Risk:
Recommendation:
Business Confirmation Needed:
*/

2. campaignEventDetails and campaignEvents

Review:

- edgeSource.campaignEventDetails
- edgeSource.campaignEvents

These are in scope.

Identify standalone behavioural features that can safely be created using only pre-AsOfDate campaign/event activity.

Possible patterns to assess include:

- total campaign event count
- distinct campaign event type count
- days since last campaign event
- recent campaign event count
- engagement/contact/update-type activity
- event-type-specific counts where supported by source/reference logic

Important:

- MEMBER_EXIT must never be used as a predictive feature
- exclude outcome-like events
- exclude post-AsOfDate events
- do not infer email sent/open/click behaviour unless the actual source fields support it
- do not use campaign or campaignAccountMapping
- if campaign event meaning is unclear, mark REVIEW REQUIRED

3. Avoid duplicate/noisy features

For all three sources, compare proposed features against existing standalone queries.

Do not create duplicates just because another table contains similar information.

Where overlapping sources exist, add a note such as:

- Preferred source
- Supporting source only
- Duplicate feature - exclude

4. Update the existing file

Add the new standalone queries directly to:

behavioural_features_business_review.sql

Do not create a new consolidated modelling dataset.

Do not start model training.

Do not change unrelated feature logic.

5. Update the final source-usage summary

At the end, update the source table summary and confirm whether these are now used:

- edgeSource.accountNetMoneyFlow
- edgeSource.campaignEventDetails
- edgeSource.campaignEvents

Also explicitly confirm that these remain deferred/not used:

- campaign
- campaignAccountMapping

6. Final validation

Before finishing, verify:

- all accountNetMoneyFlow queries are independently runnable
- all campaign/event queries are independently runnable
- FundScope is physically present in executable SQL through accountSummary.databaseCode
- exitDateRecorded is used instead of exitDate
- no future events are used
- MEMBER_EXIT is not a predictive feature
- internal transfers are excluded where relevant
- no unsupported source tables were introduced
- no duplicate/noisy features were added unnecessarily

Stop after updating and validating behavioural_features_business_review.sql.
