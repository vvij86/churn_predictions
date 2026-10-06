Please revise the currently open SQL file:

build_merceredge_base_historical_dataset.sql

I have identified an important issue in edgeSource.accountSummary:

For exited accounts, reportingDate is effectively updated to the exit date, and in many/all observed cases:

reportingDate = exitDate

Because of this, the current logic must carefully separate:

1. historical feature/base snapshot selection
2. future churn outcome detection

Do NOT use a future exit row as the historical snapshot.

IMPORTANT MODELLING RULE
------------------------
The model as_of_date must remain the fixed parameter:

@AsOfDate

For example:

DECLARE @AsOfDate DATE = '2025-03-31';

Do NOT derive as_of_date from:

- reportingDate
- exitDate
- exitDateRecorded
- any transaction/event date

The final output must use:

@AsOfDate AS as_of_date

ACCOUNT SUMMARY HISTORICAL SNAPSHOT
-----------------------------------
For the historical/base snapshot:

Use accountSummary.reportingDate only to identify the latest record that was available on or before @AsOfDate.

Conceptually:

reportingDate <= @AsOfDate

Then select the latest record per accountID.

Example:

ROW_NUMBER() OVER (
    PARTITION BY accountID
    ORDER BY reportingDate DESC
)

Keep rn = 1.

This snapshot is the information available at prediction time.

VERY IMPORTANT:
If an account exits after @AsOfDate and its accountSummary row has:

reportingDate = exitDate

that future row must NOT be included in the historical snapshot because its reportingDate is after @AsOfDate.

FUTURE CHURN OUTCOME
--------------------
Create a SEPARATE outcome lookup from accountSummary.

Do NOT rely on exitDate from the historical snapshot row to create target_churn.

Instead, independently search accountSummary for future qualifying exits where:

exitDate > @AsOfDate
AND exitDate <= @OutcomeEndDate

Create a separate CTE/temp table such as:

#future_exit_outcome

or a CTE called:

future_exit_outcome

Suggested structure:

SELECT
    accountID,
    MIN(exitDate) AS qualifying_exit_date
FROM edgeSource.accountSummary
WHERE exitDate > @AsOfDate
  AND exitDate <= @OutcomeEndDate
GROUP BY accountID

Then join this future outcome result back to the historical base population using accountID.

TARGET LOGIC
------------
Create target_churn only after the historical snapshot and future outcome are separated.

Conceptually:

CASE
    WHEN is_eligible_for_modelling = 0 THEN NULL
    WHEN qualifying_exit_date IS NOT NULL
         AND is_internal_transfer = 0
         AND is_deceased = 0
    THEN 1
    ELSE 0
END AS target_churn

Important:

- reportingDate is for historical snapshot selection
- exitDate is for future churn outcome detection
- @AsOfDate is the modelling cutoff
- these three must not be treated as interchangeable dates

INTERNAL TRANSFER LOGIC
-----------------------
Internal transfer must still be excluded from churn.

Use:

Primary:
edgeSource.accountRolloverPayment.internalTransferFlag

Supporting:
edgeSource.accountSummary.exitType = 'Internal Transfer'

IMPORTANT:
Internal-transfer outcome checks must also respect the outcome window and must not introduce future data into historical feature fields.

DEATH LOGIC
-----------
Death must remain excluded from churn.

Use accountSummary.dateOfDeath according to the agreed business rule.

If death occurs in the future outcome period, it can be used for exclusion/target determination but must not become a predictive feature.

ELIGIBILITY
-----------
An account should be eligible at @AsOfDate only if it was part of the valid modelling population at that point.

Please review the logic for accounts where:

exitDate = @AsOfDate

Do not automatically treat these as retained.

Preferred rule unless contradicted by existing business logic:

eligible at as_of_date when:
exitDate IS NULL
OR exitDate > @AsOfDate

If exitDate = @AsOfDate, flag/exclude the account from that snapshot because it has already exited on the prediction cutoff date.

However, verify this against the actual available source records and clearly document the assumption.

CURRENT KNOWN ISSUE TO FIX
--------------------------
Example:

@AsOfDate = '2025-03-31'

Account future row:

reportingDate = '2025-05-15'
exitDate      = '2025-05-15'

Correct behaviour:

Historical snapshot:
- do NOT use the 15-May-2025 accountSummary row
- use the latest valid accountSummary row with reportingDate <= 31-Mar-2025

Future outcome:
- detect exitDate = 15-May-2025
- since it falls between 01-Apr-2025 and 30-Jun-2025, target_churn should become 1
  unless internal transfer/death exclusion applies

Do NOT lose this churn event just because the future row was excluded from the historical snapshot.

KEEP BASE DATASET SCOPE ONLY
----------------------------
Do NOT start feature engineering.

Do NOT add behavioural aggregates such as:

- contribution_count_12m
- rollover_count_12m
- web_activity_count
- campaign_open_rate
- days_since_last_*
- trend features
- recency features
- transaction aggregates

This SQL must remain the BASE HISTORICAL MODELLING DATASET only.

REVIEW CURRENT SQL STRUCTURE
----------------------------
Please inspect and revise the existing logic around:

- #account_summary_latest
- #account_summary_snapshot
- #base_historical_population
- #internal_transfer_outcome
- #base_historical_dataset

Add a clearly separated future outcome CTE/temp table if it does not already exist.

Do not unnecessarily rewrite unrelated working logic.

VALIDATION
----------
After modifying the query, add validation queries for the following:

1. Count of historical account snapshots
2. Count of future qualifying exits
3. Count where reportingDate = exitDate
4. Count of churn target = 1
5. Count of retained target = 0
6. Count of target_churn IS NULL
7. Count of eligible rows where target_churn IS NULL
8. Count of exitDate = @AsOfDate cases
9. Count of future exits correctly matched back to a historical snapshot
10. Count of future exits that have no historical snapshot
11. Count of internal transfers excluded
12. Count of deceased accounts excluded

Also provide sample rows for validation containing:

accountID
historical_reporting_date
@AsOfDate as as_of_date
qualifying_exit_date
exitType
is_internal_transfer
is_deceased
is_eligible_for_modelling
target_churn

Specifically show examples where:

A. reportingDate < @AsOfDate and exitDate is in the future outcome window
B. reportingDate = exitDate and both are after @AsOfDate
C. exitDate = @AsOfDate
D. internal transfer in outcome window
E. deceased account

EXPECTED DESIGN AFTER REVISION
------------------------------
The logic should clearly look like:

STEP 1:
Define @FeatureStartDate, @AsOfDate, @OutcomeStartDate, @OutcomeEndDate

STEP 2:
Build historical accountSummary snapshot using:

reportingDate <= @AsOfDate

STEP 3:
Build future churn outcome separately using:

exitDate > @AsOfDate
AND exitDate <= @OutcomeEndDate

STEP 4:
Build internal-transfer/death exclusion logic

STEP 5:
Join future outcome back to historical population

STEP 6:
Create is_eligible_for_modelling and target_churn

STEP 7:
Return final one-row-per-accountID + as_of_date dataset

FINAL GRAIN
-----------
One row per:

account_id + as_of_date

Do not allow the future outcome row to change the historical snapshot.

At the end, explain briefly:

1. what was wrong/risky in the previous date logic
2. how reportingDate is now used
3. how exitDate is now used
4. why future exit rows are separated from historical snapshots
5. how target_churn is now created
6. how exitDate = reportingDate cases are handled
7. whether any unresolved business rule remains
