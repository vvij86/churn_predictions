Create a new Python script named train_xgboost.py.

Use the existing prepared files only:

- churn_X_train.csv
- churn_X_test.csv
- churn_y_train.csv
- churn_y_test.csv
- churn_test_account_ids.csv

Do not create a new train/test split.
Do not modify any Logistic Regression, Decision Tree or Random Forest scripts or outputs.

Install xgboost in the existing virtual environment only if it is not already installed.

Use the same feature-processing approach used in the previous models:

- Treat product_id and scheme_id as categorical columns
- Use OneHotEncoder(handle_unknown="ignore")
- Pass numeric columns without scaling
- Preserve the existing missing-value and no-history handling
- Keep the test dataset completely untouched until final evaluation

Create a stratified validation split from the existing training dataset:

- 90% model-training subset
- 10% validation subset
- random_state=42

Use the validation subset for hyperparameter selection and early stopping.
Do not select hyperparameters using the test dataset.

Calculate scale_pos_weight automatically using:

number of class 0 training rows / number of class 1 training rows

Train XGBClassifier models using tree_method="hist", random_state=42, n_jobs=-1 and eval_metric="logloss".

Test the following parameter combinations:

- n_estimators: 200, 400 and 600
- max_depth: 3, 5 and 7
- learning_rate: 0.03, 0.05 and 0.1
- min_child_weight: 1, 5 and 10
- subsample: 0.8
- colsample_bytree: 0.8
- reg_alpha: 0 and 0.1
- reg_lambda: 1
- scale_pos_weight: calculated value

Use early stopping with approximately 30 rounds where supported.

Because the dataset is large, use an efficient search strategy such as RandomizedSearchCV or a manually limited parameter search rather than running every possible combination.

Select the best model primarily using validation PR-AUC / Average Precision and secondarily using validation F1-score.

After selecting the best hyperparameters:

1. Retrain the final XGBoost pipeline using the full existing training dataset.
2. Evaluate it once on the untouched test dataset.
3. Print the selected hyperparameters.
4. Print ROC-AUC, PR-AUC, accuracy, churn precision, churn recall and churn F1-score.
5. Print the confusion matrix and classification report.
6. Print training and prediction time.

Save the outputs as:

- xgboost_model_comparison.csv
- xgboost_metrics.csv
- xgboost_test_predictions.csv
- xgboost_pipeline.joblib
- xgboost_feature_importance.csv
- xgboost_top_churn_drivers.csv

The prediction file must contain:

- ACCOUNT_ID
- actual_target
- predicted_target
- churn_probability

For feature importance:

- Save all transformed feature names and importance values
- Save the top 20 overall features
- Separately print and save the top 10 behavioural features excluding product_id and scheme_id one-hot features
- State clearly that feature importance shows model association and does not prove business causation

Read and compare metrics from:

- logistic_regression_metrics.csv
- decision_tree_metrics.csv
- random_forest_metrics.csv
- xgboost_metrics.csv

Create:

model_comparison_all_models.csv

Include for all four models:

- ROC-AUC
- PR-AUC
- Accuracy
- Precision for churn
- Recall for churn
- F1-score for churn
- Training time
- Prediction time

Clearly identify:

- Best model by PR-AUC
- Best model by recall
- Best model by F1-score
- Best overall balanced model

Do not automatically declare XGBoost the winner. Base the recommendation only on the measured test results.

Add clear comments, validations and error handling.

Run the script after creating it and report:

- selected XGBoost hyperparameters
- final test metrics
- generated output files
- comparison against the previous three models
- overall recommended model
