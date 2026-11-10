Update only the Campaign/Event contribution-related feature logic in "behavioural_features_business_review.sql" based on the completed live-data deduplication review.

Do not modify any other feature block.

Final decisions:

DE-SCOPE:

- contribution_event_count_12m
- recent_contribution_event_count_90d

RETAIN FOR REVIEW:

- rollin_event_count_12m
- recent_rollin_event_count_90d

Reason:

Live validation showed that Campaign/Event contribution activity has extremely high account and date overlap with contribution behaviour already captured from "edgeSource.accountMoneyInflow".

Therefore the Campaign/Event contribution counters should no longer be exposed as active ML features because they largely duplicate the authoritative Contribution Behaviour features.

For the two contribution event features:

1. Remove/comment them from the active Campaign/Event final SELECT output.
2. Keep the underlying source mapping/commented reference logic if useful for traceability.
3. Add a short SQL comment such as:

"BUSINESS REVIEW: De-scoped because live validation showed very high overlap with accountMoneyInflow contribution behaviour; not treated as an independent ML signal."

For Roll-in:

Keep active:

- rollin_event_count_12m
- recent_rollin_event_count_90d

Add a review comment such as:

"BUSINESS REVIEW: Retained for review as potential transfer-in behaviour. It overlaps with contribution activity but is not confirmed to represent the same underlying financial action."

Important:

- Do not merge Roll-in into Contribution.
- Do not rename Roll-in as Contribution.
- Do not change the accountMoneyInflow Contribution Behaviour block.
- Do not change Website Engagement.
- Do not change Helpline, Workflow, or any other feature section.
- Preserve one row per accountID.
- Preserve the existing FeatureStartDate / AsOfDate boundaries.

After the change, validate and report:

1. "contribution_event_count_12m" active in final Campaign/Event output: YES/NO
2. "recent_contribution_event_count_90d" active: YES/NO
3. "rollin_event_count_12m" active: YES/NO
4. "recent_rollin_event_count_90d" active: YES/NO
5. final duplicate accountID count
6. post-AsOfDate rows entering feature logic
7. pre-FeatureStartDate rows entering feature logic
8. PASS / REVIEW / FAIL

Expected result:

- contribution event features = NO
- roll-in features = YES
- duplicate accountID count = 0
- post-AsOfDate = 0
- pre-FeatureStartDate = 0

Also show exactly which SQL lines/features were changed.
