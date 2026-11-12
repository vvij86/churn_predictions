Review the AccountEngagementWeb production sample data in these two Excel files:

1. AccountEngagementWeb_RandomSample_2026-10-29_WithSuperFacts.xlsx
2. AccountEngagementWeb_RandomSample_2026-10-29_NoSuperFacts.xlsx

Context:
- edgeSource.accountEngagementWeb is empty/unavailable in UAT.
- These Excel files contain production sample data and must be used for the business review.
- Current SQL in behavioural_features_business_review.sql mainly derives behavioural features from jobTypeDescription.
- WebQuoteSummary is very broad and should NOT automatically be treated as a useful churn feature.
- We now want to investigate whether requestParameters and other available columns provide more meaningful pre-churn behavioural signals.
- Modelling grain must remain one row per accountID per AsOfDate.
- Do NOT modify behavioural_features_business_review.sql yet.
- This step is analysis/recommendation only.

Important:
Do not infer usefulness from column names alone. Inspect actual production sample values.

Tasks:

1. Profile both Excel files
For each file show:
- row count
- distinct accountID count
- distinct jobSource
- distinct jobType
- distinct jobTypeDescription
- requestDate range
- null/non-null coverage for:
  - accountID
  - requestDate
  - requestID
  - jobSource
  - jobType
  - jobTypeDescription
  - requestParameters

2. Analyse jobTypeDescription
Show:
- each distinct jobTypeDescription
- row count
- distinct accounts
- percentage of total rows
- percentage of distinct accounts

Identify:
- broad/generic activity
- potentially meaningful churn/retention behaviour
- administrative activity
- investment activity
- retirement-planning activity
- transfer/rollover activity
- insurance activity
- profile/contact updates

Do not automatically recommend WebQuoteSummary just because it has high coverage.

3. Deeply analyse requestParameters

requestParameters contains key=value style information such as:
- LeavingService
- CurrentBalance
- RetirementBenefit
- RetirementAge
- DesiredRetirementIncome
- IsHomeOwner
- PreTaxContributionPAAmount
- TargetWebPage
- InvestmentStrategyName
- ExitDate
- Address / contact fields
and potentially other parameters.

Parse requestParameters into key/value pairs.

Create a profile containing:
- parameter name
- number of rows containing it
- distinct accounts containing it
- coverage %
- sample values
- associated jobTypeDescription(s)

Do not assume the above list is complete. Discover all parameter names present in the files.

4. Assess each requestParameter for churn usefulness

Classify each discovered parameter as one of:

KEEP CANDIDATE
REVIEW
DE-SCOPE
LEAKAGE / DO NOT USE

For each parameter explain:
- behavioural meaning
- whether it describes an action/intent or merely a static value
- coverage
- whether it is available before AsOfDate
- whether it may contain outcome/future information
- whether it duplicates another retained feature already available from MercerEdge tables

Pay special attention to:

ExitDate:
- Treat as potential target leakage.
- Do NOT recommend it as a predictive feature unless it can be proven to represent information already known before AsOfDate and is not the churn outcome.
- Default recommendation should be LEAKAGE / DO NOT USE.

LeavingService:
- Determine exactly what it represents from the observed values and the related WebQuoteSummary activity.
- Check whether it reflects a member explicitly modelling a potential exit/withdrawal amount.
- Assess whether this is a stronger churn-intent signal than merely counting WebQuoteSummary events.

CurrentBalance / RetirementBenefit:
- Determine whether these duplicate FUM/current balance features available elsewhere.
- Do not retain only because the values are large.

RetirementAge / DesiredRetirementIncome:
- Assess as retirement-planning intent rather than raw monetary magnitude.

PreTaxContributionPAAmount:
- Compare conceptually with contribution features already sourced from accountMoneyInflow.
- Flag likely duplication if appropriate.

InvestmentStrategyName:
- Compare against existing investment-position/investment-switch features.

TargetWebPage:
- Determine whether specific page destinations provide meaningful digital-intent behaviour.

Address/contact parameters:
- Treat as administrative/profile information unless evidence suggests otherwise.

5. Analyse combinations, not only individual parameters

Investigate whether combinations such as these provide stronger behavioural intent:

- WebQuoteSummary + LeavingService present
- MemberRISProjection + retirement planning parameters
- BalanceRetirementProjection + retirement-related parameters
- RiskAttitudeTool / RiskAttitudeToolUpdate
- Web - Asset Switch
- Transfer Request WEB
- Transfer Request - Member Consent Transfer
- Web Request - Cancel Insurance
- Pension Commutation
- Manual Super to Pension Application

For each combination show:
- row count
- distinct accounts
- available parameter fields
- likely business meaning
- churn relevance
- leakage concern
- recommendation

6. Check duplication against existing feature groups

Compare proposed web-derived signals against existing features from:
- Campaign/Event Behaviour
- Workflow Behaviour
- Contribution Behaviour / accountMoneyInflow
- Investment Behaviour
- Partial Rollover / Withdrawal
- Insurance Behaviour

Identify whether AccountEngagementWeb gives:
A. genuinely new behavioural intent,
B. another view of an existing behaviour, or
C. direct leakage/outcome information.

7. Recommend better web features

Instead of broad generic metrics only, consider evidence-based features such as:

- retirement_planning_activity_count_12m
- recent_retirement_planning_activity_count_90d
- days_since_last_retirement_planning_activity

- investment_activity_count_12m
- recent_investment_activity_count_90d

- transfer_intent_activity_count_12m
- recent_transfer_intent_activity_count_90d

- insurance_cancel_request_count_12m
- recent_insurance_cancel_request_count_90d

- leaving_service_quote_count_12m
- recent_leaving_service_quote_count_90d
- days_since_last_leaving_service_quote

Only recommend these when supported by actual sample data.

For requestParameter-derived numeric values, prefer behavioural-change or intent measures over absolute wealth values where possible.

8. Specifically reassess the existing generic fields:

- web_activity_count_12m
- web_active_days_12m
- days_since_last_web_activity
- recent_web_activity_count_90d

Determine whether these are useful after examining the actual jobTypeDescription mix.

If they are dominated by WebQuoteSummary or administrative activity, recommend REVIEW or DE-SCOPE rather than KEEP.

9. Produce a final decision table with columns:

Feature / Candidate Feature
Source
Underlying Job Type / Parameter
Production Coverage
Business Meaning
Overlap With Existing Features
Leakage Risk
Recommendation
Reason

Recommendation must be one of:
KEEP
REVIEW
DE-SCOPE
DO NOT USE - LEAKAGE

10. Final output

Provide:
A. What the production samples tell us
B. Which current AccountEngagementWeb features remain useful
C. Which current features should be removed
D. Which new requestParameters-based features should be considered
E. Which fields must never be used because of leakage
F. A proposed final AccountEngagementWeb active feature list

Do NOT modify SQL yet.
Do NOT create features just because a parameter exists.
The objective is to identify genuinely useful pre-churn digital behavioural intent from the production data.
