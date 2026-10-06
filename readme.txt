Before making further changes to the base historical dataset query, I want to verify whether MercerEdge contains a genuine historical account snapshot source.

We have confirmed that edgeSource.accountSummary contains only one distinct row per accountID and reportingDate appears to represent the latest/current record. For exited accounts, reportingDate is also equal to exitDate.

Therefore, do NOT assume accountSummary is a historical snapshot table.

Please investigate the following 18 in-scope tables using the DDL files and read-only SQL profiling:

1. merceredge.edgeSource.accountSummary
2. merceredge.edgeSource.accountEngagementWorkflow
3. merceredge.edgePortalSource.pensionerData
4. merceredge.edgeSource.accountEngagementHelpline
5. merceredge.edgeSource.accountEngagementWeb
6. merceredge.edgeSource.AccountInsuranceCurrent
7. merceredge.edgeSource.accountInvestments
8. merceredge.edgeSource.accountMoneyInflow
9. merceredge.edgeSource.accountNetMoneyFlow
10. merceredge.edgeSource.accountRolloverPayment
11. merceredge.edgeSource.campaignEventDetails
12. merceredge.edgeSource.campaignEvents
13. merceredge.edgeSource.customerMapping
14. merceredge.edgeSource.customerSummary
15. merceredge.edgeSource.thirdPartyAuthority
16. merceredge.tableau.fundListSource
17. merceredge.edgeSource.campaign
18. merceredge.edgeSource.campaignAccountMapping

For each table, determine:

- Does the same accountID appear multiple times?
- Is there a genuine historical/snapshot date column?
- Does that date represent when the account state was valid, or only when an event occurred?
- Can the table reconstruct the state of an account as of a past @AsOfDate?
- What important account-level fields are available historically?
- Is it suitable as:
  1. historical account snapshot source
  2. historical event/transaction source
  3. current/static lookup only
  4. target/outcome source

Specifically look for any table that can provide historical values for:
- account status
- account balance / FUM
- account type
- member/account state
- other important account-level attributes

Profile candidate tables using read-only SQL.

For candidate historical snapshot tables, check:

SELECT
    COUNT(*) AS total_rows,
    COUNT(DISTINCT accountID) AS distinct_accounts
FROM <table>;

Also inspect a few accountIDs that have multiple records and order them by the relevant date column.

Produce a summary:

Table | Rows per Account | Historical Date Column | Historical Snapshot? | Recommended Purpose

IMPORTANT:
Do not modify the modelling query yet.

First identify whether a genuine historical account snapshot table exists.

If none of the 18 tables provides historical account snapshots, state that clearly rather than inventing one.

In that case, explain which parts of the modelling dataset can still be reconstructed reliably from historical event/transaction tables and which account-level attributes cannot be made point-in-time safe.
