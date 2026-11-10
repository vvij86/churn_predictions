Review ONLY the Contribution Behaviour feature block in "behavioural_features_business_review.sql" against the live MercerEdge source data.

Do NOT modify SQL yet.

Do NOT review Website Engagement or any unrelated feature block.

The purpose is to validate the business usefulness of the Contribution features and specifically address the client review comments before deciding what should be retained, renamed, de-scoped, or deduplicated.

IMPORTANT CONTEXT

The Contribution Behaviour source is primarily:

"edgeSource.accountMoneyInflow"

During the earlier Campaign/Event review, the business raised a concern that the following Campaign/Event features may duplicate contribution/transfer behaviour already captured from the contribution tables:

- "contribution_event_count_12m"
- "recent_contribution_event_count_90d"
- "rollin_event_count_12m"
- "recent_rollin_event_count_90d"

Those Campaign/Event features were temporarily retained as event-based signals, with the explicit note that overlap must be reviewed during Contribution feature deduplication.

Therefore this review MUST include a direct overlap/deduplication assessment between Campaign/Event contribution/roll-in features and "accountMoneyInflow" contribution features.

CURRENT CONTRIBUTION FEATURES TO REVIEW

Review all Contribution Behaviour features currently present, including at minimum:

- "contribution_count_12m"
- "contribution_amount_12m"
- "contribution_active_months_12m"
- "days_since_last_contribution"
- "recent_contribution_amount_90d"
- "prior_contribution_amount_90d"
- "recent_contribution_count_90d"
- "prior_contribution_count_90d"
- "contribution_change_pct_90d"
- "contribution_ceased_90d_flag"
- "employer_sg_amount_12m"
- "employer_sg_amount_90d"
- "salary_sacrifice_amount_12m"
- "salary_sacrifice_amount_90d"
- "member_voluntary_amount_12m"
- "member_voluntary_amount_90d"

CLIENT REVIEW COMMENTS THAT MUST BE ADDRESSED

1. Monetary contribution amounts are continuous values.

The business comment is essentially:

"Members are in different financial positions, therefore comparing larger/smaller contribution amounts does not necessarily indicate stronger or weaker engagement."

Do NOT interpret a larger contribution amount as automatically meaning stronger engagement.

Instead determine whether the amount features are still useful as:

- financial behaviour,
- contribution change,
- contribution cessation,
- contribution pattern,
- contribution recency,
- change relative to the same member/account's own prior contribution behaviour.

2. The comment "Amounts don't indicate engagement" must be explicitly addressed.

Assess whether raw monetary amount features should:

- remain as financial-behaviour features,
- be transformed into relative/change features,
- be retained but not described as "engagement",
- or be de-scoped if they provide little incremental information.

3. Review whether recent-vs-prior comparison features are more defensible than absolute amounts.

Specifically assess:

- "recent_contribution_amount_90d"
  vs
- "prior_contribution_amount_90d"

and:

- "recent_contribution_count_90d"
  vs
- "prior_contribution_count_90d"

and:

- "contribution_change_pct_90d"
- "contribution_ceased_90d_flag"

Determine whether these better capture a behavioural change within the same account rather than comparing rich versus less-rich members.

LIVE VALIDATION REQUIRED

Use the existing database connection pattern and actual source data.

For each contribution feature/family report:

- total source rows
- distinct accountIDs
- accounts with non-zero coverage
- min / median / average / max where appropriate
- 12-month coverage
- 90-day coverage
- zero/null rate
- extreme/outlier values where relevant

Confirm:

- no records after "@AsOfDate" enter the feature logic
- no records before "@FeatureStartDate" enter the 12-month feature logic
- final aggregation grain = one row per accountID
- final duplicate accountID count = 0

Do not confuse raw transaction-level repeated accountIDs with final aggregated duplicates.

CAMPAIGN/EVENT DUPLICATION CHECK — REQUIRED

Compare the retained Campaign/Event features:

- "contribution_event_count_12m"
- "recent_contribution_event_count_90d"
- "rollin_event_count_12m"
- "recent_rollin_event_count_90d"

against the Contribution Behaviour records/features from "edgeSource.accountMoneyInflow".

Do more than an account-level overlap count if source fields allow it.

For CONTRIBUTION and ROLLIN separately report:

1. Accounts present in Campaign/Event only.
2. Accounts present in accountMoneyInflow only.
3. Accounts present in both.
4. Percentage overlap.
5. Event/transaction date overlap where possible.
6. Whether matching activity appears to represent the same underlying transaction/business action.
7. Whether Campaign/Event is merely duplicating the financial transaction already represented by accountMoneyInflow.
8. Whether Campaign/Event adds any genuinely different information.

If exact transaction matching is not technically possible because there is no reliable common transaction ID, state that clearly and use the strongest available evidence such as:

- accountID
- date
- event type
- contribution type
- transaction amount if available

Do NOT automatically call two features duplicates merely because the same account appears in both datasets.

CLASSIFY EACH FEATURE

For every current Contribution feature return one of:

- KEEP
- REVIEW
- DE-SCOPE
- POSSIBLE DUPLICATE

Give a short evidence-based reason.

Pay special attention to whether these are more defensible retention signals:

- contribution frequency
- active contribution months
- days since last contribution
- recent contribution count
- change from prior contribution behaviour
- contribution ceased flag

versus raw absolute monetary values.

CONTRIBUTION TYPE REVIEW

Validate the actual source values used to derive:

- employer SG
- salary sacrifice
- member voluntary
- roll-in / transfer-related inflow

Do not infer categories from feature names alone.

Report the exact source values/mappings being used.

Check whether any contribution type is incorrectly grouped or double-counted.

EXPECTED OUTPUT

Return:

1. Technical integrity result: PASS / REVIEW / FAIL.

2. A decision table:

Feature | Live coverage | Business meaning | Client concern | Campaign overlap | Recommendation | Reason

3. A separate Campaign/Event deduplication table:

Campaign feature | accountMoneyInflow equivalent | Account overlap | Date/event overlap | Same underlying behaviour? | Recommendation

4. Clearly answer:

- Are raw monetary contribution amounts valid predictive financial-behaviour features even though they should not be described as "engagement"?
- Are relative/change features more defensible than absolute amounts?
- Which contribution features should remain active?
- Which Campaign contribution/roll-in features should remain active after the overlap review?
- Are any features genuinely duplicated and therefore candidates for de-scoping?

5. Show the exact active feature list you recommend after the review.

IMPORTANT:
Do NOT change the SQL in this step.
Do NOT remove a feature simply because it overlaps at account level.
Do NOT assume larger monetary amount = stronger engagement.
Base conclusions only on actual source mappings and live-data evidence.
