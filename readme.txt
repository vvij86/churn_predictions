I need to create a fresh base historical modelling dataset query for the Tactical Retention/Churn solution using MercerEdge as the ONLY source database.

This is the first modelling dataset build for the tactical approach.

IMPORTANT BUSINESS CONTEXT
--------------------------
Modelling grain:
- One row per account_id per as_of_date

Source:
- MercerEdge SQL Server only

Churn definition:
- Churn is based on exitDate from edgeSource.accountSummary
- If exitDate falls inside the defined outcome window, treat the account as churned, subject to exclusions below

Internal transfer exclusion:
- Primary indicator: internalTransferFlag from edgeSource.accountRolloverPayment
- Also use accountSummary.exitType = 'Internal Transfer' as supporting evidence
- Internal transfers must NOT be classified as churn

Death exclusion:
- Primary death indicator: dateOfDeath from edgeSource.accountSummary
- Deceased accounts must be excluded from the modelling population / churn target as per business rules
- Do not classify death exits as churn

Do not assume any other churn definition unless supported by the supplied DDL/data exploration or explicitly documented.

IN-SCOPE TABLES
---------------
Use ONLY these 18 MercerEdge tables:

1. merceredge.edgeSource.accountSummary
2. merceredge.edgeSource.accountEngagementWorkflow
3. merceredge.edgePortalSource.pensionerData
4. merceredge.edgeSource.accountEngagementHelpline
5. merceredge.edgeSource.accountEngagementWeb
6. MercerEdge.EdgeSource.AccountInsuranceCurrent
7. merceredge.edgeSource.accountInvestments
8. merceredge.edgeSource.accountMoneyInflow
9. merceredge.edgeSource.accountNetMoneyFlow
10. merceredge.edgeSource.accountRolloverPayment
11. MercerEdge.EdgeSource.campaignEventDetails
12. MercerEdge.EdgeSource.campaignEvents
13. merceredge.edgeSource.customerMapping
14. merceredge.edgeSource.customerSummary
15. merceredge.edgeSource.thirdPartyAuthority
16. merceredge.tableau.fundListSource
17. merceredge.edgeSource.campaign
18. merceredge.edgeSource.campaignAccountMapping

FILES TO USE
------------
Use the following project files as evidence/source-of-truth:

1. All_table_scripts.sql
   - DDL for previously explored MercerEdge tables

2. All_Other_tables_Not_explored.sql
   - DDL for additional MercerEdge tables

3. MercerEdge_ML_Churn_Driver_EDA_Phase2.xlsx
   - Data exploration/profile results for previously explored tables

4. MercerEdge_ML_Churn_Driver_EDA_Remaining_Tables_part2.xlsx
   - Data exploration/profile results for the additional tables

5. .env
   - SQL Server connection values

6. sample.py
   - Known working SQL Server connection example

Use the DDL files as the source of truth for physical column names and datatypes.
Use the EDA workbooks to understand nulls, date coverage, candidate churn features, leakage risks, and data quality.

SQL CONNECTION
--------------
Reuse the working SQL Server connection pattern from sample.py.

Use:
- python-dotenv
- pyodbc
- values from .env
- Windows Trusted Connection if that is what sample.py uses
- TrustServerCertificate as required

Do not hardcode credentials.

Use the currently active project Python environment.
Do not create a new environment unless absolutely required.

OBJECTIVE
---------
Create a production-style historical modelling dataset SQL query for churn model development.

The SQL must support configurable dates using explicit parameters such as:

DECLARE @FeatureStartDate DATE = '...';
DECLARE @AsOfDate DATE = '...';
DECLARE @OutcomeStartDate DATE = DATEADD(DAY, 1, @AsOfDate);
DECLARE @OutcomeEndDate DATE = DATEADD(MONTH, 3, @AsOfDate);

Do NOT hardcode feature windows separately inside every feature CTE when @FeatureStartDate can be used.

The query must clearly separate:

1. Base account population
2. Reference/member mapping
3. Account snapshot/profile data
4. Historical feature generation
5. Churn target/outcome generation
6. Eligibility/exclusion rules
7. Final account-level modelling dataset
8. Validation queries

BASE POPULATION
---------------
Use accountSummary as the primary/core account source where appropriate because it contains key profile/history fields.

However:
- Inspect actual table coverage first
- Do not silently lose valid accounts due to joins
- Use LEFT JOIN for feature sources unless business logic requires otherwise
- Keep one row per account_id + as_of_date
- Resolve duplicate/multiple source rows deterministically
- Do not create multiple final rows per account

Member ID/reference:
- Include the best available related member identifier/memberNumber as a reference column
- Use customerMapping or other appropriate mapping if needed
- It is a reference identifier, not a predictive ML feature
- Do not silently discard an account only because member mapping is unavailable; instead flag missing mapping where appropriate

ACCOUNT SUMMARY SNAPSHOT
------------------------
For accountSummary:
- Use the latest valid snapshot on or before @AsOfDate when reportingDate is available
- Do not use accountSummary records dated after @AsOfDate for features
- If reportingDate is NULL, do not fabricate historical timing
- Handle such records explicitly and document the approach
- Add useful quality/availability flags if needed, e.g. has_valid_accountsummary_snapshot
- Do not silently use future information

FEATURE WINDOW
--------------
All predictive features must use data between:

@FeatureStartDate and @AsOfDate

Do not use any event after @AsOfDate as a model input.

Where useful, derive account-level historical features such as:

ACCOUNT / PROFILE
- tenure
- age / age band
- account status
- fund/product attributes
- account balance/FUM fields only if historically valid as of @AsOfDate

CONTRIBUTIONS / MONEY INFLOW
From accountMoneyInflow and related tables:
- contribution_count
- contribution_amount
- average contribution amount
- months/days since last contribution
- contribution frequency
- recent contribution decline where feasible

NET MONEY FLOW
From accountNetMoneyFlow:
- net money flow
- negative net flow flag
- recent vs historical flow trends if supported

ROLLOVER / OUTFLOW
From accountRolloverPayment:
- rollover out count
- rollover out amount
- partial rollover indicators where supported
- days/months since last rollover
- internalTransferFlag
- internal transfer events must not become churn
- do not use outcome-period full exit activity as predictive features

WEB ENGAGEMENT
From accountEngagementWeb:
- web activity count
- recency
- inactivity flags
- only events <= @AsOfDate

HELPLINE / WORKFLOW
From accountEngagementHelpline and accountEngagementWorkflow:
- contact count
- recency
- repeat contact indicators
- useful workflow/engagement features where supported

INVESTMENTS
From accountInvestments:
- investment activity count
- recency
- investment changes
- relevant value/option aggregations where historically valid

INSURANCE
From AccountInsuranceCurrent:
- active insurance indicators
- count/value/premium fields if appropriate and historically valid

CAMPAIGN ENGAGEMENT
From campaignAccountMapping + campaign:
- campaign sends
- email opens
- email clicks
- open/click rates
- campaign engagement recency
- no-engagement flags
- relevant campaign categories if they can be safely derived

CAMPAIGN EVENTS
From campaignEventDetails + campaignEvents:
- derive only SAFE PRE-CHURN behavioural features
- e.g. CONTACT_UPDATE, INVESTMENT_CHANGE, FINANCIAL_ADVICE etc. where appropriate
- clearly separate behavioural events from target/outcome events

IMPORTANT TARGET LEAKAGE RULES
------------------------------
Do NOT use as predictive features:
- MEMBER_EXIT occurring after @AsOfDate
- exitDate from the outcome window
- full rollover completion that represents churn
- account closure outcome
- death outcome
- future reportingDate
- any field/event only known after @AsOfDate
- any direct target indicator

Such fields may be used only for target/outcome construction or exclusion logic.

CHURN TARGET
------------
Build target_churn separately from predictive features.

Suggested logic:

target_churn = 1 when:
- accountSummary.exitDate is > @AsOfDate
- accountSummary.exitDate <= @OutcomeEndDate
- account is NOT an internal transfer
- account is NOT deceased
- any additional qualifying rules must be clearly documented, not assumed

target_churn = 0 when:
- account is eligible at @AsOfDate
- no qualifying churn exit occurs during the outcome window

Exclude / flag:
- dateOfDeath is not null where the death applies to the relevant modelling period
- internalTransferFlag indicates internal transfer
- exitType = 'Internal Transfer'
- any other non-retention exit only if supported by source/business rules

Be very careful not to use exitDate from the outcome window as a feature.

ELIGIBILITY
-----------
Create explicit eligibility/exclusion flags, for example:

- is_eligible_for_modelling
- is_internal_transfer
- is_deceased
- has_valid_account_snapshot
- has_member_mapping
- has_required_history

Do not hide exclusion logic inside joins.

Final eligible modelling dataset should clearly show which rules were applied.

DATE LOGIC
----------
The query must be point-in-time safe.

For every feature source:
- source event date >= @FeatureStartDate
- source event date <= @AsOfDate

For target:
- outcome date > @AsOfDate
- outcome date <= @OutcomeEndDate

Ensure:
- no future feature leakage
- no outcome data mixed into the feature calculations
- no duplicate account_id + as_of_date rows

OUTPUT
------
Create a SQL file named:

build_merceredge_historical_modelling_dataset.sql

The final dataset should contain, where applicable:

Identifiers / metadata:
- account_id
- member_number_ref / member_id
- as_of_date
- feature_start_date
- outcome_start_date
- outcome_end_date

Eligibility/exclusion:
- is_eligible_for_modelling
- is_internal_transfer
- is_deceased
- snapshot/mapping availability flags

Predictive features:
- profile/account features
- contribution features
- net flow features
- rollover features
- engagement features
- investment features
- insurance features
- campaign engagement features
- safe campaign behavioural event features

Target:
- target_churn

Do not include raw future/outcome columns as predictive fields.

VALIDATION
----------
After creating the SQL, validate it against the actual MercerEdge SQL Server using the .env connection and sample.py connection approach.

Do not write/update/delete source data.
Read-only validation only.

Perform:

1. SQL compile/syntax validation
2. Referenced table existence validation
3. Referenced column existence validation
4. Execute with a limited/test date range if needed
5. Check final row count
6. Check distinct account_id + as_of_date count
7. Check duplicate account_id + as_of_date count
8. Check NULL account_id
9. Check NULL as_of_date
10. Check target_churn distribution
11. Check eligible vs excluded population
12. Count internal-transfer exclusions
13. Count death exclusions
14. Check feature date leakage:
    prove no feature record after @AsOfDate was used
15. Check target window:
    prove target events are strictly after @AsOfDate and within @OutcomeEndDate
16. Check major feature NULL rates
17. Check account/member mapping coverage
18. Check join row multiplication
19. Check table/date coverage for each major feature block

Also include targeted validation for:
- exitDate churn logic
- dateOfDeath death exclusion
- accountRolloverPayment.internalTransferFlag
- accountSummary.exitType = 'Internal Transfer'

IMPORTANT
---------
Before writing the final SQL:
1. Inspect the DDLs
2. Inspect the EDA workbooks
3. Verify actual physical table/column names
4. Do not invent fields
5. If a requested business field does not exist, clearly report it rather than creating a fake mapping
6. If two sources conflict, document the issue and use the most defensible source only after explaining why

Do not blindly use every column from the 18 tables.

Use only:
- identifiers/join fields needed for integration
- historically valid predictive features
- target-support fields
- eligibility/exclusion fields

FINAL RESPONSE
--------------
When complete, provide:

1. Generated SQL file name/path
2. Feature groups included
3. Tables actually used and their purpose
4. Churn target logic used
5. Internal transfer exclusion logic
6. Death exclusion logic
7. Any assumptions / unresolved business questions
8. Validation results
9. Any leakage risks identified
10. Any source/data-quality issues that could affect modelling

Do not declare completion unless the SQL compiles successfully against the actual MercerEdge database and the validation checks have been executed.
