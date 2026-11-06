The RF vs tuned RF vs XGBoost comparison is being interrupted because the comparison process is still tied to repeated SQL/model execution.

Please simplify the workflow.

1. Cache the real feature dataset once

Use the same already validated deterministic real-data sample of 10,000 accounts from the approved feature dataset.

Run the SQL extraction only once.

Save the resulting feature dataset locally as:

"member_retention_feature_sample_10000.parquet"

Preferred format: Parquet.

Also optionally save CSV for inspection:

"member_retention_feature_sample_10000.csv"

Validate before saving:

- rows = 10,000
- distinct accountID = 10,000
- duplicate accountID + AsOfDate = 0
- no synthetic rows
- same approved feature logic
- same target definition

2. Do not query SQL during model comparison

After the feature dataset is cached, all model comparison must read only from the local cached Parquet file.

Do not rerun:

- accountSummary queries
- feature CTEs
- rollover queries
- contribution queries
- other SQL lookups

during RF / XGBoost comparison.

The purpose is to isolate model comparison from SQL execution issues.

3. Use identical modelling data

Use the exact same cached dataset for:

1. Baseline Random Forest
2. Tuned Random Forest
3. XGBoost

Use the exact same:

- feature columns
- preprocessing
- target
- train split
- validation split
- random seed where applicable
- risk thresholds

Do not create different samples for different models.

4. Keep risk thresholds fixed

High >= 0.70
Medium >= 0.40 and < 0.70
Low < 0.40

Do not alter thresholds to create High Risk rows.

5. Baseline Random Forest

Run the current baseline RF configuration and capture:

- ROC-AUC
- PR-AUC
- Precision
- Recall
- F1
- confusion matrix
- probability min
- P50
- P75
- P90
- P95
- P99
- max
- High / Medium / Low counts

6. Tuned Random Forest

Use a LIGHTWEIGHT tuning search only.

Do not use a huge grid.

Test a small number of reasonable combinations around:

- n_estimators: 200, 400
- max_depth: 8, 12, None
- min_samples_leaf: 1, 5, 10
- min_samples_split: 2, 10
- max_features: sqrt
- class_weight: None, balanced

Limit the search so it completes reliably in the local environment.

Select the best tuned RF using validation performance, not High Risk count.

Capture the same metrics as baseline RF.

7. XGBoost

Run XGBClassifier on the SAME cached dataset.

If class imbalance exists, calculate:

"scale_pos_weight = negative_count / positive_count"

Use a modest configuration first, for example:

- n_estimators around 200–400
- max_depth around 3–6
- learning_rate around 0.03–0.1
- subsample around 0.8
- colsample_bytree around 0.8

Do not perform an expensive exhaustive grid search.

Capture the same metrics and probability statistics.

8. Comparison table

Produce:

Model | ROC-AUC | PR-AUC | Precision | Recall | F1 | P95 Prob | P99 Prob | Max Prob | High | Medium | Low

Compare:

- Baseline RF
- Tuned RF
- XGBoost

9. Select the model

Select the best model based primarily on:

- validation ROC-AUC
- PR-AUC
- recall / precision balance
- F1
- reasonable probability separation

Do NOT select a model only because it creates more High Risk accounts.

10. Generate outputs from selected model

Only after selecting the best model, regenerate:

"member_retention_ml_scoring_output.csv"

"member_retention_ml_scoring_sample_15.csv"

"member_retention_ml_scoring_validation.md"

using the selected model and cached real feature dataset.

11. 15-row sample

Where naturally available, select:

- 5 High
- 5 Medium
- 5 Low

If High Risk remains unavailable, do not fabricate it.

The sample must come directly from the selected model's real scoring output.

12. Final report

Clearly show:

- target class distribution
- baseline RF metrics
- tuned RF metrics
- XGBoost metrics
- probability distribution for each
- High / Medium / Low counts
- selected model
- reason for selection
- whether High Risk accounts were naturally generated

Important:
This remains a local technical comparison using a deterministic real-data sample and is not production-ready model selection.
