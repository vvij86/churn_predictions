Perform a full behavioural feature coverage audit for the Member Retention Analytics ML feature build.

Follow `.github/copilot-instructions.md` strictly.

DO NOT modify any code yet.

BUSINESS-LOGIC REFERENCE FILES

1. `behavioural_features_business_review.sql`
2. `AccountEngagementWeb_Reviewed_Features.sql`

IMPLEMENTED PYSPARK MODULES TO REVIEW

- `notebook/ml_mscs_mrt_base_population.py`
- `notebook/ml_mscs_mrt_contribution_features.py`
- `notebook/ml_mscs_mrt_rollover_features.py`
- `notebook/ml_mscs_mrt_investment_features.py`
- `notebook/ml_mscs_mrt_insurance_features.py`
- `notebook/ml_mscs_mrt_helpline_features.py`
- `notebook/ml_mscs_mrt_campaign_features.py`
- `notebook/ml_mscs_mrt_web_engagement_features.py`
- `notebook/ml_mscs_mrt_third_party_authority_features.py`

PURPOSE

Compare every reviewed/active behavioural feature from the two SQL reference files against the implemented PySpark modules and determine whether the current Databricks implementation has complete feature coverage.

Do not assume a feature is implemented just because a similarly named column exists.

For each reviewed feature verify:

1. Feature name.
2. Behavioural block/category.
3. Status in reviewed SQL:
   - active/keep
   - review/pending
   - de-scoped/removed
4. Expected source table.
5. PySpark module where it is implemented.
6. Exact final DataFrame column name.
7. Present or missing.
8. Whether business logic matches the reviewed SQL.
9. Whether the controlled `as_of_date` design is used correctly.
10. Whether point-in-time filtering is correct.
11. Whether future/outcome leakage is prevented.
12. Whether the feature is present in the FINAL module output, not only as an intermediate column.

CONTROLLED SNAPSHOT RULE

Current development snapshot:

`as_of_date = "2024-03-31"`

All implemented modules must use the shared base population from:

`notebook/ml_mscs_mrt_base_population.py`

and preserve:

one row per account_id per as_of_date

Do not treat `reportingDate`, `fundJoinDate`, event dates, transaction dates, exit dates, or current system date as the modelling `as_of_date`.

IMPORTANT COVERAGE RULES

- Do not count de-scoped features as missing.
- Do not count intermediate calculation fields as final implemented features.
- Do not reintroduce previously removed duplicate features.
- AccountEngagementWeb features may legitimately be NULL/unavailable in UAT; still count them as implemented if the reviewed logic exists and source-unavailable handling is correct.
- Do not invent missing source mappings.
- If a reviewed feature cannot be implemented because the Databricks source/column is unavailable, mark it clearly as:
  `BLOCKED - SOURCE MAPPING REQUIRED`
- If business review status is still pending, mark:
  `PENDING BUSINESS REVIEW`
- If deliberately de-scoped, mark:
  `DE-SCOPED - NO ACTION`

Produce a coverage matrix with columns:

- Behavioural Block
- Feature Name
- Reviewed Status
- Source
- PySpark Module
- Final Output Column
- Implementation Status
- SQL Logic Match
- Snapshot/Point-in-Time Safe
- Leakage Safe
- Notes

Then provide a final summary:

1. Total reviewed active features.
2. Total implemented correctly.
3. Total missing.
4. Total blocked by source mapping.
5. Total pending business review.
6. Total de-scoped.
7. Overall implementation coverage percentage.
8. List ONLY the genuinely missing feature blocks/features that still require development.
9. Confirm whether we are ready to proceed to the consolidated feature dataset.

Do not modify any `.py` or `.sql` files during this audit.
