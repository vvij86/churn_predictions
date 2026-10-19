Use this as the Copilot prompt. It tells Copilot to read the business SQL/reference files directly and generate a clean review pack of behavioural queries without inventing unreadable mappings.

> I need to restart the Member Retention ML behavioural feature engineering from scratch and first prepare a business-review version of the behavioural SQL queries before building the final feature dataset.

Please review the following available reference files in the workspace:

- MemberRetention_01-AccountBase_v006
- MemberRetention_03-MemberRetentionMetrics_v005
- the business-provided SQL/reference logic containing FlowFact, FlowTypeMap, MMRFlowColumns and related flow mappings
- existing behaviorial.sql only as a reference for the basic feature ideas; do not treat its current logic as final
- existing base historical dataset SQL only for the approved account population, AsOfDate, eligibility and target definitions

The objective is not to create the final consolidated ML feature dataset yet.
First create a new standalone SQL file:

behavioural_features_business_review.sql

This file should contain separate, easy-to-run SQL Server queries for each proposed behavioural feature/group, so I can review them with business before we consolidate them.

Important rules

1. Use SQL Server/T-SQL only.
2. Use parameters rather than hard-coded dates:
   - @AsOfDate
   - @FeatureStartDate = previous 12 months
   - @Recent90Start
   - @Prior90Start
   - @Prior90End
3. All predictive features must use data on or before @AsOfDate only.
4. Do not use any future outcome data as predictive features.
5. Do not use exitDateRecorded, MEMBER_EXIT, future account closure, future rollover completion or other target/outcome information as model inputs.
6. Internal transfers must not be treated as churn-related external rollover behaviour.
7. accountEngagementWeb is empty in UAT but populated in Prod. Keep the website feature queries in scope; do not remove them and do not convert the whole feature group to zero. Document that UAT validation will remain NULL/unavailable and Prod validation is required.
8. Do not guess or invent join keys, flow types, lookup codes, mappings or business meanings.
9. Where FlowFact, FlowTypeMap, MMRFlowColumns or any other reference mapping is required, extract the exact join/filter/mapping logic from the supplied business SQL.
10. If any exact mapping is unclear from the reference files, leave a clearly marked TODO - BUSINESS/REFERENCE CONFIRMATION REQUIRED instead of inventing logic.

First, understand the reference SQL

Before generating features, identify and document:

- how FlowFact is joined to FlowTypeMap
- how FlowFact is joined to MMRFlowColumns
- the fields that define flow type/category
- fields that distinguish inflow vs outflow
- contribution-related flow types
- rollover-in / rollover-out mappings
- withdrawals/payments
- fees
- tax
- insurance-related flows
- internal transfers
- investment-related flows
- administrative/noise flow types
- any existing business filters or exclusions in the reference SQL

Add a comment section at the top called:

REFERENCE FLOW MAPPING SUMMARY

showing the mapping/join logic you found and which source file/query it came from.

Create the following feature-query sections

1. Helpline Behaviour

Generate separate or logically grouped queries for:

- helpline_contact_count_12m
- helpline_inquiry_count_12m
- helpline_active_days_12m
- days_since_last_helpline_contact
- recent_helpline_contact_count_90d
- repeat_contact_flag

Use edgeSource.accountEngagementHelpline.

Do not assume a repeat-contact threshold without labelling it as a proposed business threshold.

2. Website Engagement

Generate:

- web_activity_count_12m
- web_active_days_12m
- days_since_last_web_activity
- recent_web_activity_count_90d

Use edgeSource.accountEngagementWeb.

Add a comment:

UAT source not populated - retain feature definitions for Prod/Databricks validation.

3. Workflow Behaviour

Generate:

- workflow_count_12m
- completed_workflow_count_12m
- open_workflow_count_asof
- days_since_last_workflow
- recent_workflow_count_90d
- repeated workflow/activity indicator where meaningful

Use edgeSource.accountEngagementWorkflow.

Also profile workflow types/statuses and identify likely operational/noisy workflows separately. Do not automatically include every workflow type.

4. Contribution Behaviour

Do not simply count every accountMoneyInflow record as a contribution.

Use the business reference mappings (FlowFact, FlowTypeMap, MMRFlowColumns) where available to identify genuine contribution flows.

Generate:

- contribution_count_12m
- contribution_amount_12m
- avg_contribution_amount_12m
- contribution_active_months_12m
- days_since_last_contribution
- recent_contribution_amount_90d
- prior_contribution_amount_90d
- contribution_decline_flag
- months_of_declining_contribution

Clearly state which mapped flow types are counted as contributions.

5. Money Flow Behaviour

Prefer the supplied mapped flow logic rather than interpreting raw transaction amounts blindly.

Generate:

- total_inflow_12m
- total_outflow_12m
- net_flow_12m
- recent_net_flow_90d
- prior_net_flow_90d
- net_flow_decline_flag
- negative_net_flow_count_12m
- negative_net_flow_months_12m
- avg_monthly_net_flow_12m

If the business reference uses a flow-sign field or mapped flow direction, use that rather than assuming the sign of amount.

6. Rollover / Withdrawal Behaviour

Generate:

- partial_rollover_count_12m
- partial_rollover_amount_12m
- days_since_last_partial_rollover
- recent_partial_rollover_count_90d
- external_rollover_count_12m
- external_rollover_amount_12m
- days_since_last_external_rollover
- recent_external_rollover_count_90d

Use the mapped rollover logic from the business SQL where possible.

Explicitly exclude internal transfers.

Clearly flag any external/full rollover feature that could be close to the churn target as:

LEAKAGE REVIEW REQUIRED

Do not include post-AsOfDate rollover events.

7. Investment Behaviour

Generate only where supported by actual source/reference columns:

- investment_change_count_12m
- days_since_last_investment_change
- investment_active_months_12m
- investment_option_count_asof if reliably derivable
- direct_investment_flag if business meaning is supported
- investment value change measures only if the reference logic proves what the amount/value represents

Do not assume that every investment row represents a behavioural change.

8. Additional Behaviour Patterns

Identify a small number of useful derived patterns from the reference SQL, such as:

- recent 90-day behaviour vs prior 90-day behaviour
- declining contribution pattern
- persistent negative-flow pattern
- increasing outflow pattern
- recent partial-rollover escalation
- engagement drop / inactivity
- repeat helpline activity
- contribution inactivity
- financial-stress pattern combining contribution decline, negative flow and partial rollover

Keep combined patterns clearly labelled as:

CANDIDATE DERIVED FEATURE - BUSINESS/MODEL VALIDATION REQUIRED

Do not create arbitrary rules.

Noise reduction

For every source/table, identify rows/events that should not automatically be treated as behavioural signals, including:

- administrative/system-generated events
- internal transfers
- duplicate/reversal records if applicable
- fees/taxes where they are not member behaviour
- target/outcome events
- events after AsOfDate
- workflow types with no meaningful member behaviour

Use the supplied business reference mappings to reduce this noise.

Output structure

For every feature query, add a header comment in this format:

/*
Feature Name:
Feature Group:
Business Meaning:
Source Table(s):
Source Column(s):
Feature Window:
Filters / Mapping Used:
Point-in-Time Status:
Leakage Risk:
Business Confirmation Needed:
*/

Then provide the runnable SQL query.

At the end of the SQL file, create a review summary

Return one result set/table containing:

- feature_name
- feature_group
- business_meaning
- source_table
- source_columns
- reference_mapping_used
- feature_window
- filter_logic
- point_in_time_status
- leakage_risk
- recommendation
- business_question

recommendation must be one of:

- INCLUDE
- REVIEW REQUIRED
- EXCLUDE
- INCLUDE PENDING PROD VALIDATION

Also create a concise business-review section

At the bottom, group the proposed features under:

1. Helpline Engagement
2. Website Engagement
3. Workflow Activity
4. Contribution Behaviour
5. Money Flow Behaviour
6. Rollover / Withdrawal Behaviour
7. Investment Behaviour
8. Derived Trend / Change Patterns

For each feature, explain the meaning in one simple sentence so a non-technical business user can review it.

Very important

Do not:

- build the final consolidated ML feature dataset
- start model training
- implement missing-value treatment
- perform feature selection
- create Databricks/PySpark code
- change the existing Step 1–5 SQL files
- overwrite behaviorial.sql

Only create:

behavioural_features_business_review.sql

Stop after generating and validating the individual business-review feature queries.

Finally, summarize:

- total number of candidate features
- features sourced directly from existing MercerEdge tables
- features enhanced using FlowFact / FlowTypeMap / MMRFlowColumns
- features requiring business confirmation
- features requiring leakage review
- features that cannot yet be implemented because the reference mapping is unclear.



This version is safer than asking Copilot simply to “generate more behavioural features,” because it forces it to reuse the actual business mappings and explicitly stop when the SQL reference does not support an assumption.
