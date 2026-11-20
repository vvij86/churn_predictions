Update the following existing feature modules to use the corrected controlled-snapshot base population:

- notebook/ml_mscs_mrt_contribution_features.py
- notebook/ml_mscs_mrt_rollover_features.py
- notebook/ml_mscs_mrt_investment_features.py
- notebook/ml_mscs_mrt_insurance_features.py

Follow `.github/copilot-instructions.md` strictly.

Do NOT rewrite these files from scratch.

Preserve all already-reviewed:

- business logic
- feature names
- source mappings
- logging
- validation
- exclusions
- point-in-time logic

The only purpose of this change is to align all modules with the corrected modelling snapshot design.

MANDATORY RULE:

All feature modules must reuse the common base population from:

`ml_mscs_mrt_base_population.py`

and must use the same explicitly supplied controlled:

`as_of_date`

For the current development run:

as_of_date = "2024-03-31"

Do NOT derive `as_of_date` from:

- reportingDate
- fundJoinDate
- exit dates
- transaction dates
- event dates
- system date

Each module should accept the active SparkSession and controlled snapshot date, conceptually:

run_<feature>_pipeline(
    spark,
    as_of_date="2024-03-31"
)

Pass the same `as_of_date` to:

`run_base_population_pipeline(...)`

Do not independently rebuild the account population inside individual feature modules.

Feature windows must remain relative to the controlled `as_of_date`.

Examples:

- trailing 12-month contribution window
- recent 90-day contribution window
- prior 90-day contribution window
- rollover feature windows
- investment position as of snapshot
- insurance position as of snapshot

All source records used in predictive features must satisfy:

event/source date <= as_of_date

Do not generate multiple snapshots inside any individual feature module.

Final grain of every module must remain:

one row per account_id per as_of_date

For the current run, all output rows should have:

as_of_date = 2024-03-31

Keep the existing final DataFrames:

- contribution_features_df
- rollover_features_df
- investment_features_df
- insurance_features_df

Do not persist these individual feature DataFrames as tables yet.

Validation for each module must confirm:

- output row count
- distinct account_id + as_of_date
- duplicate count = 0
- null account_id = 0
- null as_of_date = 0
- future leakage count = 0 where applicable
- exactly one controlled snapshot date for this development run

Do not change feature business logic unless required specifically to remove dependence on reportingDate-derived as_of_date.

Do not modify unrelated Data Engineering / Power BI files.

After updating, provide a short summary by file of what changed.
