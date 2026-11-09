Before moving to the next feature block, perform one final validation only. Do not modify the SQL.

In "behavioural_features_business_review.sql", validate the Campaign/Event feature logic and confirm:

1. Number of rows inside the actual Campaign/Event feature base/CTE where eventDate > @AsOfDate.
2. Number of rows inside the actual Campaign/Event feature base/CTE where eventDate < @FeatureStartDate.
3. Confirm the Campaign/Event feature window is exactly:
   @FeatureStartDate <= eventDate <= @AsOfDate
4. Confirm no retained Campaign/Event feature uses post-AsOfDate data.
5. Confirm final Campaign aggregation still has one row per accountID.

Important:
Do not report the total number of source-table records after @AsOfDate unless they actually enter the feature CTE. I only care about leakage into the feature dataset.

Return only:

- post-AsOfDate rows entering feature logic = X
- pre-FeatureStartDate rows entering feature logic = X
- duplicate accountID count = X
- PASS / FAIL
