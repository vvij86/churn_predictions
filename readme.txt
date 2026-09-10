Please update the existing Phase 3 SQL in build_account_level_features.sql to fix both the member-number resolution issue and the feature-window parameterization.

Do not rebuild the entire Phase 3 solution from scratch. Update the existing SQL in place.

Critical modelling grain

The final modelling grain must remain:

one row per account_id + as_of_date

Do not allow any join or mapping logic to create duplicate rows for the same account_id + as_of_date.

member_number_ref must remain a reference/output identifier only and must not be used as a predictive ML feature.

Explicit feature window parameters

Add explicit configurable parameters:

DECLARE @feature_start_date DATE = '2025-01-01';
DECLARE @as_of_date DATE = '2025-12-31';

Use these parameters consistently throughout all time-based feature engineering logic.

For applicable dated source records, use:

source_date >= @feature_start_date
AND source_date <= @as_of_date

Apply this consistently to:

contributions / money inflow

rollovers / withdrawals

net money flow

web engagement

helpline engagement

investments

insurance where date-based

any other behavioural or transaction-based source with a relevant date


Do not use records before @feature_start_date.

Do not use records after @as_of_date.

Do not rely only on DATEADD(MONTH, -12, @as_of_date) when an explicit @feature_start_date is now available.

For recency features such as:

months_since_last_contribution

days_since_last_web_activity

days_since_last_helpline_contact

months_since_last_rollover_out


use the latest eligible event within the defined feature window unless there is a clearly documented reason to use a longer historical period.

Base account universe

Use edgeSource.account as the primary base account source where possible because it contains:

accountId

fundId

memberNumber


Do not rely on accountSummary to decide whether an account should exist in the final dataset.

All valid accounts should remain in the modelling universe even if:

accountSummary.reportingDate is NULL

there is no valid accountSummary snapshot on or before @as_of_date


Do NOT reintroduce:

WHERE has_valid_accountsummary_snapshot = 1

The final dataset must not drop an account only because a valid AccountSummary snapshot is unavailable.

For such accounts:

retain account_id

retain as_of_date

retain member_number_ref where resolvable

keep AccountSummary-derived features NULL where no valid historical snapshot is available

keep diagnostic flags showing snapshot availability


Member number problem

After removing the final has_valid_accountsummary_snapshot = 1 filter, many rows have:

member_number_ref = NULL

Please fix this using a robust member-number resolution strategy.

Potential member-number sources include:

edgeSource.customerMapping

edgeSource.accountSummary

edgeSource.account


Use the actual column names available in the existing SQL / Phase 2 workbook.

Member-number resolution priority

For each account_id, resolve member_number_ref in this order:

1. Prefer a valid member number from customerMapping that is valid on or before @as_of_date.


2. Otherwise use accountSummary.memberNumber from the selected valid historical snapshot on or before @as_of_date.


3. Otherwise fall back to edgeSource.account.memberNumber.


4. If still unavailable, leave member_number_ref as NULL and flag it for investigation.



Do not arbitrarily choose a member number when multiple conflicting values exist.

Use deterministic ranking based on valid date/order fields where available.

CustomerMapping date rule

If customerMapping contains an effective/accrual/mapping date such as accurateDate, only use records valid on or before @as_of_date.

Prefer the latest valid mapping on or before @as_of_date.

If the relevant mapping date is NULL:

do not automatically treat it as historically valid

use it only if business logic clearly supports that interpretation

otherwise fall back to another source and flag the ambiguity


AccountSummary snapshot rule

For AccountSummary attributes:

select the latest row where reportingDate <= @as_of_date

do not use reportingDate > @as_of_date

do not automatically use a NULL reportingDate row as a historical snapshot


If no valid dated AccountSummary snapshot exists:

keep the account

set AccountSummary-derived fields to NULL

set has_valid_accountsummary_snapshot = 0


Member-number traceability fields

Add these non-predictive diagnostic/reference fields to the final dataset:

member_number_ref

member_number_source

member_number_conflict_flag


Populate member_number_source with values such as:

CustomerMapping

AccountSummary

Account

Unavailable


Set:

member_number_conflict_flag = 1

when multiple non-null sources provide different member numbers for the same account.

Otherwise set it to 0.

Do not use:

member_number_ref

member_number_source

member_number_conflict_flag


as predictive ML features.

They are for traceability and validation only.

Conflict handling

If one account maps to multiple distinct member numbers:

do not duplicate the account row

preserve one row per account_id + as_of_date

use a deterministic valid mapping rule only where supported by dates/business logic

otherwise flag the conflict

do not silently pick an arbitrary value


Final dataset requirements

The final #account_level_features dataset must include:

account_id

member_number_ref

member_number_source

member_number_conflict_flag

as_of_date

has_valid_accountsummary_snapshot

has_null_reportingdate_record

account_summary_reporting_date

all valid engineered account-level features


Do not add target_churn yet.

Time-window validation

Add validation SQL to confirm:

1. @feature_start_date


2. @as_of_date


3. feature-window duration


4. no eligible feature record is earlier than @feature_start_date


5. no eligible feature record is later than @as_of_date



For each major dated feature block, add a concise validation count showing how many source records were included within the feature window.

Account coverage validation

Add validation SQL showing:

1. total distinct accounts in edgeSource.account


2. total distinct accounts in the base account universe


3. total distinct accounts in the final feature dataset


4. accounts missing from the final feature dataset


5. duplicate account_id + as_of_date combinations


6. null account_id


7. null as_of_date



The duplicate count must be zero.

Member-number validation

Also report:

1. total final accounts


2. accounts with non-null member_number_ref


3. accounts with null member_number_ref


4. member numbers resolved from CustomerMapping


5. member numbers resolved from AccountSummary


6. member numbers resolved from Account


7. unresolved member numbers


8. accounts with conflicting member numbers across sources


9. accounts mapping to multiple distinct member numbers


10. sample unresolved account IDs


11. sample conflicting account IDs



AccountSummary coverage validation

Also report:

1. accounts with a valid AccountSummary snapshot on or before @as_of_date


2. accounts without a valid AccountSummary snapshot


3. accounts having NULL reportingDate


4. accounts having only future AccountSummary records relative to @as_of_date



Do not exclude these accounts from the final dataset solely because AccountSummary coverage is unavailable.

Important ML rules

Do not use:

account_id

member_number_ref

raw IDs

raw PII


as predictive features.

Keep all feature calculations account-level.

Do not use future information.

Do not add target_churn yet.

Final check

After updating the SQL, run the validation and print a summary containing:

feature_start_date

as_of_date

base account count

final account count

duplicate account + as_of_date count

member numbers resolved from each source

unresolved member count

member conflict count

valid AccountSummary snapshot count

accounts without valid AccountSummary snapshot

final SQL status


Do not consider the correction complete until:

all valid accounts are retained

member_number_ref is resolved as fully as possible without arbitrary mapping

no duplicate account_id + as_of_date rows exist

all time-based features respect @feature_start_date and @as_of_date

no target_churn column is added.
