Review the existing Member Retention Analytics code, particularly:

- ml_mscs_mrt_config.py
- ml_mscs_mrt_target_labels.py
- ml_mscs_mrt_historical_snapshots.py
- ml_mscs_mrt_temporal_split.py
- Existing target validation SQL files.

Check whether changing the churn prediction window from 3 months to 6 months can be achieved through a single configuration parameter.

Verify:

1. Existing prediction window configuration and default value.
2. Any hardcoded 3-month prediction window conditions.
3. Outcome start and end date calculations.
4. Handling of snapshots with incomplete future outcome data.
5. Temporal split logic and prevention of overlapping outcome windows across dataset boundaries.
6. Impact on Ground Truth generation and modelling dataset preparation.

Provide a concise summary of the findings, affected files and minimal changes required, if any.

Do not modify any files, create new files, execute scripts or write to Databricks tables.

Do not change ATO exclusion or Other payment type logic at this stage.

Do not modify the existing feature engineering pipeline or regenerate historical feature snapshots.
