Please revise the current Copilot-generated SQL and STEP BACK to create ONLY the BASE HISTORICAL MODELLING DATASET.

Do NOT proceed to feature engineering yet.

The current query has gone too far by creating engineered features such as:
- contribution_count_12m
- contribution_amount_12m
- days_since_last_contribution
- net_money_flow_12m
- rollover_count_12m
- web_activity_count_3m
- helpline_call_count_6m
- campaign_open_rate
- campaign_click_rate
- investment activity aggregates
- recent vs prior period trend flags
- other derived behavioural aggregates

These belong to the NEXT feature-engineering step and must be removed from this base-dataset version.

OBJECTIVE
---------
Create a clean BASE HISTORICAL MODELLING DATASET only for the Tactical Retention/Churn solution using MercerEdge as the ONLY source database.

The base dataset should establish:

1. Historical account population
2. Account/member/customer mappings
3. Correct historical account snapshot as of the modelling date
4. Eligibility/exclusion rules
5. Churn target definition
6. Date boundaries for later feature engineering
7. Raw/reference source columns needed for the next step

MODELLING GRAIN
---------------
The final grain must be:

one row per account_id + as_of_date

IN-SCOPE MERCEREDGE TABLES
--------------------------
The following 18 tables are in scope for this tactical solution:

1. merceredge.edgeSource.accountSummary
2. merceredge.edgeSource.accountEngagementWorkflow
3. merceredge.edgePortalSource.pensionerData
4. merceredge.edgeSource.accountEngagementHelpline
5. merceredge.edgeSource.accountEngagementWeb
6. merceredge.edgeSource.AccountInsuranceCurrent
7. merceredge.edgeSource.accountInvestments
8. merceredge.edgeSource.accountMoneyInflow
9. merceredge.edgeSource.accountNetMoneyFlow
10. merceredge.edgeSource.accountRolloverPayment
11. merceredge.edgeSource.campaignEventDetails
12. merceredge.edgeSource.campaignEvents
13. merceredge.edgeSource.customerMapping
14. merceredge.edgeSource.customerSummary
15. merceredge.edgeSource.thirdPartyAuthority
16. merceredge.tableau.fundListSource
17. merceredge.edgeSource.campaign
18. merceredge.edgeSource.campaignAccountMapping

IMPORTANT:
- These 18 tables are the complete source scope for the tactical solution.
- Do NOT force all 18 tables into the base historical dataset.
- Use only the tables required at this stage for:
  - base population
  - account/member/customer mapping
  - historical snapshot
  - target creation
  - eligibility/exclusion logic
  - raw/reference fields
- Tables mainly needed for behavioural feature engineering should be documented for the next step, not aggregated now.

FILES TO USE
------------
Use these project files:

1. All_table_scripts.sql
   - DDL/source structure

2. All_Other_tables_Not_explored.sql
   - Additional DDL/source structure

3. MercerEdge_ML_Churn_Driver_EDA_Phase2.xlsx
   - Existing data exploration results

4. MercerEdge_ML_Churn_Driver_EDA_Remaining_Tables_part2.xlsx
   - Remaining-table exploration results

5. .env
   - SQL Server connection values

6. sample.py
   - Existing working DB connection example

Use the DDL files as the source of truth for actual table and column names.

Use the EDA Excel files only to understand:
- data availability
- nulls
- date coverage
- source relevance
- data quality
- possible leakage concerns

DATABASE CONNECTION
-------------------
Reuse the working SQL Server connection logic from sample.py.

Use:
- pyodbc
- python-dotenv
- values from .env
- Trusted Connection / Windows Authentication if that is what sample.py uses
- TrustServerCertificate if required

Do not hardcode credentials.

Use the currently active Python environment.

Do not create a new environment unless absolutely required.

DATE PARAMETERS
---------------
Keep explicit modelling parameters such as:

DECLARE @FeatureStartDate DATE = '...';
DECLARE @AsOfDate DATE = '...';
DECLARE @OutcomeStartDate DATE = DATEADD(DAY, 1, @AsOfDate);
DECLARE @OutcomeEndDate DATE = DATEADD(MONTH, 3, @AsOfDate);

At this stage:

- @FeatureStartDate and @AsOfDate define the historical observation boundary
- do NOT calculate aggregated ML features yet
- @OutcomeStartDate and @OutcomeEndDate are used only for target creation

BASE POPULATION
---------------
Use edgeSource.accountSummary as the main/core historical account source where appropriate.

Before finalizing:
- inspect actual coverage
- confirm reportingDate usage
- ensure one historical row per account as of @AsOfDate

Do not silently lose accounts because of joins.

Use LEFT JOIN where appropriate.

Maintain:
one row per account_id + as_of_date

ACCOUNT SUMMARY SNAPSHOT
------------------------
For accountSummary:

- select the latest valid accountSummary snapshot on or before @AsOfDate
- use reportingDate for point-in-time selection where available
- do not use reportingDate after @AsOfDate
- do not fabricate historical dates where reportingDate is NULL
- clearly flag missing or invalid historical snapshot cases

Retain directly sourced/raw fields where physically available, such as:

- accountID
- memberNumber
- customerID
- fundID
- reportingDate
- fundJoinDate
- exitDate
- exitType
- dateOfDeath
- account status
- account type
- current age
- age band
- state
- raw account balance / FUM fields
- directly sourced profile fields useful for later modelling

Do NOT transform these into engineered features yet.

MEMBER / CUSTOMER MAPPING
-------------------------
Use customerMapping and/or customerSummary only where needed to resolve:

- member_number_ref
- customer_id
- account/member/customer relationship
- directly sourced customer/profile fields

These identifiers are reference/join fields, not predictive ML features.

Do not remove an account only because member mapping is unavailable.

Instead create a flag such as:

- has_member_mapping

Do not use customer/member IDs as predictive features.

CHURN TARGET
------------
Create target_churn only.

Primary churn source:
- accountSummary.exitDate

Suggested target logic:

target_churn = 1 when:
- exitDate > @AsOfDate
- exitDate <= @OutcomeEndDate
- account is not an internal transfer
- account is not deceased
- account satisfies eligibility rules

target_churn = 0 when:
- account is eligible at @AsOfDate
- no qualifying churn exit occurs during the outcome window

Do NOT use exitDate as a predictive feature.

INTERNAL TRANSFER EXCLUSION
---------------------------
Use:

Primary:
- edgeSource.accountRolloverPayment.internalTransferFlag

Supporting:
- edgeSource.accountSummary.exitType = 'Internal Transfer'

Create:
- is_internal_transfer

Internal transfers must NOT be classified as churn.

Do not engineer rollover features yet.

Do not calculate:
- rollover_count
- rollover_amount
- days_since_last_rollover
- partial rollover aggregates
or other rollover-derived features yet.

DEATH EXCLUSION
---------------
Use:

- accountSummary.dateOfDeath as the primary death indicator

Create:
- is_deceased

Deceased accounts must be excluded from the churn modelling population according to the agreed business rule.

Do not create death-related predictive features.

ELIGIBILITY
-----------
Create only clear modelling eligibility/support flags such as:

- has_valid_accountsummary_snapshot
- has_member_mapping
- is_internal_transfer
- is_deceased
- is_eligible_for_modelling

Do NOT create behavioural-history flags based on feature activity unless explicitly required by an agreed business rule.

Do NOT create:
- has_required_history based on contribution/web/campaign/etc. activity

unless the minimum required history rule has already been confirmed.

If minimum historical coverage is still undecided, clearly document it as a pending business rule.

RAW SOURCE FIELDS FOR LATER FEATURE ENGINEERING
-----------------------------------------------
Where useful, retain or document directly sourced raw fields required for the next stage, for example:

From accountMoneyInflow:
- raw inflow date
- raw inflow type
- raw inflow amount

From accountNetMoneyFlow:
- raw reference date
- raw cash flow sign/type
- raw amount

From accountRolloverPayment:
- raw payment date
- raw payment amount
- withdrawal/full-partial indicators
- internalTransferFlag

From accountEngagementWeb:
- raw activity/request date
- raw activity/event fields

From accountEngagementHelpline:
- raw call/contact date
- raw contact type

From accountEngagementWorkflow:
- raw workflow dates/status fields

From accountInvestments:
- raw investment date
- investment option/type
- raw value/units

From AccountInsuranceCurrent:
- raw insurance status/effective dates/amounts

From campaignAccountMapping:
- campaignID
- dateSent
- openDate
- clickDate

From campaignEventDetails/campaignEvents:
- eventID
- eventName
- eventDate
- eventAmount

From thirdPartyAuthority:
- raw request/effective dates
- raw status/type fields

IMPORTANT:
Do NOT directly join lower-grain transaction/event rows into the final base dataset if that breaks:

one row per account_id + as_of_date

If lower-level raw rows cannot be included without duplicating accounts:
- do not aggregate them yet
- document the table/column for the next feature-engineering step

NO FEATURE ENGINEERING YET
--------------------------
Do NOT create any of these in this base historical dataset:

- contribution_count_*
- contribution_amount_*
- avg_contribution_*
- contribution decline/trend flags
- days/months_since_last_contribution
- net_money_flow_*
- negative_net_flow_flag
- rollover_count_*
- rollover_amount_*
- partial_rollover_count_*
- days_since_last_rollover
- web_activity_count_*
- web inactivity flags
- days_since_last_web_activity
- helpline_contact_count_*
- repeat helpline flags
- workflow_count_*
- investment activity counts
- investment value aggregates
- insurance aggregates
- campaign_send_count
- campaign_open_count
- campaign_click_count
- campaign_open_rate
- campaign_click_rate
- campaign engagement recency
- campaign event counts
- recent_90 vs prior_90 comparisons
- trend flags
- recency-derived features
- behavioural aggregates
- transformed ML-ready features

These belong to the NEXT STEP:

FEATURE ENGINEERING

Do not start that step now.

EXPECTED BASE HISTORICAL DATASET OUTPUT
---------------------------------------
The final output should be simple and contain fields like:

Identifiers:
- account_id
- member_number_ref
- customer_id
- fund_id

Modelling dates:
- as_of_date
- feature_start_date
- outcome_start_date
- outcome_end_date

Historical source dates:
- account_summary_reporting_date
- fund_join_date

Raw account/profile fields:
- account_status
- account_type
- current_age
- age_band
- state
- raw account_balance / FUM
- directly sourced account/profile fields

Target-support fields:
- exit_date
- exit_type
- date_of_death
- internalTransferFlag

Eligibility/exclusion flags:
- has_valid_accountsummary_snapshot
- has_member_mapping
- is_internal_transfer
- is_deceased
- is_eligible_for_modelling

Target:
- target_churn

IMPORTANT:
exit_date, exit_type, date_of_death and internalTransferFlag are support fields for target/exclusion logic and must NOT later become predictive features automatically.

TEMP TABLE / CTE STRUCTURE
--------------------------
Keep the SQL simple and staged.

Suggested structure:

1. Parameters
2. account_summary_ranked
3. account_summary_snapshot
4. member/customer mapping resolution
5. internal transfer logic
6. death exclusion logic
7. outcome/churn target logic
8. base historical dataset assembly
9. validation queries

Use clear temp-table names such as:

- #base_historical_population
- #base_historical_dataset

Do NOT use confusing names such as:

- #modelling_dataset_scored

because there is no ML scoring at this stage.

VALIDATION
----------
After revising the SQL, validate it against the actual MercerEdge SQL Server using:

- .env
- sample.py connection approach
- pyodbc
- read-only queries only

Validate:

1. SQL compiles successfully
2. one row per account_id + as_of_date
3. duplicate account_id + as_of_date count = 0
4. NULL account_id count = 0
5. NULL as_of_date count = 0
6. selected accountSummary snapshot is <= @AsOfDate
7. no future account snapshot leakage
8. target_churn only uses the outcome window
9. exitDate after @AsOfDate is not used as a feature
10. death exclusion using dateOfDeath works correctly
11. internal transfer exclusion using internalTransferFlag works correctly
12. accountSummary.exitType = 'Internal Transfer' is used as supporting evidence
13. account/member mapping coverage
14. eligible vs excluded account counts
15. churn vs retained counts
16. no engineered feature columns remain
17. final grain remains one row per account_id + as_of_date

Also print sample rows showing:

- retained account
- churn account
- internal transfer account
- deceased account
- missing member mapping account
- missing valid snapshot account if present

FINAL DELIVERABLE
-----------------
Create/update:

build_merceredge_base_historical_dataset.sql

Do NOT create the feature-engineering SQL yet.

At the end, summarize:

1. Which of the 18 tables are actually used in the base historical dataset
2. Why each used table is required
3. Which of the 18 tables are deferred to feature engineering
4. What feature-engineering logic was removed from the previous query
5. Final dataset grain
6. Churn target logic
7. Internal transfer logic
8. Death exclusion logic
9. Eligibility logic
10. Any unresolved business rules
11. Validation results

Please revise the existing Copilot-generated SQL IN PLACE and step back to this base historical dataset stage.

Do not jump ahead to feature engineering.
