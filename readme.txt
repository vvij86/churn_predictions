Update the historical snapshot runner from the current 3-snapshot test to the full controlled historical modelling range.

Current file:

"ml_mscs_mrt_historical_snapshots.py"

The 3-snapshot test has completed successfully with all validations PASS.

Now change the runner to use a configurable historical range rather than test-only constants.

Requirements:

- Historical source availability starts from "2023-04-01".
- Generate monthly month-end snapshots.
- First usable monthly snapshot:
  "2023-04-30"
- Use this current historical end date:
  "2026-07-31"

Reason for the end date:

- the target outcome horizon is currently 90 days
- each labelled snapshot must have a complete future outcome window
- "2026-07-31" is the latest safe month-end snapshot with a fully observed 90-day target window based on current data availability

Do NOT generate later labelled snapshots such as August, September or October 2026 until their full outcome windows are available.

Use:

"HISTORICAL_START_DATE = "2023-04-30""

"HISTORICAL_END_DATE = "2026-07-31""

Keep both values centrally configurable.

Do NOT derive snapshot dates from:

- reportingDate
- fundJoinDate
- exitDate
- transaction/event dates
- system/current date

Reuse the existing centralized snapshot generator in:

"ml_mscs_mrt_config.py"

Continue to generate month-end snapshots only.

Processing

Process snapshots sequentially.

Keep:

"stop_on_first_failure=True"

For every snapshot:

1. Generate consolidated features.
2. Run existing feature validations.
3. Persist only after PASS.
4. Generate target/ground truth from the persisted feature snapshot.
5. Run existing target validations.
6. Persist only after PASS.
7. Log snapshot runtime and status.

Do NOT change:

- feature engineering business logic
- churn/target definition
- 90-day outcome horizon
- eligibility logic
- leakage rules
- account_id + as_of_date grain
- existing validation logic

Persistence

Continue writing all snapshots into the same Delta tables:

"mer_wealth_dev.mer_wealth_mra_mlops.member_retention_features"

and

"mer_wealth_dev.mer_wealth_mra_mlops.member_retention_ground_truth"

Do NOT create a separate table per month.

Keep the existing idempotent MERGE / snapshot-safe write logic.

Rerunning an existing snapshot must:

- not create duplicates
- not delete other snapshots
- safely replace/update only that snapshot if required

Existing snapshots such as:

- "2024-03-31"
- "2024-04-30"
- "2024-05-31"

must remain valid and must not duplicate when encountered again.

Final historical-run summary

At the end print:

Snapshot | Feature Status | Feature Rows | Target Status | Churn Rows | Churn % | Runtime

Also print:

- requested snapshot count
- successful snapshot count
- failed snapshot count
- first snapshot
- last snapshot
- total runtime
- overall PASS/FAIL

After the full run, validate:

- all requested as_of_date values are present
- no duplicate account_id + as_of_date
- row counts by snapshot
- target distribution by snapshot
- no snapshots accidentally overwritten
- no snapshot generated beyond the allowed complete target horizon

Do NOT create train/validation/test splits yet.

Do NOT start model training yet.

After implementation tell me:

1. start date
2. end date
3. total number of monthly snapshots generated
4. first and last snapshot dates
5. confirmation that the 90-day outcome window remains unchanged
6. confirmation that existing business logic was not changed
7. confirmation that persistence remains idempotent
8. exact file I should run for the full historical generation
