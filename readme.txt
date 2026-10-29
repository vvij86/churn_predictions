Review the complete file:

"behavioural_features_business_review.sql"

The file currently contains standalone SQL queries for approximately 133 behavioural features identified for the Member Retention ML solution.

I want to reduce the feature set by removing clear duplicates, mathematically redundant features, weak analysis-only fields, and unnecessary overlapping features, while retaining strong behavioural signals for ML training.

Do not rebuild the SQL from scratch. Review and modify the existing queries in "behavioural_features_business_review.sql".

Important Rules

1. Use the current "behavioural_features_business_review.sql" as the source of truth.
2. Do not restore older features that have already been removed.
3. Preserve all already validated business mappings and filters.
4. Each standalone query must remain independently runnable.
5. Do not change approved source mappings unless required to remove a redundant feature.
6. Use "exitDateRecorded", not "exitDate".
7. Preserve:
   - "fundJoinDate <= @AsOfDate"
   - approved "databaseCode" / FundScope filtering
   - death exclusions
   - internal-transfer exclusions
   - point-in-time / AsOfDate logic
   - no information after AsOfDate
   - target-leakage protections
8. Do not introduce new features during this task.
9. Do not keep a feature simply because it already exists.
10. Do not remove a feature simply to reduce the total feature count.
11. Prefer business meaning and potential predictive usefulness over achieving an arbitrary smaller feature count.
12. Do not create a "REVIEW REQUIRED" feature set for this exercise. Keep strong candidates and remove clearly weak/redundant ones.

VERY IMPORTANT – Recent Behaviour Features

Business specifically requested that useful recent member behaviours be captured.

Therefore, do not remove 30-day or 90-day features merely because a corresponding 12-month feature exists.

Treat the time windows as different behavioural signals:

- 12 months = longer-term behavioural baseline
- 90 days = recent behavioural activity/change
- 30 days = very recent / near-term behavioural activity

Retain the 30-day and 90-day features intentionally added where they represent strong and meaningful recent behaviour.

Examples that can legitimately coexist:

- "complaint_count_12m"
- "recent_complaint_count_90d"
- "recent_complaint_flag_30d"

Similarly retain useful recent variants for:

- helpline activity
- advice engagement
- complaint behaviour
- rollover/consolidation enquiries
- retirement enquiries
- website activity
- workflow activity
- campaign/event behaviour
- contribution behaviour
- partial rollover behaviour
- net-money-flow behaviour

Only remove a recent 30d/90d feature when it is clearly:

- mathematically equivalent to another retained feature
- providing exactly the same information
- weak/noisy based on the existing SQL semantics
- analysis-only rather than a meaningful member behaviour

Do not remove useful recent features simply because they are correlated with a 12-month version. Correlation-based removal can be handled later using actual modelling data.

General Reduction Principle

Different types of information should generally be retained when they capture different aspects of behaviour.

For example:

- count = frequency
- amount = magnitude
- days since last event = recency
- active months/days = consistency
- 12-month value = long-term behaviour
- 90-day value = recent behaviour
- 30-day value = very recent behaviour
- change percentage = trend
- cessation flag = complete stop in activity

Do not classify these as duplicates automatically.

Remove features only where there is strong redundancy.

---

Helpline Features

Retain strong general features such as:

- contact frequency
- active days
- days since last contact
- recent 90-day activity
- useful selective 30-day activity

Retain meaningful inquiry-description-based groups where present in the current SQL, for example:

- advice
- contribution
- consolidation / rollover
- retirement / pension
- investment
- insurance
- complaint
- digital access

Do not restore the old "repeat_contact_flag" if it has already been replaced by stronger inquiry-description-based features.

For category-specific features, retain recent 90-day / 30-day features only where they represent meaningful near-term behaviour.

---

Website Features

Keep the core website features currently defined, such as:

- activity count 12m
- active days 12m
- days since last activity
- recent activity 90d
- selective 30d activity if already intentionally included

The UAT website source is not populated.

Do not convert unavailable UAT website behaviour to zero.

Do not remove website features purely because UAT has no data if they are expected to be available in Production.

---

Workflow Features

Use the latest workflow logic based primarily on meaningful "jobDescription" behaviour.

Preserve business-confirmed exclusions such as:

- RF-Processor
- SUPERFACTS / SUPERFACTSS
- operational/system/batch workflow
- technical/admin activity

Keep only clearly meaningful member-driven categories already implemented in the current SQL, such as:

- member inquiry/service
- complaint/escalation
- member detail/contact change
- beneficiary activity

Retain useful overall workflow behaviour such as:

- meaningful workflow count 12m
- active days 12m
- days since last meaningful workflow
- recent 90-day activity
- recent 30-day activity
- completed/open workflow where these are genuinely different signals

Do not reintroduce rollover, payment, contribution, investment or insurance workflow features when stronger dedicated source tables already cover those behaviours.

---

Campaign / Event Features

Use the latest grouped event logic.

Do not restore excluded target/near-exit events such as:

- "MEMBER_EXIT"
- "ROLLOVER"
- "PAYMENT_EXTERNAL"

Keep strong meaningful groups already implemented, such as:

- advice
- digital engagement
- member service
- investment
- contribution
- roll-in
- retirement/pension
- insurance
- beneficiary

Remove analysis-only or weak buckets such as:

- "other_review_event_count_12m"

unless the current SQL shows a clear business meaning for them.

Do not create one feature for every raw event name.

Retain useful 90-day and selective 30-day behaviour where already added.

---

Contribution Behaviour – accountMoneyInflow

This section currently contains the largest amount of overlapping information.

Reduce redundant contribution features carefully.

Overall Contribution Behaviour

Prefer strong features such as:

- contribution count 12m
- contribution amount 12m
- contribution active months 12m
- days since last contribution
- recent contribution amount 90d
- recent contribution count 90d where useful
- contribution change percentage 90d
- contribution cessation flag 90d

Avoid keeping all of these simultaneously when they provide mathematically duplicate information:

- previous contribution amount 90d
- absolute contribution amount change 90d
- percentage contribution change 90d
- decline flag

For example, if change percentage plus cessation flag already represents the trend adequately, remove the weaker mathematically-derived variant.

Do not remove useful recent 90-day contribution behaviour.

Average Contribution Amount

Review whether:

"avg_contribution_transaction_amount_12m"

adds meaningful information beyond total contribution amount and contribution count.

Because it is mathematically derived from amount/count, it is a candidate for removal if it adds no distinct business information.

Employer SG

Do not retain every combination of:

- current amount
- previous amount
- absolute change
- percentage change
- increase flag
- decline flag
- cessation flag

Prefer a compact strong set such as:

- current Employer SG amount
- recent Employer SG amount 90d if already useful
- Employer SG change percentage
- Employer SG cessation flag

Remove previous amount / absolute change / increase or decline flags when they are redundant with retained change percentage and cessation.

Salary Sacrifice

Apply the same reduction principle.

Prefer:

- current Salary Sacrifice amount
- recent 90-day Salary Sacrifice amount where useful
- Salary Sacrifice change percentage
- Salary Sacrifice cessation flag

Remove redundant:

- previous amount
- absolute change
- separate increase flag
- separate decline flag

where the retained features already represent the same information.

Member Voluntary

Apply the same principle.

Prefer:

- current Member Voluntary amount
- recent 90-day amount where useful
- change percentage
- cessation flag

Remove redundant previous/absolute-change/increase/decline variants where appropriate.

Important Contribution Mapping

Do not modify the approved contribution mapping logic.

Preserve the existing validated logic for:

- Employer SG
- Salary Sacrifice
- Member Voluntary

Preserve approved exclusions including:

- internal transfers
- rollover type exclusions
- adjustments
- Mercer-related rollover/transfer inflows
- unrelated inflows

Do not simplify or invent contribution mappings.

---

Partial Rollover Behaviour

Use "edgeSource.accountRolloverPayment" as the preferred source.

Keep the validated partial-rollover features such as:

- partial rollover count 12m
- partial rollover amount 12m
- days since last partial rollover
- recent partial rollover count 90d
- recent partial rollover amount 90d

Do not remove the 90-day features simply because 12-month versions exist.

Do not restore full/external rollover features that were intentionally removed because of potential leakage.

Preserve:

"internalTransferFlag = 0"

logic.

Do not duplicate rollover behaviour through "accountMoneyInflow", campaign events or workflow when "accountRolloverPayment" provides the preferred source.

---

Investment Features

Treat "accountInvestments" as periodic investment-position snapshots, not investment-change events.

Keep only the latest validated position-as-of features:

- "investment_option_count_asof"
- "total_investment_value_asof"
- "direct_investment_flag"

Use the newest valid investment record for each:

"accountID + investmentCode"

on or before "@AsOfDate".

Do not restore old features such as:

- investment row/change count
- active investment days/months
- recent investment-change count

because periodic snapshots should not automatically be interpreted as member-driven changes.

---

Insurance Features

Use the point-in-time effective-date logic already implemented.

Keep the compact riskEvent-based features:

- Death cover flag
- Death cover amount
- TPD cover flag
- TPD cover amount
- Income Protection cover flag
- Income Protection cover amount
- insurance cover type count

Do not create features for every raw "coverDescription".

Do not combine Death + TPD + IP into one meaningless total insurance amount unless the existing validated SQL explicitly requires it.

---

Third Party Authority Features

Keep the compact point-in-time features:

- active third-party authority flag
- active adviser authority flag
- active family/legal authority flag
- active Power of Attorney flag
- active third-party authority count

Do not use high-cardinality fields such as adviser/company names or external identifiers.

If the overall active flag is completely derivable from retained subtype flags/count and provides no additional value, it may be marked as redundant and removed.

---

Net Money Flow – accountNetMoneyFlow

This should remain the preferred source for overall account-level money-flow behaviour.

Preserve the validated "cashFlowSign" logic and internal-transfer exclusion.

Review the existing features including:

- net flow 12m
- total positive cash flow 12m
- total negative cash flow 12m
- negative net-flow months 12m
- average active monthly net flow 12m
- recent net flow 90d
- prior net flow 90d
- net-flow decline flag
- days since last negative flow
- cashflow active months 12m

Retain different measures when they represent distinct concepts:

- net amount
- severity of outflow
- frequency of negative months
- recency of negative flow
- recent trend

But remove mathematically unnecessary features where another retained metric clearly contains the same information.

For example:

"net_flow_12m = positive_flow - negative_flow"

so review whether all three are required.

Do not automatically remove useful recent 90-day net-flow behaviour.

---

Cross-Source Duplication

Check the entire file for features that represent the same business behaviour through different source tables.

Use these preferred source responsibilities:

- "accountEngagementHelpline" → helpline/inquiry behaviour
- "accountEngagementWeb" → website behaviour when available
- "accountEngagementWorkflow" → meaningful workflow behaviour
- "campaignEventDetails/campaignEvents" → meaningful campaign/event behaviour
- "accountMoneyInflow" → contribution behaviour
- "accountRolloverPayment" → partial rollover/withdrawal behaviour
- "accountNetMoneyFlow" → overall net money-flow behaviour
- "accountInvestments" → investment position as of AsOfDate
- "AccountInsuranceCurrent" → active insurance position
- "thirdPartyAuthority" → active authority position

Do not duplicate the same rollover, contribution, investment, insurance or money-flow signal through multiple weaker sources when a preferred source exists.

---

What NOT to Remove Automatically

Do not automatically remove:

- 12m + 90d versions of the same behaviour
- 90d + 30d versions when both have a valid business purpose
- frequency + amount
- amount + recency
- frequency + recency
- current status + amount
- category-specific behaviours
- flags and amounts that represent different information
- recent behaviours specifically requested by business

Correlation-based removal should not be performed in this task unless features are also clearly mathematically or semantically redundant.

Actual correlation analysis can be performed later on the combined modelling dataset.

---

Final SQL Requirements

After reviewing the entire file:

1. Update "behavioural_features_business_review.sql".
2. Remove only clearly redundant / unnecessary features.
3. Do not modify unrelated business logic.
4. Remove SQL calculations/CTE columns that are no longer used.
5. Remove unused variables caused by feature removal.
6. Keep every standalone query independently runnable.
7. Keep SQL formatting compact and readable.
8. Avoid excessive blank lines.
9. Preserve existing feature documentation comments and update them to reflect the final retained features.
10. Do not build the final consolidated modelling dataset.
11. Do not train a model.
12. Do not modify any other files.

---

Feature Reduction Report

Before editing, create a proposed removal list:

"S.No | Feature Proposed for Removal | Feature Retained Instead | Reason"

Reasons should be limited to items such as:

- Exact duplicate
- Mathematically redundant
- Same business signal
- Analysis-only feature
- Duplicate signal from weaker source
- No distinct behavioural information

Do not use:

- High correlation

as a removal reason unless actual data correlation has been calculated later.

After updating the SQL, print the final removed-feature list.

Also report:

- Original feature count
- Number of features removed
- Final retained feature count
- Feature count by feature group

Example:

"Helpline = X"
"Website = X"
"Workflow = X"
"Campaign/Event = X"
"Contribution = X"
"Partial Rollover = X"
"Investment = X"
"Insurance = X"
"Third Party Authority = X"
"Net Money Flow = X"

---

Important Final Validation

Before finishing, confirm:

- useful 30-day/90-day recent behavioural features requested by business have not been accidentally removed
- 12-month baseline features remain where useful
- no future information is used
- no post-AsOfDate activity is used
- no churn target/outcome fields are included as predictive features
- "MEMBER_EXIT" is excluded
- full/external rollover leakage features remain excluded
- internal transfers remain excluded where applicable
- contribution mappings remain unchanged
- workflow system/admin noise remains excluded
- investment snapshots are not interpreted as investment-change events
- insurance effective-date logic remains point-in-time safe
- every standalone query still runs independently
- no unused feature calculations remain

Do not optimise for the smallest possible feature count.

The goal is:

retain a compact but strong feature set while preserving useful long-term and recent member behaviours for ML training.
