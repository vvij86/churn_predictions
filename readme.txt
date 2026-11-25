Read and strictly follow ".github/copilot-instructions.md".

Perform a targeted review and correction of the recently introduced runtime leakage validation logic across ALL existing ML feature modules.

Current Databricks execution results for as_of_date = 2024-03-31:

- Contribution module completed successfully after the recent correction, with 785885 output rows and zero reported future leakage.
- Rollover module failed with:
  "ValueError: Critical validation failure: future rollover records detected in feature logic."

Review the following modules together:

- ml_mscs_mrt_contribution_features.py
- ml_mscs_mrt_rollover_features.py
- ml_mscs_mrt_investment_features.py
- ml_mscs_mrt_helpline_features.py
- ml_mscs_mrt_campaign_features.py
- ml_mscs_mrt_web_engagement_features.py
- ml_mscs_mrt_third_party_authority_features.py
- ml_mscs_mrt_insurance_features.py
- ml_mscs_mrt_account_profile_features.py

Implementation requirements:

1. Understand the recent successful contribution module correction and assess whether equivalent defects exist in the remaining modules.
2. Trace each leakage counter to the actual DataFrame consumed during feature calculation.
3. Distinguish future records present in raw source tables from future records actually consumed by features.
4. Correct false-positive validation logic wherever identified.
5. If genuine leakage exists, correct the relevant point-in-time feature filtering.
6. Check all runtime evidence calls for correct column references, DataFrame aliases, schema compatibility, data types and function arguments.
7. Prevent unresolved column errors and Spark Connect/PyArrow type conversion errors.
8. Do not introduce tautological validation checks, hardcoded zero counts or artificial PASS results.
9. Preserve NOT VALIDATED wherever sufficient evidence is unavailable.
10. Review compatibility with the existing runtime leakage evidence utility and feature validation runner.

Mandatory restrictions:

- Maintain one row per account_id per as_of_date.
- Preserve fundJoinDate-based account eligibility.
- Never use reportingDate for as-of-date filtering.
- Preserve historical source start date 2023-04-01.
- Newly joined accounts must remain eligible.
- AccountEngagementWeb remains empty; preserve NULL handling.
- Preserve insurance historical availability limitations.
- Do not reintroduce de-scoped workflow features.
- Do not change approved business feature calculations unless required to fix genuine leakage.
- Do not modify base population, target labels, historical snapshots or temporal split logic.
- Do not generate new Python files or notebooks.
- Do not execute Databricks jobs or write permanent tables.

Apply all necessary corrections together in this single request. Avoid unrelated refactoring.

Perform a final static consistency check across all reviewed modules before completing.

Provide a concise module-wise summary showing:

- Module name
- Issue identified
- Correction applied
- Remaining validation limitations

Do not claim runtime validation has passed without execution evidence.
