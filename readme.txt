Description:

The "Edge.AccountEngagementWeb" view contains records, but the following key columns are completely empty (NULL):

- WebAccountId
- JobSource
- JobType
- JobDescription
- RequestDate
- RequestParameters
- RequestId

Expected Result:
The key columns should contain relevant data where available from the source.

Actual Result:
All the above columns contain NULL values across all records.

Impact:
Missing data in these columns prevents evaluation of account web engagement features for the ML churn prediction model.
