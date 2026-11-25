Follow ".github/copilot-instructions.md".

Based on the previous read-only review, implement only the following two corrections in "notebook/ml_mscs_mrt_consolidated_features.py".

1. Integrate the existing account profile feature pipeline using its actual function signature and the shared base population DataFrame.
2. Extend the existing de-scoped column validation to explicitly prevent workflow features, target labels and temporal split assignment columns from entering the consolidated feature output. Use actual column names from the repository.

Requirements:

- Ensure all nine active feature modules are integrated.
- Handle overlapping account profile and base population columns explicitly without introducing duplicate or ambiguous columns.
- Maintain exactly one row per account_id + as_of_date.
- Preserve all eligible base population accounts.
- Preserve existing feature names, calculations, historical coverage, runtime leakage safeguards and NULL/zero handling.
- Preserve web engagement SOURCE_UNAVAILABLE behavior.
- Ensure persist_output=False prevents all persistent table writes.
- Preserve existing pipeline function signatures and persistence behavior.

Strict restrictions:

- Modify only "ml_mscs_mrt_consolidated_features.py".
- Do not modify individual feature modules, historical coverage, runtime leakage evidence, base population, target labels or temporal split logic.
- Do not create new files.
- Do not execute scripts, notebooks, SQL or terminal commands.
- Do not redesign the existing architecture.

Perform a static review of the changes and provide minimal Databricks execution code for as_of_date="2024-03-31" with persist_output=False.

Keep the implementation and response concise.
