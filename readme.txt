Create a new Python script named train_random_forest.py.

Use the existing files only:

- churn_X_train.csv
- churn_X_test.csv
- churn_y_train.csv
- churn_y_test.csv
- churn_test_account_ids.csv

Do not create a new train/test split.
Do not modify the Logistic Regression or Decision Tree scripts and outputs.

Use the same preprocessing logic already used in train_decision_tree.py:

- Treat product_id and scheme_id as categorical columns
- Use OneHotEncoder(handle_unknown="ignore")
- Pass numeric features without scaling
- Preserve the existing missing-value and no-history handling

Train and compare RandomForestClassifier models using:

- n_estimators: 100 and 200
- max_depth: 10, 15 and None
- min_samples_leaf: 10, 50, 100 and 500
- max_features: "sqrt"
- class_weight: "balanced"
- random_state: 42
- n_jobs: -1

Evaluate every combination on the existing test set using:

- ROC-AUC
- PR-AUC / Average Precision
- Accuracy
- Precision for churn class 1
- Recall for churn class 1
- F1-score for churn class 1

Select the best model primarily by PR-AUC and secondarily by F1-score.

For the final selected model:

1. Print the selected hyperparameters.
2. Print confusion matrix and classification report.
3. Save all parameter results to:
   random_forest_model_comparison.csv
4. Save final metrics to:
   random_forest_metrics.csv
5. Save predictions with ACCOUNT_ID, actual_target, predicted_target and churn_probability to:
   random_forest_test_predictions.csv
6. Save the full trained preprocessing and model pipeline to:
   random_forest_pipeline.joblib
7. Save all transformed feature importances to:
   random_forest_feature_importance.csv
8. Save the top 20 feature importances to:
   random_forest_top_churn_drivers.csv
9. Separately show the top 10 behavioural drivers, excluding product_id and scheme_id.
10. Add clear comments, validations and error handling.

Then compare:

- Logistic Regression
- Decision Tree
- Random Forest

Read metrics from:

- logistic_regression_metrics.csv
- decision_tree_metrics.csv
- random_forest_metrics.csv

Create:

model_comparison_all_models.csv

Include ROC-AUC, PR-AUC, Accuracy, Precision, Recall and F1-score for all three models.

Clearly identify:

- Best model by PR-AUC
- Best model by recall
- Best model by F1-score
- Training and prediction time where available

Do not claim feature importance proves business causation. State that it represents model association only.

Run the script and report the selected hyperparameters, final metrics, generated files and the overall best model.
