Create a new Python script named train_decision_tree.py.

Use the existing prepared files:

- churn_X_train.csv
- churn_X_test.csv
- churn_y_train.csv
- churn_y_test.csv
- churn_test_account_ids.csv

Use the same preprocessing approach already used in train_logistic_regression.py:

- Treat product_id and scheme_id as categorical columns
- One-hot encode categorical columns with handle_unknown="ignore"
- Pass numeric columns through without scaling because scaling is not required for a decision tree
- Preserve the same missing-value and no-history handling already present in the existing workflow
- Do not create a new train/test split
- Do not modify the existing logistic regression files

Train a DecisionTreeClassifier with:

- random_state=42
- class_weight="balanced"
- max_depth values: 3, 5, 8, 10, 15 and None
- min_samples_leaf values: 1, 10, 50, 100 and 500

Evaluate every parameter combination on the existing test set using:

- ROC-AUC
- PR-AUC / Average Precision
- Accuracy
- Precision for churn class 1
- Recall for churn class 1
- F1-score for churn class 1

Select the best model primarily using PR-AUC, and use F1-score as the secondary metric.

For the selected model:

1. Print the chosen hyperparameters.
2. Print the confusion matrix and classification report.
3. Save all parameter-comparison results to:
   decision_tree_model_comparison.csv
4. Save final metrics to:
   decision_tree_metrics.csv
5. Save test predictions with:
   ACCOUNT_ID,
   actual_target,
   predicted_target,
   churn_probability
   to decision_tree_test_predictions.csv
6. Save the complete preprocessing and trained model pipeline to:
   decision_tree_pipeline.joblib
7. Extract and save feature importance for all transformed features to:
   decision_tree_feature_importance.csv
8. Save the top 20 feature importances to:
   decision_tree_top_churn_drivers.csv
9. Separately identify the top 10 behavioural features, excluding product_id and scheme_id one-hot features.
10. Add clear error handling, comments and console summaries.

Also compare the final decision-tree metrics against logistic_regression_metrics.csv and create:

model_comparison_logistic_vs_decision_tree.csv

Include both models and clearly state which model performs better for:

- ROC-AUC
- PR-AUC
- Precision
- Recall
- F1-score

Do not claim that feature importance proves causation. Mention that it shows model association only.

Run the script after creating it and report the generated files and the final comparison results.
