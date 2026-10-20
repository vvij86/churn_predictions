# Member Retention ML - Copilot Instructions

## Purpose

This file contains the reusable context, business rules, source references, technical guardrails and execution guidance for the MercerEdge Member Retention / Churn ML tactical solution.

Read this file before generating or modifying any ML feature engineering SQL.

Do not assume any business logic that is not explicitly supported by the reference files or confirmed rules below.

---

# 1. Business Reference SQL Files

Use the following business-provided SQL files as the primary reference for approved account population logic, source mappings, lookup logic, flow classifications, description filters, type filters and other reusable business rules:

- `MemberRetention_01-AccountBase_v006.sql`
- `MemberRetention_03-MemberRetentionMetrics_v005.sql`

Use these files as reference sources of truth where applicable.

Important:
- Reuse relevant mapping/filter/join logic.
- Do not blindly copy complete queries.
- Do not invent lookup values or flow classifications.
- If reference logic is unclear, mark it as:

`TODO - BUSINESS / REFERENCE CONFIRMATION REQUIRED`

---

# 2. ML Objective

The tactical ML solution predicts account-level member churn / retention risk.

The modelling grain is:

`one row per account_id + AsOfDate`

The model output is expected to contain account-level churn probability, risk band and churn drivers for downstream consumption.

---

# 3. Training History

The current expectation is to train using approximately:

`36 months of historical data`

This is the **overall training history** and is different from the feature window.

Important:
- Training history = how much historical snapshot/training data is used to build the model.
- Feature window = how much past behaviour is used to calculate features for each individual AsOfDate.

Current default:
- Training history: approximately 36 months
- Feature window per snapshot: previous 12 months
- Outcome window: future period after AsOfDate, currently proposed as 3 months

Do **not** automatically use a 36-month feature window just because the training history is 36 months.

Historical availability must be validated against Bronze/MercerEdge source views.

---

# 4. Approved Source Tables / Views

Use the following 15 source tables/views as the primary source scope:

1. `edgeSource.accountSummary`
2. `edgeSource.accountEngagementWorkflow`
3. `edgeSource.accountEngagementHelpline`
4. `edgeSource.accountEngagementWeb`
5. `edgeSource.AccountInsuranceCurrent`
6. `edgeSource.accountInvestments`
7. `edgeSource.accountMoneyInflow`
8. `edgeSource.accountNetMoneyFlow`
9. `edgeSource.accountRolloverPayment`
10. `edgeSource.campaignEventDetails`
11. `edgeSource.campaignEvents`
12. `edgeSource.customerMapping`
13. `edgeSource.customerSummary`
14. `edgeSource.thirdPartyAuthority`
15. `tableau.fundListSource`

Do not introduce additional source tables unless:
- clearly required,
- supported by the business reference SQL,
- or explicitly requested.

Campaign-related extra tables such as `Campaign` or `CampaignAccountMapping` should not automatically be added to the current tactical feature scope unless explicitly requested.

---

# 5. Data Exploration Reference Files

Use the following EDA workbooks to understand useful churn-driver columns, source behaviour, null patterns, data quality and table usefulness:

- `MercerEdge_ML_Churn_Driver_EDA_Phase2.xlsx`
- `MercerEdge_ML_Churn_Driver_EDA_Remaining_Tables_part2.xlsx`

Use these for:
- candidate feature identification
- useful columns
- source profiling
- data quality awareness
- sparse/null field awareness
- behavioural feature discovery

Do not treat an EDA suggestion as an approved business rule unless separately confirmed.

---

# 6. DDL Reference Files

Use the following SQL files to confirm:

- table names
- column names
- data types
- available source fields

Files:

- `All_table_scripts.sql`
- `All_Other_tables_Not_explored.sql`

Always validate source column names against these files before writing SQL.

Do not invent column names.

---

# 7. Database / Python Environment

Use the existing Python environment for profiling, query validation or utility scripts.

Use:
- the existing project Python virtual environment
- `.env` for required configuration / credentials
- `sample.py` as the reference database connection example

Do not hard-code usernames, passwords or secrets.

If package installation requires authenticated access, use the existing environment/configuration already provided in the project.

Do not expose credentials in generated code.

---

# 8. Environment / Architecture

Current tactical architecture:

`Bronze -> ML Feature Engineering -> Gold / ML Feature Dataset -> ML Model -> Persisted ML Scoring Output -> Power BI`

There is no Silver layer for the current tactical approach.

Bronze is expected to use truncate-and-load behaviour, therefore Bronze itself does not preserve previous load versions.

Important distinction:

Truncate-and-load does not automatically mean historical business events are unavailable.

A Bronze view may still contain historical dated rows such as:
- inflow transactions
- rollover events
- helpline contacts
- workflow events

However, current-state tables may not allow old account states to be reconstructed.

When designing historical training features, assess whether each source supports point-in-time reconstruction.

If historical values cannot be reconstructed reliably from Bronze, historical feature snapshots / feature versioning may need to be retained in Gold.

---

# 9. AsOfDate / Snapshot Date

For this ML solution:

`AsOfDate = Snapshot Date`

They represent the historical prediction cut-off date.

Example:

`AsOfDate = 31-Mar-2024`

Only information available on or before this date may be used as predictive input.

Do not derive AsOfDate from `fundJoinDate`.

AsOfDate is the chosen prediction/snapshot date.

---

# 10. Account Historical Existence Rule

Use `fundJoinDate` to determine whether an account existed at the AsOfDate.

Approved rule:

```sql
fundJoinDate <= @AsOfDate
```

Meaning:

- `fundJoinDate <= AsOfDate` -> account existed at the snapshot
- `fundJoinDate > AsOfDate` -> account did not yet exist and must be excluded

Newly joined accounts are allowed.

Do not enforce a minimum tenure unless specifically requested or confirmed later.

---

# 11. Approved Exit / Churn Date

IMPORTANT:

Use:

`accountSummary.exitDateRecorded`

Do NOT use:

`exitDate`

The latest business-confirmed churn/exit date field is:

`exitDateRecorded`

Search generated SQL and ensure old `exitDate` logic is not used.

---

# 12. Historical Eligibility Logic

The account should exist at AsOfDate and should not already have exited.

Use logic aligned to:

```sql
fundJoinDate <= @AsOfDate
AND (
    exitDateRecorded IS NULL
    OR exitDateRecorded > @AsOfDate
)
```

Also apply approved death exclusion logic.

`exitDateRecorded` may be used for:
- historical eligibility
- target creation

It must not be used as a predictive model feature.

---

# 13. Churn Definition

The churn target is based on `exitDateRecorded`.

For an eligible account:

```sql
exitDateRecorded > @AsOfDate
AND exitDateRecorded <= @OutcomeEndDate
```

and after applying:
- internal transfer exclusion
- death exclusion

then:

`target_churn = 1`

Otherwise, for an eligible retained account:

`target_churn = 0`

Example:

- AsOfDate = 31-Mar-2024
- Outcome window = 01-Apr-2024 to 30-Jun-2024
- exitDateRecorded = 15-May-2024
- internalTransferFlag = 0
- not deceased

Result:

`target_churn = 1`

---

# 14. Retention Definition

An eligible account is retained when no qualifying churn event occurs during the outcome window.

For such accounts:

`target_churn = 0`

---

# 15. Internal Transfer Rule

Internal transfers are not treated as normal churn.

Use the approved source logic from:
- `accountRolloverPayment.internalTransferFlag`
- and/or business reference mapping logic

Do not count internal transfers as:
- churn
- external rollover behaviour
- churn-risk rollover events unless explicitly required for another business purpose

---

# 16. Death Exclusion

Death-related exits are excluded from ordinary churn modelling.

Use the approved accountSummary death fields / business logic.

Death-related records should not be labelled as ordinary churn.

---

# 17. Feature Window

Current default feature window:

`previous 12 months before AsOfDate`

This is intentionally separate from the 36-month overall training history.

Example:

- AsOfDate = 31-Mar-2024
- FeatureStartDate = 01-Apr-2023
- FeatureEndDate = 31-Mar-2024

All predictive behavioural features must use:

```sql
event_date >= @FeatureStartDate
AND event_date <= @AsOfDate
```

Do not use post-AsOfDate activity.

Do not automatically extend the feature window to 36 months unless explicitly requested or supported by business/model validation.

---

# 18. Outcome Window

Outcome observation starts:

`AsOfDate + 1 day`

Example:

- AsOfDate = 31-Mar-2024
- OutcomeStartDate = 01-Apr-2024

Current proposed outcome period:

`3 months`

Example:

01-Apr-2024 to 30-Jun-2024

Use the approved value once business confirmation is final.

---

# 19. Target Leakage Rules

The following must not be predictive features:

- `exitDateRecorded`
- `MEMBER_EXIT`
- future account closure
- future full rollover completion
- future outcome-window events
- any feature derived using information after AsOfDate
- days until exit
- future churn flag
- future closure indicator

`exitDateRecorded` is allowed only for:
- eligibility
- target creation

Never include it in the predictive feature matrix.

---

# 20. Point-in-Time Safety

Every predictive feature must be calculated using data available on or before the AsOfDate.

Mandatory rule:

```sql
event_date <= @AsOfDate
```

Prefer:

```sql
event_date >= @FeatureStartDate
AND event_date <= @AsOfDate
```

For each feature, document:

- source date column
- feature window
- point-in-time status
- leakage risk

---

# 21. Website Engagement Special Handling

`edgeSource.accountEngagementWeb` is currently not populated in UAT.

However, the source is expected to contain data in Prod.

Therefore:

- do not remove website features
- do not treat missing UAT data as zero
- keep website features NULL/unavailable in UAT
- mark them:

`INCLUDE PENDING PROD VALIDATION`

Possible website features include:
- web_activity_count_12m
- web_active_days_12m
- days_since_last_web_activity
- recent_web_activity_count_90d

---

# 22. Behavioural Feature Groups

## 22.1 Helpline Engagement

Candidate features:

- helpline_contact_count_12m
- helpline_inquiry_count_12m
- helpline_active_days_12m
- days_since_last_helpline_contact
- recent_helpline_contact_count_90d
- repeat_contact_flag

Use:
`edgeSource.accountEngagementHelpline`

Reduce noise using business/reference logic where available.

## 22.2 Website Engagement

Candidate features:

- web_activity_count_12m
- web_active_days_12m
- days_since_last_web_activity
- recent_web_activity_count_90d

Use:
`edgeSource.accountEngagementWeb`

UAT handling:
keep NULL, do not convert to zero.

## 22.3 Workflow Behaviour

Candidate features:

- workflow_count_12m
- completed_workflow_count_12m
- open_workflow_count_asof
- days_since_last_workflow
- recent_workflow_count_90d
- repeated workflow indicator where meaningful

Use:
`edgeSource.accountEngagementWorkflow`

Important:
Do not automatically count all workflow types.

Profile and identify:
- useful member-driven workflow types
- administrative workflows
- system-generated workflows
- noisy operational workflows

Mark unclear types for business review.

## 22.4 Contribution Behaviour

Use exact business mapping/filter logic where available.

Candidate features:

- contribution_count_12m
- contribution_amount_12m
- avg_contribution_amount_12m
- contribution_active_months_12m
- days_since_last_contribution
- recent_contribution_amount_90d
- prior_contribution_amount_90d
- contribution_decline_flag
- months_of_declining_contribution

Use genuine contribution types only.

Based on reference logic, candidate mapped types may include:

- Employer SG
- Salary Sacrifice
- Post Tax Voluntary

Only use these if confirmed from the business reference SQL.

Do not automatically count:
- rollover in
- internal transfer
- insurance claim proceeds
- adjustments
- unrelated inflows

Avoid broad filters such as:

```sql
inflowDescription NOT IN (...)
```

if they allow unrelated inflows to be counted as contributions.

---

# 23. Business Flow Mapping

Use `MemberRetention_03-MemberRetentionMetrics_v005.sql` as the main reference for flow classification logic.

Where supported by the reference SQL, derive a normalized field such as:

`mapped_flow_type`

Possible mappings seen in reference logic include patterns such as:

- Employer / Employer Additional Conts -> Employer SG
- Voluntary Member Salary Sacrifice -> Salary Sacrifice
- Member Voluntary -> Post Tax Voluntary
- Rollovers-In -> Rollover In
- Internal Transfer -> Internal Transfer In
- Adjustment -> Adjustment
- insurance/claim-related Other Conts -> Insurance Claim Proceeds

Do not simplify these rules without checking the reference SQL.

Do not invent new mappings.

---

# 24. Net Money Flow Behaviour

Candidate features:

- total_inflow_12m
- total_outflow_12m
- net_flow_12m
- recent_net_flow_90d
- prior_net_flow_90d
- net_flow_decline_flag
- negative_net_flow_count_12m
- negative_net_flow_months_12m
- avg_monthly_net_flow_12m

Use the reference flow direction/sign logic.

Do not assume:
positive amount = inflow
negative amount = outflow

unless supported by the reference logic.

---

# 25. Rollover / Withdrawal Behaviour

Candidate features:

- partial_rollover_count_12m
- partial_rollover_amount_12m
- days_since_last_partial_rollover
- recent_partial_rollover_count_90d
- external_rollover_count_12m
- external_rollover_amount_12m
- days_since_last_external_rollover
- recent_external_rollover_count_90d

Keep separate:
- partial rollover
- rollover in
- external rollover out
- internal transfer

Internal transfers must be excluded from external rollover risk behaviour.

Any full/external rollover feature close to actual account closure should be marked:

`LEAKAGE REVIEW REQUIRED`

---

# 26. Investment Behaviour

Candidate features may include:

- investment_change_count_12m
- days_since_last_investment_change
- investment_active_months_12m
- investment_option_count_asof
- direct_investment_flag
- investment value/change measures where business meaning is clear

Use:
`edgeSource.accountInvestments`

Do not assume every investment row represents member behavioural activity.

Use only fields whose business meaning is supported by source/reference logic.

---

# 27. Insurance Behaviour

Use:
`edgeSource.AccountInsuranceCurrent`

Treat current-state insurance fields carefully.

Check whether historical point-in-time reconstruction is possible.

Do not assume current insurance status represents the historical AsOfDate state unless supported by:
- effectiveDateFrom
- effectiveDateTo
- historical rows
- other valid effective-date logic

Insurance claim proceeds must not be counted as ordinary contributions.

---

# 28. Third Party Authority

Use:
`edgeSource.thirdPartyAuthority`

Possible point-in-time rule:

```sql
dateAuthorityRequested <= @AsOfDate
AND (
    terminationDate IS NULL
    OR terminationDate > @AsOfDate
)
```

Use only where business/source semantics are supported.

---

# 29. Campaign Features

Campaign engagement is currently deferred / not active tactical scope unless explicitly reintroduced.

Do not automatically add campaign engagement features to the final feature set.

Campaign-related outcome events such as `MEMBER_EXIT` must never be predictive features.

If campaign logic is explored, keep it separate and mark its status clearly.

---

# 30. Customer Experience / Qualtrics

Candidate future features may include:

- CSAT
- NPS
- VoC
- survey response recency

These are not automatically approved current tactical inputs.

Use only after business and source confirmation.

If included later, only use survey/customer-experience data available on or before AsOfDate.

---

# 31. Derived Trend Features

Prefer meaningful behavioural patterns over only raw totals.

Candidate derived patterns:

- recent 90 days vs previous 90 days
- contribution decline
- persistent negative cash flow
- increasing outflow
- recent rollover escalation
- engagement drop
- inactivity
- repeated helpline contact
- months with no contributions
- financial stress pattern

Any combined feature rule must be labelled:

`CANDIDATE DERIVED FEATURE - BUSINESS/MODEL VALIDATION REQUIRED`

Do not invent arbitrary thresholds without marking them for review.

---

# 32. Noise Reduction

For every behavioural source, explicitly check for noise.

Potential exclusions / review items include:

- internal transfers
- adjustments
- insurance claim proceeds
- fees
- tax
- administrative records
- system-generated records
- duplicate records
- reversal records
- future outcome events
- target events
- events after AsOfDate
- workflow types without meaningful member behaviour

Use business reference SQL to determine valid filters where available.

---

# 33. Missing Value Principles

Do not apply missing-value treatment blindly during initial feature engineering.

Understand the business meaning of NULL first.

Examples:

- no matching contribution rows may legitimately mean zero contribution activity
- no rollover rows may legitimately mean zero rollover activity
- recency features may remain NULL when no historical event exists
- website features must remain NULL in UAT because the entire UAT source is not populated

Do not convert the entire web feature group to zero.

Missing-value treatment should be documented separately and applied only after feature semantics are understood.

---

# 34. Feature Versioning / Historical Reproducibility

Bronze is truncate-and-load and does not preserve previous ingestion versions.

Therefore evaluate whether historical feature snapshots can be reconstructed from dated Bronze rows.

For each source classify as:

- HISTORICAL / REBUILDABLE
- CURRENT STATE ONLY
- UNCLEAR

If important historical feature values cannot be reconstructed later, persist/version ML feature snapshots in Gold.

Feature versioning should support:
- training reproducibility
- auditability
- model version traceability
- recreating historical training inputs

---

# 35. Feature Dataset Persistence

For training, a persisted feature dataset in the ML/Gold area is recommended where it supports:
- repeated model experiments
- reproducibility
- historical snapshot preservation
- auditability

For scoring:
- the temporary scoring feature dataset does not necessarily need to be persisted
- the final ML scoring output should be persisted

High-level scoring flow:

`Bronze -> Feature Engineering -> Temporary Scoring Dataset -> Model -> Persistent ML Output -> Power BI`

---

# 36. Validation Requirements

Every feature-engineering step must include validation.

At minimum validate:

## Grain
One row per:

`account_id + AsOfDate`

## Duplicate check

Expected:

`duplicate_account_id_asof_count = 0`

## Point-in-time safety

No feature event may be later than AsOfDate.

Expected:

`future_events_used_in_features = 0`

## Target preservation

When adding features, target counts should remain unchanged unless the population intentionally changes.

Validate:
- churn row count
- retained row count
- null target row count

## Row-count preservation

Joining features must not unintentionally create or remove eligible accounts.

Compare:
- eligible rows before feature join
- rows after feature join

## Null profiling

For each feature:
- null_count
- null_pct

## Variance / usefulness

Check:
- distinct_count
- constant/near-constant features
- extreme sparsity

## Leakage

Flag features too close to:
- churn outcome
- closure
- full rollover completion
- future events

---

# 37. Time-Based Validation

Use time-based validation rather than random splitting for model validation.

High-level requirement:

Older data is used for training and later data is used for validation.

Example:

Train through:
`31-Dec-2024`

Validate:
`Jan-Mar 2025`

Detailed fold design belongs in the ML design document.

Do not put detailed implementation logic into the FRS unless specifically requested.

---

# 38. Risk Bands

Initial proposed risk bands:

- High Risk: churn_probability >= 0.70
- Medium Risk: 0.40 to 0.69
- Low Risk: < 0.40

Business meaning:

- High Risk -> relatively high likelihood of churn / priority attention
- Medium Risk -> moderate likelihood / monitor
- Low Risk -> relatively low likelihood of churn

These thresholds may be refined after model validation and business review.

---

# 39. ML Output

Expected scoring output may include:

- account_id
- member_id
- as_of_date
- churn_probability
- risk_band
- primary_churn_driver
- additional_churn_drivers
- retention_category
- current_account_fum_amount
- model_version
- scoring_date

Power BI should consume the persisted ML scoring output.

Power BI should not directly trigger model execution.

---

# 40. General Copilot Guardrails

Always follow these rules:

1. Read this instruction file first.
2. Read the relevant reference SQL before generating feature logic.
3. Do not invent source columns.
4. Do not invent lookup values.
5. Do not invent business mappings.
6. Do not invent join keys.
7. Do not silently change confirmed business rules.
8. Use `exitDateRecorded`, not `exitDate`.
9. Use `fundJoinDate <= @AsOfDate` for account historical existence.
10. Use only data available on or before AsOfDate for predictive features.
11. Never use the churn label as a feature.
12. Never use future outcome data as a feature.
13. Internal transfers are not ordinary churn.
14. Death-related exits are excluded.
15. Keep accountEngagementWeb features in scope despite UAT being empty.
16. Use exact reference flow mapping logic where available.
17. Reduce noise before aggregating behavioural events.
18. Prefer recency, frequency, trend and recent-vs-prior features over raw counts only.
19. Keep query logic modular and reviewable.
20. Do not overwrite existing validated SQL unless explicitly requested.
21. When rebuilding from scratch, create new files.
22. Validate every major feature-engineering step.
23. If uncertain, mark:
    `TODO - BUSINESS / REFERENCE CONFIRMATION REQUIRED`
24. Do not confuse 36-month training history with the 12-month feature window.
25. Do not use a 36-month feature window unless explicitly requested or validated.

---

# 41. Restart-from-Scratch Rule

For the new feature-engineering rebuild:

Do not use the previously generated Step 1-Step 5 SQL as the source of truth.

They may be used only for:
- comparison
- validation
- checking previously identified feature ideas

The new implementation must be rebuilt using:

1. latest business rules
2. `MemberRetention_01-AccountBase_v006.sql`
3. `MemberRetention_03-MemberRetentionMetrics_v005.sql`
4. 15 approved source tables/views
5. EDA workbooks
6. DDL files
7. this instruction file

This is intended to avoid carrying old assumptions or incorrect mappings into the rebuilt solution.

---

# 42. Recommended Development Sequence

When rebuilding feature engineering from scratch, follow this sequence:

1. Validate source availability and history
2. Build eligible historical account population
3. Apply approved churn/retention target logic
4. Build reusable business flow mappings
5. Build account / tenure / product features
6. Build helpline engagement features
7. Build website engagement definitions
8. Build workflow behavioural features
9. Build contribution behaviour
10. Build money-flow behaviour
11. Build rollover / withdrawal behaviour
12. Build investment / insurance features where historically valid
13. Add recency / trend / recent-vs-prior features
14. Join back to one row per account_id + AsOfDate
15. Validate point-in-time safety
16. Validate leakage
17. Validate row grain and duplicates
18. Profile missing values / sparsity
19. Review candidate feature list with business
20. Only then prepare the final modelling feature dataset

---

# 43. Output Style for Feature SQL

When generating individual feature SQL queries, use this comment block:

```sql
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
Business Confirmation Needed:
*/
```

Keep individual queries readable and independently reviewable.

Do not create one huge consolidated SQL until the feature definitions have been reviewed.

---

# 44. Feature Review Recommendation Values

When generating a feature review summary, use only:

- `INCLUDE`
- `REVIEW REQUIRED`
- `EXCLUDE`
- `INCLUDE PENDING PROD VALIDATION`

Recommended review columns:

- feature_name
- feature_group
- business_meaning
- source_table
- source_columns
- reference_mapping_used
- included_types
- excluded_types
- feature_window
- point_in_time_status
- leakage_risk
- recommendation
- business_question

---

# 45. Mandatory Final Checks

Before declaring any feature SQL ready, confirm:

- no unintended `exitDate` usage
- `exitDateRecorded` used where churn/exit date is required
- no post-AsOfDate data used
- no target field included as a predictor
- internal transfers excluded correctly
- death exclusion preserved
- one row per account_id + AsOfDate
- no duplicate account snapshot rows
- flow mappings match reference SQL
- web UAT limitation documented
- no invented source logic
- training history and feature window are treated as separate concepts
