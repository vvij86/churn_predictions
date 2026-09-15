For this task — “Define Churn target, eligibility, dates and modelling rules” — your job is to lock down the rules before you create target_churn and train the model.

For your retention project, I would complete these items:

1. Define the modelling grain

One row per account_id per as_of_date

memberNumber only as a reference field, not a model feature.



2. Define exactly what counts as churn For example:

Full rollover out → churn?

Full withdrawal / account exit → churn?

Account closure → churn?

Partial rollover/withdrawal → probably not churn, but can be a risk feature.

Death exit → exclude from churn population rather than label as churn.


This needs business/SME confirmation.


3. Define target_churn Something like:

target_churn = 1 → account experiences a qualifying churn event during the outcome window.

target_churn = 0 → account remains retained throughout the outcome window.



4. Define the three important dates/windows

Example:

Feature Start Date : 2025-01-01
As-Of Date         : 2025-12-31
Outcome Start      : 2026-01-01
Outcome End        : 2026-03-31

Meaning:

Jan 2025 ---------------- Dec 2025 | Jan-Mar 2026
     Feature window                 Outcome window
                           ^
                        As-of date

Features must only use information available on or before the as-of date.


5. Define account eligibility Decide which accounts are allowed into the modelling population.

Questions to confirm:

Must account exist/be active at as_of_date?

Minimum tenure required?

Accounts opened very close to as_of_date included or excluded?

Accounts already exited before as_of_date excluded?

Death exits excluded?

What to do when AccountSummary is unavailable?

Do we require minimum observable history?


This is especially important given what you found: many accounts exist in ACCOUNT but have little/no AccountSummary information.


6. Define leakage rules Explicitly document that information occurring after as_of_date cannot be used as features.

For example, these may be target-support fields but not ML features:

final exit status

exit date

full rollover completion

post-exit status

account balance at exit



7. Define historical feature period You already identified this issue in your SQL. Decide whether the feature window is:

fixed 12 months, or

explicit feature_start_date → as_of_date.


I recommend documenting both parameters explicitly.


8. Produce a short rules document/table Your output for this ADO task could be something like:



Rule	Agreed definition

Grain	Account + As-of date
Churn = 1	Qualifying full exit within outcome window
Retained = 0	No qualifying exit within outcome window
Partial withdrawal	Risk feature, not churn
Death exit	Excluded
Feature window	12 months before as-of date
Outcome window	3 months after as-of date
Existing exits before as-of	Excluded
Future information	Prohibited from features
Member number	Reference only


The most important part of this task is not writing code yet. First get agreement from your lead/BA/SME on the churn event and eligibility rules. Then you can implement the target logic in SQL.

Your next practical action should be to prepare the questions for David/Sai/Taj and get these rules confirmed. After that, the following task can be the SQL implementation of target_churn.
