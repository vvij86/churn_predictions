Follow ".github/copilot-instructions.md".

Fix the runtime error in "ml_mscs_mrt_runtime_leakage_evidence.py", specifically inside "append_runtime_leakage_evidence()" around line 57.

Error: "pyarrow.lib.ArrowTypeError: object of type <class 'str'> cannot be converted to int".

- Compare every value passed to createDataFrame against its declared schema and column order.
- Ensure DateType receives Python datetime.date, numeric fields receive appropriate Python integers, and string fields receive strings.
- Preserve NULL values where applicable. Do not convert missing leakage evidence to zero.
- Ensure compatibility with Databricks Serverless and Spark Connect.
- Review all existing callers of this shared utility for argument compatibility to prevent the same error in other feature modules.
- Preserve existing leakage validation semantics.
- Modify only the shared runtime leakage evidence utility unless another change is strictly necessary.
- Do not change business feature calculations, base population, fundJoinDate eligibility, target labels or temporal split logic.
- Do not use reportingDate.
- Do not execute any code or create permanent tables.

Apply the minimal fix and provide a short summary.
