Yes. Your query is creating 8 temporary tables, each with one clear job. Think of it as progressively cleaning and narrowing the data until you get the final base modelling dataset.

1. #account_universe — Starting population

Source: mainly accountSummary.

Purpose: create the master list of accounts and basic reference fields such as account/member/customer IDs, fundJoinDate, DOB, gender, exitDate, exitType, death fields, etc.

Main filter:

accountID IS NOT NULL

Layman meaning: “Start with every valid account we know about.”

Important: no historical snapshot logic is used here.



2. #pensioner_reference — Additional pension/death information

Source: pensionerData.

Purpose: bring in clientCommencementDate, clientEarliestCommencementDate, deceasedDate, death indicator.

Main filter:

accountID IS NOT NULL

Layman meaning: “If accountSummary doesn't have enough commencement/death information, use pensionerData as supporting information.”

It is not treated as a complete historical snapshot.



3. #historical_eligibility — Was this account valid at the AsOfDate?

Combines #account_universe + #pensioner_reference.

Determines a commencement_date_used, generally preferring:

fundJoinDate
→ clientCommencementDate
→ clientEarliestCommencementDate

Main rules are roughly:

commencement_date_used <= @AsOfDate
exitDate IS NULL OR exitDate > @AsOfDate
not deceased on/before @AsOfDate

Creates:

existed_by_asof_flag

exited_on_or_before_asof_flag

death_exclusion_asof_flag

is_eligible_for_modelling

historical_eligibility_status


Layman meaning: “Was this person/account actually active and eligible when we pretend we are standing on the AsOfDate?”



4. #customer_mapping_reference — Find useful member/customer IDs

Source: customerMapping.

Used for customer ID, member number, Salesforce IDs, policy number, etc.

Main filter:

accountID IS NOT NULL
AND accurateDate <= @AsOfDate

Layman meaning: “Use the best available mapping known by the cutoff date to enrich the account with IDs.”

Very important: if mapping is missing, the account is not automatically excluded.



5. #third_party_authority_reference — Historical authority status support

Source: thirdPartyAuthority.

Main filters:

dateAuthorityRequested <= @AsOfDate

and termination date must be:

NULL/open-ended
OR > @AsOfDate

Sentinel future dates like 3999-12-13 are normalized.

Layman meaning: “Was a third-party authority active for this account at the cutoff date?”

Currently this is staged for later use; it does not appear to drive your final base population yet.



6. #internal_transfer_outcome — Identify non-churn internal transfers

Source: accountRolloverPayment.

Looks only in the future outcome window:

dateOfPayment > @AsOfDate
AND dateOfPayment <= @OutcomeEndDate

Then checks:

internalTransferFlag = 1

Layman meaning: “If the account leaves during the outcome period because it was only an internal transfer, don't call that churn.”



7. #future_churn_outcome — Create the churn target

Starts from the eligible historical population.

Future exit condition:

exitDate > @AsOfDate
AND exitDate <= @OutcomeEndDate

Then excludes:

internal transfers

death-related exits


Creates:

future_exit_in_outcome_window_flag
internal_transfer_exclusion_flag
death_exclusion_outcome_flag
target_churn

Conceptually:

eligible + future valid exit = target_churn 1
eligible + no valid future exit = target_churn 0
not eligible = NULL

Layman meaning: “Look forward three months and determine whether this account actually churned.”



8. #base_historical_dataset — Final modelling base row

Joins the previous outputs together.

Keeps one row per:

account_id + as_of_date

Includes IDs, modelling dates, eligibility flags, exclusion flags and target_churn.

Final fields include things like:

account_id
as_of_date
feature_start_date
outcome_start_date
outcome_end_date
fund_join_date
exit_date
internal_transfer_exclusion_flag
death_exclusion_flag
is_eligible_for_modelling
target_churn
retained_flag
historical_eligibility_status

Layman meaning: “This is the clean base row that will later receive engineered ML features.”




The easiest way to remember the whole flow is:

All accounts
   ↓
Add pension/death support
   ↓
Check who was eligible at AsOfDate
   ↓
Add reference IDs
   ↓
Check internal-transfer outcome
   ↓
Check future exit/death outcome
   ↓
Create target_churn
   ↓
Final base historical dataset

One important point: FeatureStartDate is mostly just carried in this base dataset right now. The behavioural tables such as money inflow, net money flow, workflow, campaign events, etc. will actually use:

event_date >= @FeatureStartDate
AND event_date <= @AsOfDate

in your next feature-engineering step.
