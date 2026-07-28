Yes. That is a valid technical scalability test.

Ask Copilot to:

duplicate the existing model-safe training and test records to create larger row counts;

keep the same feature columns;

generate new synthetic account IDs so duplicate IDs do not break validation;

benchmark every model using the same dataset sizes;

measure loading, preprocessing, training and prediction time;

capture memory usage if possible;

export the results to an Excel workbook.


Important caveat:

> Duplicate data can test runtime, memory and scalability, but it must not be used to judge model accuracy because it does not add new behavioural patterns.



You can paste this prompt into Copilot:


---

Create a Python benchmarking script for the churn-model POC.

Existing files

Use these prepared files:

churn_X_train.csv
churn_X_test.csv
churn_y_train.csv
churn_y_test.csv
churn_train_account_ids.csv
churn_test_account_ids.csv

The project also contains training scripts and saved configurations for:

Logistic Regression
Decision Tree
Random Forest
XGBoost
HistGradientBoosting

Objective

Test how model training and prediction times change as the number of records increases.

This is a technical volume and timing test only. Synthetic duplicated records must not be used to make conclusions about model accuracy or business performance.

Dataset sizes

Create benchmark datasets of approximately:

Current original size
1,000,000 rows
1,500,000 rows
2,000,000 rows
3,000,000 rows

If the machine does not have enough memory, skip the failed size safely, record the error, and continue with the next model or smaller size.

Synthetic data creation rules

1. Duplicate existing rows to reach each target size.


2. Shuffle the repeated rows.


3. Preserve the relationship between X, y, and account IDs.


4. Generate unique synthetic account IDs for every duplicated row.


5. Do not change feature values or targets.


6. Clearly label each dataset as synthetic volume-expanded data.


7. Do not write all expanded datasets to disk unless required; prefer generating them in memory to reduce storage use.


8. Use a fixed random seed for reproducibility.



Models

Benchmark:

Logistic Regression
Decision Tree
Random Forest
XGBoost
HistGradientBoosting

Use the same final hyperparameters selected during the original POC. Do not run hyperparameter grid search again, because this test is for scalability rather than model selection.

For Random Forest, capture:

n_estimators
max_depth
min_samples_leaf
n_jobs

Timing measurements

For each model and dataset size, record separately:

data expansion time
preprocessing fit/transform time
model training time
prediction time
total runtime
prediction rows per second

Measure time using time.perf_counter().

Run prediction on the corresponding expanded test dataset. Use a consistent train/test proportion for all benchmark sizes.

Memory measurements

Where possible, record:

process memory before training
peak memory during training
memory after training

Use psutil or another reliable Python approach.

Also record:

success or failure status
error message

The script must catch memory and model errors instead of terminating the entire benchmark.

Fair comparison requirements

1. Use the same feature schema for all models.


2. Use the same expanded dataset for all models at a given size.


3. Use the same random seed.


4. Do not include ACCOUNT_ID as a model feature.


5. Treat product_id and scheme_id using the same categorical preprocessing as the existing model pipelines.


6. Delete temporary models and dataframes between runs and call garbage collection to reduce memory carry-over.


7. Run each successful test at least three times if practical and calculate:

average time;

minimum time;

maximum time;

standard deviation.



8. Record machine information:

CPU count;

total RAM;

Python version;

operating system.




Model metrics

Accuracy metrics are secondary because the rows are duplicated. Record them only as a consistency check:

ROC-AUC
PR-AUC
precision
recall
F1-score

Add a note in the output that these metrics are not valid evidence of improved model performance on synthetic duplicated data.

Excel output

Create:

model_scalability_benchmark.xlsx

Include these sheets:

Benchmark_Summary

One row per model and dataset size, with columns such as:

model
target_total_rows
train_rows
test_rows
run_number
status
data_expansion_seconds
preprocessing_seconds
training_seconds
prediction_seconds
total_seconds
predictions_per_second
memory_before_mb
peak_memory_mb
memory_after_mb
roc_auc
pr_auc
precision
recall
f1
error_message

Aggregated_Results

Average, minimum, maximum and standard deviation by model and dataset size.

Random_Forest_Detail

Random Forest settings and timing results.

Environment

CPU, RAM, Python version, package versions and test date.

Notes

State clearly:

The larger datasets were created by duplicating DEV records.
The results are suitable only for runtime, memory and scalability testing.
They are not suitable for assessing production accuracy, data diversity or model generalisation.

Charts

Add Excel charts for:

1. Training time versus number of training rows, one series per model.


2. Prediction time versus number of test rows, one series per model.


3. Peak memory versus dataset size.


4. Random Forest training time versus number of records.



Final response

After writing the code, explain:

1. How the synthetic datasets are created.


2. How account IDs remain unique.


3. How timings are measured.


4. How memory failures are handled.


5. Why duplicated data cannot be used to assess accuracy.


6. How to run the script.


7. The expected Excel output structure.



Save the Python script as:

benchmark_model_scalability.py


---

For your first run, start with the original size, 1 million and 1.5 million rows. Jumping straight to 3 million across five models—especially Random Forest—may make the laptop reconsider its career choices.
