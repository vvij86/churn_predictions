The current XGBoost model includes the approved partial rollover features, but account-level SHAP results still show that partial rollover is rarely becoming a primary or additional churn driver.

I want to tune XGBoost properly and check whether the model can capture rollover-related churn patterns better.

Do NOT artificially force partial rollover to become important.

Do NOT change risk thresholds merely to produce desired results.

Use the same real feature dataset, same target, same train/validation methodology, and same leakage rules.

1. Confirm rollover features are in the model

Before tuning, verify these approved rollover features are present in the XGBoost feature matrix:

- partial_rollover_count_12m
- partial_rollover_amount_12m
- days_since_last_partial_rollover
- recent_partial_rollover_count_90d
- recent_partial_rollover_amount_90d

Also include any other approved rollover behavioural feature already present in the consolidated feature dataset.

Print FOUND / NOT FOUND for each.

2. Baseline model

Run the current XGBoost configuration first and capture baseline metrics:

- ROC-AUC
- PR-AUC / Average Precision
- Precision
- Recall
- F1
- confusion matrix
- Brier score if available
- probability P50
- P90
- P95
- P99
- max probability
- High / Medium / Low counts

Also calculate SHAP-based rollover diagnostics:

- number of rollover-positive accounts
- number where rollover is top SHAP driver
- number where rollover is in top 3 SHAP drivers
- number where rollover is in top 5 SHAP drivers
- average rollover SHAP contribution among rollover-positive accounts
- median rollover SHAP contribution
- maximum rollover SHAP contribution

3. Tune XGBoost

Use a lightweight, controlled hyperparameter search.

Test reasonable combinations around:

- n_estimators: 200, 400, 600
- max_depth: 3, 4, 5, 6
- learning_rate: 0.03, 0.05, 0.1
- min_child_weight: 1, 3, 5, 10
- subsample: 0.7, 0.8, 1.0
- colsample_bytree: 0.6, 0.8, 1.0
- gamma: 0, 0.1, 0.3
- reg_alpha: 0, 0.1, 0.5
- reg_lambda: 1, 2, 5

If churn class imbalance exists, calculate:

"scale_pos_weight = negative_count / positive_count"

and compare:

- scale_pos_weight = 1
- calculated scale_pos_weight

Do not run an excessively large exhaustive grid if it is too slow locally.

Prefer RandomizedSearchCV or a limited manual search.

4. Use proper validation

Use the same chronological/time-based validation where available.

Do not randomize historical snapshots unless necessary for this technical comparison.

Select the best model based primarily on:

- ROC-AUC
- PR-AUC
- recall / precision balance
- F1
- calibration / Brier score
- sensible probability separation

Do NOT select the model merely because rollover importance increased.

5. Recalculate SHAP for each candidate / best model

After selecting the best tuned model, calculate account-level SHAP values again.

For rollover-positive accounts, inspect:

- partial_rollover_count_12m
- partial_rollover_amount_12m
- days_since_last_partial_rollover
- recent_partial_rollover_count_90d
- recent_partial_rollover_amount_90d

For each account calculate:

- actual feature value
- SHAP contribution
- SHAP rank
- whether rollover is primary driver
- whether rollover is additional driver

6. Compare baseline vs tuned XGBoost

Create a comparison table:

Model | ROC-AUC | PR-AUC | Precision | Recall | F1 | Brier | Max Prob | High Count | Rollover Top1 | Rollover Top3 | Rollover Top5

Include:

- Baseline XGBoost
- Tuned XGBoost

Also compare:

- average rollover SHAP
- median rollover SHAP
- maximum rollover SHAP

among rollover-positive accounts.

7. Specifically inspect high-risk rollover accounts

Find accounts where:

- risk_band = High
  AND
- partial_rollover_count_12m > 0

or qualifying external rollover activity exists.

For at least 10 such accounts, print:

- account_id
- churn_probability
- risk_band
- partial_rollover_count_12m
- partial_rollover_amount_12m
- days_since_last_partial_rollover
- recent_partial_rollover_count_90d
- recent_partial_rollover_amount_90d
- top 10 positive SHAP features
- primary_churn_driver
- additional_churn_drivers

This is to check whether rollover is genuinely predictive for the riskiest accounts.

8. Check feature interactions

Use XGBoost interaction analysis / SHAP interaction values if practical.

Specifically inspect whether rollover becomes more predictive when combined with:

- contribution cessation / decline
- long gap since last contribution
- retirement / pension enquiry
- investment switch activity
- account tenure
- lower engagement

Do not force these interactions; report only what the model supports.

9. Avoid artificial rollover weighting

Do NOT:

- manually multiply rollover SHAP values
- duplicate rollover columns
- change labels to make rollover appear primary
- lower thresholds only for rollover accounts
- oversample rollover accounts solely to increase importance

Any increase in rollover importance should come naturally from the tuned model and real data.

10. Driver output

After tuning, regenerate:

- primary_churn_driver
- additional_churn_drivers
- driver_count

using the best tuned XGBoost model and fresh SHAP values.

If rollover is materially positive for an account, map it to business-friendly labels such as:

- Partial rollover-out activity
- Recent partial rollover activity
- External rollover activity

Group related rollover features into one business driver where appropriate.

11. Final output

Regenerate:

- member_retention_ml_scoring_output.csv
- member_retention_ml_scoring_sample_15.csv
- member_retention_ml_scoring_validation.md

Keep the fixed risk thresholds:

- High >= 0.70
- Medium >= 0.40 and < 0.70
- Low < 0.40

12. Final conclusion

At the end clearly answer:

1. Did tuned XGBoost improve validation performance?
2. Did rollover SHAP contribution increase?
3. How many rollover-positive accounts now have rollover as:
   - primary driver
   - top 3 driver
   - top 5 driver
4. Did rollover become more important naturally, or is it still weak?
5. Which XGBoost configuration should be retained?
6. Should rollover remain model-driven only, or should a separate business-priority display rule be considered?

Do not claim production readiness.
