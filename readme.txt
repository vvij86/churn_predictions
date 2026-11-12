Generate a standalone SQL Server query for AccountEngagementWeb behavioural features based on the production XLSX analysis already completed.

IMPORTANT:
- Do NOT modify behavioural_features_business_review.sql yet.
- Create a new standalone query/file, for example:
  AccountEngagementWeb_Reviewed_Features.sql
- Grain must be ONE ROW PER accountID PER @AsOfDate.
- Use only information available on or before @AsOfDate.
- Feature window = previous 12 months.
- Recent window = previous 90 days.
- Avoid target leakage.
- Do NOT use ExitDate from requestParameters.
- Do NOT use any future-dated exit/outcome field.
- Do NOT include generic WebQuoteSummary activity counts.
- Do NOT include profile/address/contact update features.
- Do NOT include static CurrentBalance, RetirementBenefit, contribution amount, investment strategy, or similar values already captured in other feature groups.

Source:
edgeSource.accountEngagementWeb

Use the same eligible-account logic and parameter style already used in behavioural_features_business_review.sql:
- @AsOfDate
- @FeatureStartDate
- @Recent90Start
- eligible_accounts

Production XLSX analysis established the following decisions.

==================================================
1. RETIREMENT PLANNING — KEEP
==================================================

Use jobTypeDescription values:
- MemberRISProjection
- BalanceRetirementProjection

Create:

retirement_planning_activity_count_12m

recent_retirement_planning_activity_count_90d

days_since_last_retirement_planning_activity

Definition:
- count actual qualifying web requests
- recent count only within previous 90 days
- recency = DATEDIFF(DAY, MAX(requestDate), @AsOfDate)

Do NOT use ExitDate from requestParameters.

Do NOT directly use:
- RetirementAge
- DesiredRetirementIncome
- CurrentBalance
- ProjectedBalanceAtRetirement
- RetirementBenefit
as model features in this first version.

The behavioural signal is that the member performed retirement-planning activity, not the resulting monetary values.

==================================================
2. LEAVING SERVICE / WITHDRAWAL QUOTE — REVIEW FEATURE
==================================================

WebQuoteSummary itself is too broad.

Only classify a WebQuoteSummary request as leaving-service intent when requestParameters contains a valid LeavingService value.

Create:

leaving_service_quote_count_12m

recent_leaving_service_quote_count_90d

days_since_last_leaving_service_quote

Do NOT use ExitDate.

Do NOT create a generic WebQuoteSummary count.

Do NOT use LeavingService monetary amount itself in the first version.

The feature should represent:
"member actively modelled a leaving-service / withdrawal scenario"

rather than generic quote activity.

Please inspect the real requestParameters format from the production XLSX examples and implement robust SQL parsing.

If requestParameters is pipe-delimited key=value text, extract/check LeavingService safely using SQL Server string logic.

Do not simply search for the word "LeavingService" if it can occur without a usable value.
Where possible, require a non-empty/non-null value.

==================================================
3. TRANSFER INTENT — REVIEW
==================================================

Use specific intentional event:
- Transfer Request WEB

Create:

transfer_intent_activity_count_12m

recent_transfer_intent_activity_count_90d

days_since_last_transfer_intent_activity

Do not combine this with generic web activity.

==================================================
4. INVESTMENT SWITCH INTENT — REVIEW
==================================================

Use:
- Web - Asset Switch

Create:

investment_switch_activity_count_12m

recent_investment_switch_activity_count_90d

days_since_last_investment_switch_activity

This represents an explicit online investment-change action.

==================================================
5. DO NOT INCLUDE
==================================================

Do not generate active ML features for:

- WebQuoteSummary generic count
- generic web_activity_count_12m
- web_active_days_12m
- days_since_last_web_activity
- recent_web_activity_count_90d
- profile/address/contact updates
- Update Basic Details
- UpdateAccessCode
- UpdateAllDetails
- UpdateBeneficiaries
- UpdateTFN
- UpdateTFNConsent
- UpdateCommunicationPreferences
- Web - Update Email Address

Do not use:
- ExitDate
- any future exit/outcome fields
- CurrentBalance
- RetirementBenefit
- static contribution amounts
- static investment strategy/profile values

Do not automatically include RiskAttitudeTool / RiskAttitudeToolUpdate yet.
Leave these as REVIEW only because production coverage is low.

Also leave the following very-low-volume events outside the active feature set for now:
- Web Request - Cancel Insurance
- Manual Super to Pension Application
- Pension Commutation

==================================================
6. DATA QUALITY / FILTERS
==================================================

Use:

requestDate >= @FeatureStartDate
AND requestDate <= @AsOfDate

Recent 90-day features use:
requestDate >= @Recent90Start
AND requestDate <= @AsOfDate

Use only eligible accounts.

Preserve NULL handling appropriately.

Do not allow future requestDate records.

Account-level aggregation must return at most one row per accountID.

==================================================
7. QUERY STRUCTURE
==================================================

Prefer clear CTEs such as:

eligible_accounts
web_base
classified_web_activity
web_behaviour_features

In classified_web_activity create explicit flags such as:

retirement_planning_flag
leaving_service_quote_flag
transfer_intent_flag
investment_switch_flag

Then aggregate these to account level.

Final SELECT should contain:

accountID

retirement_planning_activity_count_12m
recent_retirement_planning_activity_count_90d
days_since_last_retirement_planning_activity

leaving_service_quote_count_12m
recent_leaving_service_quote_count_90d
days_since_last_leaving_service_quote

transfer_intent_activity_count_12m
recent_transfer_intent_activity_count_90d
days_since_last_transfer_intent_activity

investment_switch_activity_count_12m
recent_investment_switch_activity_count_90d
days_since_last_investment_switch_activity

==================================================
8. VALIDATION OUTPUT
==================================================

After the main query, add validation queries for:

1. total rows
2. distinct accountID
3. duplicate accountID count
4. records with requestDate > @AsOfDate entering feature logic
5. records before @FeatureStartDate entering feature logic
6. coverage for every generated feature
7. number of accounts with each feature > 0
8. min / avg / max for each count feature
9. NULL coverage for each days-since feature
10. source event counts by jobTypeDescription
11. LeavingService parsing success count
12. WebQuoteSummary rows where LeavingService is absent vs present

Also provide 20 sample qualifying source rows for:
- retirement planning
- leaving-service quote
- transfer intent
- investment switch

Include:
accountID,
requestDate,
jobSource,
jobType,
jobTypeDescription,
requestParameters

for manual business verification.

==================================================
9. IMPORTANT
==================================================

Do not modify any other feature block.

Do not invent mappings not observed in the production XLSX files.

Base the requestParameters parsing on the actual production examples already analysed.

At the end provide:

A. exact active feature list
B. mapping from each feature to source jobTypeDescription/requestParameters condition
C. any assumptions made
D. PASS / REVIEW / FAIL assessment
E. features intentionally excluded and reason
