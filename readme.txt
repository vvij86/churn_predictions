Based on the Contribution Behaviour live-data review just completed, make the FINAL evidence-based deduplication recommendation between:

Campaign/Event features:

- contribution_event_count_12m
- recent_contribution_event_count_90d
- rollin_event_count_12m
- recent_rollin_event_count_90d

and the Contribution Behaviour features sourced from:
"edgeSource.accountMoneyInflow"

Do NOT modify SQL yet.

We already established:

- Campaign contribution events have extremely high account overlap with accountMoneyInflow contribution activity.
- Same-account + same-day / ±1-day alignment is very high.
- There is no reliable common transaction ID.
- Campaign contribution event features therefore appear to represent largely the same underlying contribution activity.
- Roll-in events show material overlap, but are not necessarily identical because roll-in/transfer behaviour may not be represented by the same accountMoneyInflow contribution logic.

Perform the final decision separately for CONTRIBUTION and ROLLIN.

For CONTRIBUTION:

Decide whether these should be DE-SCOPED from the active Campaign/Event ML feature list:

- contribution_event_count_12m
- recent_contribution_event_count_90d

Use the live overlap evidence already obtained.

If de-scoping is recommended, explicitly state that accountMoneyInflow contribution frequency/change/recency features remain the authoritative contribution behaviour features.

For ROLLIN:

Review:

- rollin_event_count_12m
- recent_rollin_event_count_90d

Determine whether these capture a genuinely distinct roll-in / transfer-in event that is not already represented by the current accountMoneyInflow contribution feature set.

Check actual source event mappings and, where possible:

- source event names
- same account overlap
- same/near date overlap
- whether accountMoneyInflow explicitly includes or excludes roll-in / transfer transactions
- whether roll-in represents new incoming money from another fund rather than a normal contribution

Return exactly:

Feature | Final decision | Evidence | Reason

Allowed decisions:

- KEEP
- DE-SCOPE
- REVIEW

Also return:

1. Final Campaign/Event active feature list after contribution deduplication.
2. Final Contribution Behaviour active feature list.
3. A short business-review comment I can paste against Nathan's original "likely duplication with Contributions table" comment.

Do NOT change SQL in this step.
