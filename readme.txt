Follow ".github/copilot-instructions.md" and "AGENTS.md".

Fix the following runtime validation failure in "ml_mscs_mrt_contribution_features.py" around line 674:

"ValueError: Critical validation failure: future contribution records detected in feature context."

Snapshot date: 2024-03-31.

- Trace the future leakage counter to the exact DataFrame used for contribution feature aggregation.
- Determine whether future records actually influence calculated features or are merely present in the raw source or intermediate candidate dataset.
- If it is a validation false positive, correct the validation logic.
- If actual leakage exists, correct the relevant point-in-time filtering.
- Do not suppress the exception, hardcode zero counts or artificially force PASS.
- Preserve approved contribution calculations and historical coverage logic.
- Maintain account_id + as_of_date grain, fundJoinDate eligibility and no reportingDate filtering.
- Briefly inspect the other feature modules for the same validation defect to avoid repeated runtime failures. Report any findings without modifying those modules.
- Modify only the contribution feature module.
- Do not execute code or write permanent tables.

Apply the minimal necessary correction and provide a concise summary.
