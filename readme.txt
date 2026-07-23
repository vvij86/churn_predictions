Create a new Python script named train_hist_gradient_boosting.py.

Use the existing prepared files only:

- churn_X_train.csv
- churn_X_test.csv
- churn_y_train.csv
- churn_y_test.csv
- churn_test_account_ids.csv

Do not create a new overall train/test split.
Do not modify any existing Logistic Regression, Decision Tree, Random Forest or XGBoost scripts and output files.

Use the same existing training and untouched test datasets so that model comparison remains fair.

Preprocessing requirements:

- Treat product_id and scheme_id as categorical variables
- Detect dynamically whether each categorical column is present
- Remove any categorical column only if it is constant
- Encode retained categorical columns using OrdinalEncoder with:
  handle_unknown="use_encoded_value"
  unknown_value=-1
- Pass numeric columns without scaling
- Preserve the existing missing-value and no-history indicator handling
- Do not include ACCOUNT_ID as a model feature
- Ensure all transformed model inputs are numeric
- Add validation to prevent target or outcome leakage columns from entering the model

Create a stratified validation split from the existing training data:

- 90% model-training subset
- 10% validation subset
- random_state=42

Use the validation data only for hyperparameter selection.
Keep the existing test dataset untouched until the final model evaluation.

Train HistGradientBoostingClassifier models using:

- random_state=42
- class_weight="balanced"
- early_stopping=True
- validation_fraction=0.1
- n_iter_no_change=20

Test a limited and efficient set of parameter combinations using a manual search or RandomizedSearchCV:

- learning_rate: 0.03, 0.05 and 0.1
- max_iter: 200, 400 and 600
- max_leaf_nodes: 15, 31 and 63
- max_depth: None, 5 and 10
- min_samples_leaf: 20, 50, 100 and 500
- l2_regularization: 0.0, 0.1 and 1.0
- max_bins: 255

Because the dataset is large, do not run every possible combination.
Use a reasonable limited search of approximately 20 to 30 combinations.

For each candidate model, calculate validation:

- ROC-AUC
- PR-AUC / Average Precision
- Accuracy
- Precision for churn class 1
- Recall for churn class 1
- F1-score for churn class 1
- Training time

Select the best model primarily by validation PR-AUC and secondarily by validation F1-score.

After selecting the best hyperparameters:

1. Retrain the final preprocessing and HistGradientBoosting model using the full existing training dataset.
2. Evaluate it only once on the untouched test dataset.
3. Print the selected hyperparameters.
4. Print:
   - ROC-AUC
   - PR-AUC / Average Precision
   - Accuracy
   - Precision for churn class 1
   - Recall for churn class 1
   - F1-score for churn class 1
5. Print the confusion matrix and classification report.
6. Print training time and prediction time.
7. Print the number of boosting iterations used by the final model where available.

Save the following output files:

- hist_gradient_boosting_model_comparison.csv
- hist_gradient_boosting_metrics.csv
- hist_gradient_boosting_test_predictions.csv
- hist_gradient_boosting_pipeline.joblib

The test prediction file must contain:

- ACCOUNT_ID
- actual_target
- predicted_target
- churn_probability

HistGradientBoostingClassifier does not provide standard tree feature_importances_.

Therefore, calculate feature importance using permutation importance on a reproducible sample of the test dataset:

- Use random_state=42
- Use a manageable stratified test sample, such as a maximum of 20,000 rows
- Use scoring="average_precision"
- Use 5 repeats
- Do not calculate permutation importance on the entire 158,000-row test dataset if it causes excessive runtime

Save:

- hist_gradient_boosting_permutation_importance.csv
- hist_gradient_boosting_top_churn_drivers.csv

The importance files should contain:

- feature_name
- importance_mean
- importance_std
- driver_group
- rank

Classify each feature as either:

- Behavioural
- Product/Scheme association

Save the top 20 overall features.

Separately print and save the top 10 behavioural churn drivers, excluding product_id and scheme_id.

Clearly state:

- Permutation importance shows the model’s predictive association with churn
- It does not prove that the feature causes churn

Read and compare available metrics from:

- logistic_regression_metrics.csv
- decision_tree_metrics.csv
- random_forest_metrics.csv
- xgboost_metrics.csv, if available
- hist_gradient_boosting_metrics.csv

Create or update:

model_comparison_all_models.csv

Include for every available model:

- model
- ROC-AUC
- PR-AUC
- Accuracy
- Precision for churn class 1
- Recall for churn class 1
- F1-score for churn class 1
- Training time
- Prediction time

Clearly identify:

- Best model by ROC-AUC
- Best model by PR-AUC
- Best model by recall
- Best model by F1-score
- Fastest prediction model
- Best overall balanced model

Do not automatically declare HistGradientBoosting as the winner.
Base the recommendation only on the measured test results.

Add clear comments, error handling and validation for:

- missing input files
- missing required columns
- target values other than 0 and 1
- ACCOUNT_ID mismatch
- train/test schema mismatch
- duplicate account IDs
- target leakage columns
- unsupported scikit-learn parameters or version differences

Run the script after creating it and report:

- selected hyperparameters
- final test metrics
- generated files
- comparison with the previous models
- recommended model based on PR-AUC, F1, recall, runtime and explainability
