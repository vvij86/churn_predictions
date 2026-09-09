I am now starting Phase 3 of ML-focused churn feature engineering.

Phase 1 and Phase 2 are already complete.

Use the existing Phase 2 workbook as the authoritative input:

MercerEdge_ML_Churn_Driver_EDA_Phase2.xlsx

Do NOT rebuild Phase 1 or Phase 2.

The goal of Phase 3 is to convert technically usable raw source columns into a clear set of account-level ML features for churn modelling.

Critical modelling grain

The modelling grain is:

one row per account_id per as_of_date

This must be enforced throughout Phase 3.

Also retain the related member_id/member_number needed for traceability and downstream reporting.

Important:

account_id is the modelling grain key.

member_id/member_number is a related identifier and should be retained as a non-predictive reference/output field.

Do NOT use member_id/member_number as an ML feature.

If one account can map to multiple member IDs, do not duplicate the modelling grain. Resolve the mapping safely or flag it for investigation.

Final output must still have only one row per account_id + as_of_date.


Do NOT create transaction-level, event-level, customer-level, member-level, or other lower-grain model records.

If the source data is transaction-level or event-level, aggregate it to account level before creating ML features.

Phase 3 objective

For all Phase 2 columns classified as:

Confirmed Candidate

Candidate with Transformation

Investigate Further where business logic is sufficiently clear


design meaningful account-level features for churn prediction.

Do not automatically create one ML feature per raw column.

Use business/ML reasoning to determine whether a raw field should:

be used directly

be transformed

be aggregated

be converted to a flag/category

be excluded

be retained only as a join/reference key


Time-aware feature engineering

All features must be calculated using data available on or before the prediction as_of_date.

Do not use future information.

For behavioural/transactional features, prefer historical windows such as:

1 month

3 months

6 months

12 months


where appropriate.

Do not create all windows mechanically for every field.

Choose windows based on the business meaning of the source data.

Feature engineering patterns

Consider features such as:

Contributions / money inflow

Examples:

contribution_count_3m

contribution_count_6m

contribution_count_12m

contribution_amount_3m

contribution_amount_6m

contribution_amount_12m

avg_contribution_amount_12m

months_since_last_contribution

contribution_frequency_12m

contribution_amount_change_3m_vs_prior_3m

contribution_amount_change_6m_vs_prior_6m

no_contribution_last_3m_flag


Rollovers / withdrawals / money outflow

Examples:

rollover_out_count_12m

rollover_out_amount_12m

partial_withdrawal_count_12m

partial_withdrawal_amount_12m

months_since_last_rollover_out

months_since_last_withdrawal

rollover_out_to_balance_ratio

withdrawal_to_balance_ratio


Any feature related to closure, full exit, final withdrawal, or completed churn must be carefully checked for leakage.

Net money flow

Examples:

net_money_flow_3m

net_money_flow_6m

net_money_flow_12m

avg_monthly_net_flow_12m

negative_net_flow_months_12m

net_flow_trend

negative_net_flow_flag


Web engagement

Examples:

web_activity_count_1m

web_activity_count_3m

web_activity_count_6m

days_since_last_web_activity

active_web_months_12m

no_web_activity_3m_flag


Helpline engagement

Examples:

helpline_contact_count_3m

helpline_contact_count_6m

helpline_contact_count_12m

days_since_last_helpline_contact

repeat_helpline_contact_flag


Investments

Examples:

investment_option_count

investment_switch_count_12m

investment_balance

investment_diversification_count

investment_change_flag

investment_activity_recency


Only create these if supported by the available raw data.

Insurance

Examples:

has_insurance_flag

active_insurance_count

annual_premium

total_annual_premium

insurance_cover_type_count

insurance_status_category


Account / lifecycle

Examples:

tenure_months

account_age_years

months_since_account_open

active_account_flag


Do not use post-exit information.

Demographics / customer attributes

Examples:

age

age_band

state / region category

contactability flags

communication preference flags


Do not use raw PII such as name, email address, phone number, street address, or external IDs as ML features.

Account/member mapping rule

Retain the related member identifier in the final output where a valid relationship exists.

Use the actual source column name found in Phase 2, such as:

memberID

memberNumber

or the equivalent field present in the source tables


Do not invent a member identifier name if the actual field differs.

Document:

source table

source member identifier column

account-to-member mapping logic

whether the relationship is one-to-one, one-to-many, or unclear


If the relationship is one-to-many:

do not duplicate account-level rows

do not arbitrarily pick a member ID

flag the mapping as requiring business validation

use a safe deterministic rule only if supported by the source/business definition


The member identifier must appear in the final feature dataset as a reference column only, not as a predictive ML feature.

Account-level aggregation rule

For every proposed feature, document exactly how lower-grain data is aggregated to account level.

Examples:

contribution_amount_12m

= SUM of contribution amount for the account where transaction date is greater than as_of_date - 12 months and less than or equal to as_of_date.

web_activity_count_3m

= COUNT of web activity records for the account in the 3 months up to as_of_date.

months_since_last_contribution

= difference between as_of_date and the latest contribution date on or before as_of_date.

Required Phase 3 output

Create a new workbook:

MercerEdge_ML_Churn_Feature_Engineering_Phase3.xlsx

Do not overwrite Phase 1 or Phase 2 workbooks.

Create these worksheets:

1. Feature_Catalog


2. Source_Coverage


3. Account_Member_Mapping


4. Leakage_Review


5. Validation



Feature_Catalog worksheet

Create one row per engineered ML feature.

Include:

Feature ID

Feature Name

Feature Group

Business Definition

Source Table

Source Column(s)

Source Grain

Target Grain

Transformation Type

Aggregation Window

Calculation Logic

SQL Logic / Pseudocode

Expected Data Type

Null Handling

Leakage Risk

As-of-Date Rule

Phase 2 Source Usability

Include for Modelling

Reason

Business Validation Needed

Notes


Target Grain must always be:

Account + AsOfDate

Do not treat member_id/member_number as an ML feature. It is an output/reference identifier.

Source_Coverage worksheet

For every Phase 2 raw source column, show whether it is:

used directly

used in an engineered feature

join/reference key only

excluded

requires investigation


Include:

Source Table

Source Column

Phase 2 Usability

Phase 3 Usage

Related Feature Name(s)

Reason


This is important so that no Phase 2 candidate disappears without explanation.

Account_Member_Mapping worksheet

Create a dedicated mapping review containing:

Account ID Column

Member ID / Member Number Column

Source Table

Mapping Join Logic

Relationship Type

One Account to One Member?

One Account to Multiple Members?

Mapping Data Quality Issue

Recommended Rule

Business Validation Needed

Notes


The purpose is to ensure member_id/member_number can be retained without breaking the account-level grain.

Leakage_Review worksheet

Create a dedicated review of features with possible timing leakage.

Include:

Feature Name

Source Table

Source Column(s)

Leakage Risk

Why Risk Exists

Available Before AsOfDate?

Requires Business Confirmation?

Final Recommendation


Pay particular attention to:

exit status

closure status

cancellation

final withdrawal

full rollover out

account balance at exit

post-exit fields

termination date

outcome-related statuses


Do not include a feature for modelling if it is only known after the prediction point.

Do not create target yet

Do NOT create or derive target_churn in Phase 3.

Phase 3 is feature engineering only.

Target definition and outcome-window logic will be handled separately after feature engineering.

Mandatory SQL output

In addition to the Phase 3 Excel workbook, create a separate SQL file:

build_account_level_features.sql

This SQL file must implement the proposed Phase 3 engineered features as far as possible using the actual source tables and columns identified in Phase 2.

The required final grain of this SQL output is:

one row per account_id per as_of_date

Also retain the related member identifier as a reference/output column where valid.

Conceptually, the final output should look like:

account_id
member_id_or_member_number
as_of_date
tenure_months
contribution_count_12m
contribution_amount_12m
months_since_last_contribution
web_activity_count_3m
helpline_contact_count_6m
rollover_out_amount_12m
net_money_flow_12m
...

Do not use member ID/member number as an ML feature.

The SQL must not create duplicate account records for the same as_of_date.

Use CTEs or clearly separated logical sections for feature groups such as:

base account/member mapping

account / lifecycle

contributions / money inflow

rollovers / withdrawals

net money flow

web engagement

helpline engagement

investments

insurance

demographics / customer attributes


For lower-grain transaction or event tables, aggregate to account_id before joining to the final account-level dataset.

As-of-date filtering

All time-based features must use only records available on or before as_of_date.

Examples:

transaction_date <= as_of_date

and for a 12-month feature window:

transaction_date > DATEADD(MONTH, -12, as_of_date)
AND transaction_date <= as_of_date

Do not include future records.

SQL implementation rules

Do not use placeholder table or column names if actual names are available in the Phase 2 workbook or DDL.

Use the exact source tables and columns.

If a proposed feature cannot yet be implemented because the business definition, date column, account mapping, or aggregation logic is unclear:

do not invent SQL

add a clearly marked comment such as:


-- TODO: Business definition required before implementation

and document the same issue in the Phase 3 Feature Catalog.

Feature-selection rules

Do not create predictive features from:

raw IDs

account IDs

member IDs/member numbers

names

raw emails

raw phone numbers

raw addresses

ETL metadata

load timestamps

technical audit fields

100% null columns

constant columns

obvious post-churn fields


unless there is a clear derived business feature that is valid before as_of_date.

For example:

raw email address -> do not use

but:

has_valid_email_flag -> potentially usable

Avoid feature explosion

Do not generate hundreds of repetitive features automatically.

Prefer a smaller, explainable feature set.

Only create multiple 3/6/12 month windows where they are genuinely meaningful.

If several raw columns represent the same business concept, consolidate them where appropriate.

Feature naming

Use consistent snake_case names.

Examples:

tenure_months

contribution_amount_12m

contribution_count_12m

days_since_last_web_activity

rollover_out_amount_12m

net_money_flow_6m


Names should clearly indicate:

business meaning

aggregation

time window where applicable


SQL validation

At the end of build_account_level_features.sql, include validation SQL for:

1. total row count


2. distinct account count


3. distinct member count where member identifier is available


4. duplicate account_id + as_of_date combinations


5. null account_id


6. null as_of_date


7. null member identifier count


8. accounts mapping to multiple member IDs


9. feature null counts for major engineered features



The duplicate account validation must return zero duplicate combinations.

Also explicitly check:

COUNT(*) vs COUNT(DISTINCT account_id + as_of_date)

using a SQL Server-compatible implementation.

Workbook validation

Before considering Phase 3 complete, validate:

1. Every proposed feature has a documented source table and source column.


2. Every feature produces account-level values.


3. Target grain is always Account + AsOfDate.


4. No feature uses data after as_of_date.


5. Every Phase 2 Confirmed Candidate is either:

used

transformed

excluded with reason



6. Every Phase 2 Candidate with Transformation has a documented transformation or exclusion reason.


7. Join/reference keys are not used as predictive features.


8. member_id/member_number is retained only as a reference/output field.


9. PII is not used directly.


10. Leakage-risk features are clearly documented.


11. No duplicate feature names exist.


12. SQL logic references valid Phase 2 tables and columns.


13. Account/member mapping does not create duplicate account-level rows.


14. All generated features can be traced back to Phase 2 source columns.



Final summary

At the end print:

number of Phase 2 source columns reviewed

number of engineered features proposed

number of direct features

number of aggregated features

number of transformed features

number of excluded source columns

number of features requiring business validation

number of leakage-risk features

account/member mapping status

duplicate account + as_of_date count

output workbook path

SQL file path


Do not consider Phase 3 complete unless both outputs are generated:

MercerEdge_ML_Churn_Feature_Engineering_Phase3.xlsx

build_account_level_features.sql


and all features are designed at account_id + as_of_date grain, with the related member_id/member_number retained only as a reference/output identifier.
