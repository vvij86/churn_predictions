Yes. Update the Copilot prompt so exitDateRecorded is the only churn/exit date field used, not exitDate.

Use this revised prompt:

> Please review and correct all queries in behavioural_features_business_review.sql.

Use the business-provided Member Retention reference SQL as the source of truth, especially the logic that derives flow categories/types from:

- accountMoneyInflow
- accountNetMoneyFlow
- accountRolloverPayment
- FlowFact
- FlowTypeMap
- MMRFlowColumns
- and any other relevant lookup/mapping logic in the supplied reference SQL.

The objective is to apply the correct business filters and mappings to every behavioural feature query, reduce noise, and keep all logic aligned with the latest approved churn definition.

Latest approved churn rule

Use accountSummary.exitDateRecorded instead of exitDate everywhere.

The latest business confirmation is:

- exitDateRecorded is the approved exit date used for churn logic.
- exitDate must not be used in the behavioural feature engineering queries, eligibility logic, churn-target logic, examples, validation checks or comments.
- Search the entire generated SQL and replace/remove any use of exitDate where the intended business field is exitDateRecorded.

Account eligibility / historical existence rule

Use:

fundJoinDate <= @AsOfDate
AND (exitDateRecorded IS NULL OR exitDateRecorded > @AsOfDate)

This means the account had commenced by the snapshot date and had not already exited before/on the AsOfDate.

Retain the approved death exclusion logic.

Churn target rule

exitDateRecorded can be used to create the churn target for the future outcome window:

exitDateRecorded > @AsOfDate
AND exitDateRecorded <= @OutcomeEndDate

subject to the approved internal-transfer and death exclusions.

exitDateRecorded is a target/eligibility field only and must not be used as a predictive model feature.

Do not create features such as:

days_until_exit
exit_date_flag
future_exit_date

because these would cause target leakage.

Important rules

1. Do not invent any mapping, join key, flow code, status code or filter.
2. Reuse the exact mapping/filter logic from the Member Retention reference SQL wherever possible.
3. If a required mapping cannot be confirmed from the reference SQL, mark it:

TODO - BUSINESS / REFERENCE CONFIRMATION REQUIRED

4. Keep all predictive feature logic point-in-time safe:

event_date >= @FeatureStartDate
AND event_date <= @AsOfDate

5. Never use post-AsOfDate events as predictive features.
6. Do not use exitDateRecorded, MEMBER_EXIT, future account closure, future full rollover completion or other future outcome information as predictive model inputs.
7. Internal transfers must not be treated as churn-related external rollover behaviour.

First create a reusable flow classification layer

Before calculating financial behavioural features, create a reusable mapped flow CTE/temp table using the exact logic from the Member Retention reference query.

It should derive a normalized field such as:

mapped_flow_type

using the same business rules as the reference query.

For example, only if supported exactly by the reference SQL:

- Employer / Employer Additional Conts → Employer SG
- Voluntary Member Salary Sacrifice → Salary Sacrifice
- Member Voluntary → Post Tax Voluntary
- Rollovers-In → Rollover In
- internal transfer → Internal Transfer In
- Adjustment → Adjustment
- claim/insurance-related Other Conts → Insurance Claim Proceeds

Do not simplify or broaden these mappings.

Contribution features

Contribution features must count only genuine contribution flow types.

Include only mapped contribution types such as:

- Employer SG
- Salary Sacrifice
- Post Tax Voluntary

if confirmed by the business reference SQL.

Do not count:

- Rollover In
- Internal Transfer In
- Insurance Claim Proceeds
- Adjustment
- unrelated inflows

Review and correct:

- contribution_count_12m
- contribution_amount_12m
- avg_contribution_amount_12m
- contribution_active_months_12m
- days_since_last_contribution
- recent_contribution_amount_90d
- prior_contribution_amount_90d
- contribution_decline_flag
- months_of_declining_contribution

Remove broad logic such as:

inflowDescription NOT IN (...)

where it could accidentally allow unrelated inflow types to be treated as contributions.

Rollover / withdrawal features

Use only rollover-specific mapped types.

Keep separate:

- rollover in
- partial rollover out
- external rollover out
- internal transfer

Internal transfers must be excluded from external rollover risk features.

Any full/external rollover feature that is very close to the churn outcome must be marked:

LEAKAGE REVIEW REQUIRED

Do not include rollover events after @AsOfDate.

Net money flow

Use the reference flow-direction/sign logic.

Do not assume positive amount = inflow and negative amount = outflow unless the reference query confirms it.

Review:

- total_inflow_12m
- total_outflow_12m
- net_flow_12m
- recent_net_flow_90d
- prior_net_flow_90d
- negative_net_flow_count_12m
- negative_net_flow_months_12m
- net_flow_decline_flag

Workflow features

Profile workflow types/statuses first.

Do not count every workflow record automatically.

Exclude or flag:

- system-generated workflows
- administrative workflows
- operational/noisy workflow types

Keep only meaningful member-behaviour workflows where supported by the reference/business logic.

Helpline features

Apply any relevant filters found in the reference SQL for:

- valid call/event rows
- useful inquiry types
- duplicate/system records

Review:

- contact count
- inquiry count
- active days
- recency
- recent contacts
- repeat contact indicator

Website features

Keep the feature definitions unchanged.

accountEngagementWeb is empty in UAT, so:

- do not remove the features
- do not convert them all to zero
- keep them NULL/unavailable in UAT
- mark them INCLUDE PENDING PROD VALIDATION

Investment features

Only include fields where the reference SQL confirms the business meaning.

Do not assume every investment row is an investment-change event.

Review:

- investment change count
- investment recency
- active investment months
- investment option count
- direct investment flag

Insurance-related flows

Do not treat insurance claim proceeds as ordinary contributions.

Keep insurance-related flows separate or mark them for review.

Noise-reduction checks

For every query, explicitly verify whether the following should be excluded:

- internal transfers
- adjustments
- insurance claims
- fees
- tax
- administrative/system events
- duplicate/reversal records
- target/outcome events
- post-AsOfDate events

Mandatory exitDateRecorded validation

Before completing the file, search the entire SQL for:

exitDate

Confirm that no old exitDate reference remains where the approved business field should be exitDateRecorded.

Output a validation result such as:

old_exitDate_reference_count = 0
exitDateRecorded_reference_count = <count>
churn_date_field_validation = PASS

Output required

For each feature query, add:

/*
Feature Name:
Business Meaning:
Source:
Reference Mapping Used:
Included Flow/Event Types:
Excluded Flow/Event Types:
Point-in-Time Rule:
Leakage Risk:
Business Confirmation Needed:
*/

At the end, produce a review table with:

- feature_name
- feature_group
- source_table
- mapping/filter_used
- included_types
- excluded_types
- point_in_time_status
- leakage_risk
- recommendation
- business_question

Use only these recommendation values:

- INCLUDE
- REVIEW REQUIRED
- EXCLUDE
- INCLUDE PENDING PROD VALIDATION

Do not build the final modelling dataset yet.

Do not start model training.

Only correct and validate the individual behavioural feature queries for business review.

Stop after updating behavioural_features_business_review.sql.



The key new instruction is:

> exitDateRecorded = approved churn/exit date everywhere. exitDate = do not use.



That will also prevent Copilot from quietly falling back to the older exitDate logic in some of the individual queries.
