Update the existing file:

notebook/ml_mscs_mrt_base_population.py

Follow `.github/copilot-instructions.md` strictly.

IMPORTANT: Do not rewrite the file from scratch. Preserve the current structure, logging, validation, helper functions, source mappings and eligibility logic unless required for this correction.

The current implementation incorrectly derives `as_of_date` from `reportingDate`.

Correct this.

MANDATORY RULE:

`as_of_date` must be an explicit controlled modelling snapshot parameter equivalent to the reviewed SQL Server `@AsOfDate`.

For the current development run use:

AS_OF_DATE = "2024-03-31"

Do NOT derive `as_of_date` from:

- reportingDate
- fundJoinDate
- exitDate
- exitDateRecorded
- any event date
- system/current date

Use `fundJoinDate` only for eligibility and tenure logic, e.g.:

fundJoinDate <= as_of_date

Use exit logic only for eligibility:

exitDateRecorded IS NULL OR exitDateRecorded > as_of_date

Preserve the reviewed deceased-member exclusions and database/fund scope.

`reportingDate` must NOT become the modelling snapshot date.

It may only be used if genuinely required for deterministic source-record selection, and if so document why.

The base population output must contain:

- account_id
- member_id
- customer_id
- fund_id
- fund_join_date
- as_of_date

Every eligible account for this run must have:

as_of_date = 2024-03-31

Final grain:

one row per account_id per as_of_date

Update `run_base_population_pipeline()` so it accepts the controlled `as_of_date` parameter.

Prefer:

run_base_population_pipeline(spark, as_of_date="2024-03-31")

Do not generate multiple snapshots inside this file.

Multiple snapshots will be handled later by a higher-level process that repeatedly calls this pipeline with different controlled dates.

Validation must include:

- output row count
- distinct account_id + as_of_date
- duplicate count
- null account_id
- null as_of_date
- distinct as_of_date values
- minimum as_of_date
- maximum as_of_date

For this development run, validate that exactly one distinct modelling snapshot date exists:

2024-03-31

Do not modify unrelated ML feature files yet.

After making the changes, summarize exactly what was changed and flag any remaining dependency on reportingDate.
