One additional confirmed business requirement:

The business has asked us to use historical data starting from 01-Apr-2023 for model training.

Please incorporate this into the proposed design before rewriting the SQL.

Important interpretation:

- 01-Apr-2023 is the earliest available/in-scope historical source-data date.
- We are currently planning a 12-month feature window and 3-month outcome window.
- Therefore, if a complete 12-month feature history is required, the earliest full training snapshot should be:

  FeatureStartDate = 2023-04-01
  AsOfDate         = 2024-03-31
  OutcomeStartDate = 2024-04-01
  OutcomeEndDate   = 2024-06-30

- Subsequent historical training snapshots can move quarterly.
- Do not interpret "train from 01-Apr-2023" as requiring an AsOfDate of 01-Apr-2023, because there would be no prior 12-month feature history available.

Also review historical eligibility carefully:

- An account must have existed as of the supplied @AsOfDate.
- Where fundJoinDate/account commencement date is reliable, require it to be <= @AsOfDate.
- Accounts that exited before or on @AsOfDate should not be treated as active prediction candidates.
- Future exits after @AsOfDate may be used only for target/outcome creation.

One caution on customerMapping:
Profiling showed one current row per account. Do not automatically treat accurateDate <= @AsOfDate as proof of a complete historical mapping snapshot. Use it only where point-in-time validity is defensible and document any limitation.

Please update the proposed structure with these requirements only.

Do NOT modify build_merceredge_base_historical_dataset.sql yet.
