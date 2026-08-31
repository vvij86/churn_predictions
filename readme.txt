Copilot Prompt — Step 11: Data / Feature Drift Monitoring POC

Create a new Databricks notebook named:

"11_feature_drift_monitoring_poc.ipynb"

This notebook should continue from the existing MLOps POC.

Current State

Already completed:

- Model registration in Unity Catalog
- Version 1 = Champion
- Version 2 = Candidate
- Batch scoring using "@Champion"
- Model output schema
- Unity Catalog scoring output table
- Databricks Job scheduling POC
- Prediction monitoring POC

Existing datasets:

Training data:

"Training_ds/churn_X_train.csv"

Current scoring/test data:

"Test_ds/churn_X_test.csv"

Purpose

Demonstrate basic feature drift monitoring by comparing the feature distribution used during model development/training against the current scoring dataset.

The purpose is to identify whether input data characteristics have changed significantly.

Do not retrain the model.
Do not change Champion/Candidate aliases.
Do not create another model version.

Step 11 - Data / Feature Drift Monitoring

Create a Markdown heading:

"# Step 11 - Data / Feature Drift Monitoring POC"

Explain in simple terms:

Feature drift means that the data being given to the model today looks different from the data the model originally learned from.

Example:

If average withdrawal count during training was 2 but current scoring data has an average of 8, that feature may have drifted.

Explain that feature drift does not automatically mean the model is wrong, but it indicates that investigation may be required.

1. Import Required Libraries

Import:

import pandas as pd
import numpy as np

Also import any simple statistical utilities required from scipy only if scipy is already available.

Do not install new libraries.

2. Load Reference and Current Data

Load:

"Training_ds/churn_X_train.csv"

into:

"reference_df"

Load:

"Test_ds/churn_X_test.csv"

into:

"current_df"

Explain:

- "reference_df" represents the model development/training feature distribution
- "current_df" represents the current scoring feature distribution for this POC

Print:

- reference row count
- current row count
- number of columns
- common columns

3. Validate Feature Compatibility

Identify:

- common columns
- columns present only in reference
- columns present only in current

Display these clearly.

Only compare features that exist in both datasets.

Do not compare target columns.

Do not compare identifiers such as account_id if present.

Create a configurable exclusion list for:

- identifiers
- target fields
- obvious metadata fields

4. Separate Numeric and Categorical Features

Automatically identify:

- numeric columns
- categorical/string columns

Print:

- number of numeric features
- number of categorical features

For this POC, prioritize numeric feature drift.

5. Numeric Feature Drift Summary

For every numeric feature, calculate:

Reference data:

- mean
- median
- standard deviation
- minimum
- maximum
- null percentage

Current data:

- mean
- median
- standard deviation
- minimum
- maximum
- null percentage

Calculate:

- absolute mean difference
- percentage mean change
- null percentage change

Handle cases where the reference mean is zero safely.

Create a dataframe named:

"numeric_drift_summary"

6. Define Simple POC Drift Thresholds

Use simple example thresholds:

- Mean percentage change <= 10% → "LOW"
- Mean percentage change > 10% and <= 25% → "MEDIUM"
- Mean percentage change > 25% → "HIGH"

Also flag a feature if null percentage changes by more than 10 percentage points.

Clearly state:

POC Note: These drift thresholds are examples only. Production thresholds must be determined based on feature behaviour, statistical analysis, business context, and model sensitivity.

7. Assign Drift Status

For each numeric feature assign:

- "NO_DRIFT"
- "WARNING"
- "HIGH_DRIFT"

Create columns such as:

- feature_name
- reference_mean
- current_mean
- mean_change_pct
- reference_null_pct
- current_null_pct
- null_change_pct_points
- drift_status

Sort with "HIGH_DRIFT" features first.

Display the top drifted features.

8. Categorical Feature Drift

For categorical features, perform a simple comparison.

For each categorical feature:

- reference distinct count
- current distinct count
- top category in reference
- top category percentage in reference
- top category in current
- top category percentage in current

Also identify:

- new categories present in current but not reference
- categories missing from current

Create:

"categorical_drift_summary"

Do not use complex statistical testing.

9. Create Overall Drift Summary

Calculate:

- total numeric features checked
- number with NO_DRIFT
- number with WARNING
- number with HIGH_DRIFT
- number of categorical features checked
- number containing new categories

Print an overall summary.

Example:

Numeric features checked: 25
No drift: 18
Warning: 5
High drift: 2
Categorical features checked: 4
Features with new categories: 1

10. Visualize Most Drifted Features

Select the top 5 numeric features by absolute mean percentage change.

Create simple bar charts using matplotlib.

Show:

- feature name
- reference mean
- current mean

Keep charts simple and readable.

Do not use seaborn.

11. Save Drift Monitoring Results

Save:

"numeric_drift_summary"

to:

"Output_Metrics/feature_drift_numeric_summary_<current_date>.csv"

Save:

"categorical_drift_summary"

to:

"Output_Metrics/feature_drift_categorical_summary_<current_date>.csv"

Use current UTC date in "YYYYMMDD" format.

Do not overwrite unrelated files.

Print saved paths.

12. Optional Unity Catalog Drift Table Design

Add a Markdown-only section explaining that in production the drift results could be persisted into tables such as:

"superdata_au_dev.mlops.feature_drift_monitoring"

Possible columns:

- scoring_date
- feature_name
- reference_value
- current_value
- change_percentage
- drift_status
- model_name
- model_version

Do not create this production monitoring table automatically in this POC.

13. Explain Relationship to Prediction Monitoring

Add Markdown explaining:

Prediction Monitoring asks:

"Has the model output changed?"

Feature Drift Monitoring asks:

"Has the model input data changed?"

Example:

If predicted churn suddenly increases, feature drift monitoring can help identify whether changes in contribution, withdrawal, tenure, or other input features may be contributing to that change.

14. Explain Production Improvements

Add Markdown explaining that production drift monitoring could later use more robust methods such as:

- Population Stability Index (PSI)
- Kolmogorov-Smirnov test
- Jensen-Shannon divergence
- distribution-based monitoring
- Databricks monitoring capabilities if available

Do not implement these advanced methods in this notebook.

15. Final Summary

Print:

- reference dataset
- current dataset
- number of numeric features checked
- number of warning features
- number of high-drift features
- top 5 drifted features
- number of categorical features with new categories

Print:

"Step 11 completed successfully. Data and feature drift monitoring has been demonstrated."

Important Requirements

- Do not retrain the model.
- Do not modify model aliases.
- Do not create another model version.
- Do not perform prediction monitoring again.
- Do not use Hyperopt.
- Do not install extra libraries.
- Keep the POC implementation simple.
- Clearly label all thresholds as POC examples.
- Add Markdown explanations before every major section.
