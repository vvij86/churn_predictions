Please update the current:

build_merceredge_base_historical_dataset.sql

Business has now confirmed that:

edgePortalSource.pensionerData

is NOT required for the tactical churn model.

Please remove all logic that depends on pensionerData from this base historical dataset query.

IMPORTANT:
Do not redesign unrelated working logic.
Do not start feature engineering.
Only remove pensionerData-related logic and simplify the affected sections safely.

Specifically remove:

1. #pensioner_reference temp table
2. Reads from:
   edgePortalSource.pensionerData
3. clientCommencementDate
4. clientEarliestCommencementDate
5. deceasedDate
6. pensioner deathIndicatorFlag
7. pensioner_death_indicator_flag
8. Any fallback logic that uses pensionerData for commencement date
9. Any fallback death logic that uses pensionerData
10. Any joins to #pensioner_reference
11. Any comments/documentation saying pensionerData is used for commencement/death support
12. Any validation queries specifically related to pensionerData

After removing pensionerData, use accountSummary as the source for the remaining relevant account-level fields.

For commencement / existence logic:
- use accountSummary.fundJoinDate where available
- do not invent another fallback date unless it is already validated elsewhere
- if fundJoinDate is NULL, preserve the existing conservative eligibility behavior unless business rules require otherwise

For death logic:
- use accountSummary.dateOfDeath
- use accountSummary.deathIndicatorFlag if available
- remove all dependence on pensionerData.deceasedDate and pensionerData.deathIndicatorFlag

Review and simplify:

- #historical_eligibility
- commencement_date_used
- normalized_date_of_death
- death_exclusion_asof_flag
- death_exclusion_outcome_flag
- death_exclusion_flag
- is_eligible_for_modelling
- historical_eligibility_status

Make sure target_churn logic still works correctly after the removal.

Keep these core rules unchanged:

- @AsOfDate remains manually supplied
- fundJoinDate is only used for existence/eligibility
- exitDate is used for future churn outcome
- internal transfers remain non-churn/excluded from positive churn
- death remains excluded from churn
- one row per account_id + as_of_date
- no reportingDate snapshot logic
- no customerSummary current-state features
- no feature engineering yet

After the change, run/read-only validate the query and report:

1. total account universe
2. eligible accounts
3. retained count
4. churn count
5. target NULL count
6. death exclusions
7. internal-transfer exclusions
8. duplicate account_id + as_of_date count
9. NULL account_id count
10. confirm there are no remaining references to pensionerData anywhere in the SQL

Also briefly summarize:
- what pensionerData logic was removed
- what now replaces the commencement/death fallback logic
- whether row counts changed materially after removal

Do not modify any other project files unless required for validation.
