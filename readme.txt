Strictly follow ".github/copilot-instructions.md" and "AGENTS.md".

Fix the following Databricks runtime error in "ml_mscs_mrt_contribution_features.py", around line 570:

"UNRESOLVED_COLUMN.WITH_SUGGESTION: src.contributionType cannot be resolved. SQLSTATE: 42703"

Inspect the recently added runtime leakage validation logic.

- Identify where contributionType is derived and why it is unavailable in the validation DataFrame.
- Reuse the existing approved contribution classification logic and correct DataFrame references.
- Do not assume inflowRolloverType is equivalent to contributionType.
- Ensure leakage validation checks the actual feature-consumed records.
- Do not change existing business feature calculations, historical coverage logic or output schema.
- Preserve account-level grain, fundJoinDate eligibility and existing point-in-time rules.
- Do not use reportingDate.
- Modify only the contribution feature module.
- Do not execute any code or create permanent tables.

Apply the minimal correction and provide a short summary.
