Copilot Prompt — Step 10: Prediction Monitoring POC

Create a new Databricks notebook named:

"10_prediction_monitoring_poc.ipynb"

This notebook should continue from the existing MLOps POC.

Current State

The following are already completed:

- Model registered in Unity Catalog
- Version 1 = Champion
- Version 2 = Candidate
- Batch scoring using the Champion alias
- Scoring output schema created
- Scoring results written to Unity Catalog
- Databricks Job/scheduling POC created
- Step 7 CSV output is date-stamped for each scoring run

The current scoring output files follow a pattern similar to:

"Output_Metrics/champion_batch_scoring_output_YYYYMMDD.csv"

Purpose

Demonstrate basic prediction monitoring by comparing two scoring runs and identifying whether model prediction behaviour has changed significantly.

This is a lightweight POC only.

Do not implement feature drift yet.
Do not implement retraining.
Do not change the Champion/Candidate aliases.

Step 10 - Prediction Monitoring

Create a Markdown heading:

"# Step 10 - Prediction Monitoring POC"

Explain in simple terms that prediction monitoring checks whether the model’s output behaviour changes over time.

Examples of changes to monitor:

- average churn probability increases or decreases
- predicted churn rate changes
- High-risk population changes
- total number of scored accounts changes
- prediction distribution changes unexpectedly

1. Import Required Libraries

Import:

import pandas as pd
import numpy as np
import os
import glob
from datetime import datetime

2. Discover Available Scoring Output Files

Look under:

"Output_Metrics/"

for files matching:

"champion_batch_scoring_output_*.csv"

Use Python "glob".

Sort the files by scoring date extracted from the filename.

Display the available scoring files.

If fewer than 2 scoring files exist, print a clear message explaining that at least two scoring runs are required for historical comparison.

For POC purposes only, if only one real scoring file exists, allow creation of a clearly labelled simulated previous run by sampling/modifying the existing data slightly.

Do not overwrite the real scoring file.

If simulated data is used, clearly state:

POC Note: A simulated previous scoring run is being used only to demonstrate prediction monitoring because two historical scoring runs are not yet available.

3. Select Previous and Current Runs

Identify:

- previous scoring file
- latest/current scoring file

Load them into:

previous_df
current_df

Print:

- previous file name
- current file name
- row counts

4. Calculate Monitoring Metrics

For each scoring run calculate:

- total scored records
- average churn probability
- predicted churn count
- predicted churn rate
- Low-risk count
- Medium-risk count
- High-risk count
- High-risk percentage

Store them in dictionaries such as:

previous_metrics
current_metrics

5. Create Comparison Table

Create a dataframe with columns:

- Metric
- Previous Run
- Current Run
- Absolute Change
- Percentage Change

Include:

- Total Scored Records
- Average Churn Probability
- Predicted Churn Rate
- Low Risk Count
- Medium Risk Count
- High Risk Count
- High Risk Percentage

Display the comparison table clearly.

6. Define Simple POC Monitoring Thresholds

Use example thresholds such as:

- Average churn probability change > 10%
- Predicted churn rate change > 10%
- High-risk percentage change > 15%
- Total scored population change > 20%

Clearly add this Markdown note:

POC Note: These monitoring thresholds are examples only. Final alert thresholds must be agreed with the business and ML team during production implementation.

7. Flag Monitoring Alerts

Create simple alert logic.

For each important metric, produce:

- "OK"
- "WARNING"

Example:

Average churn probability: OK
Predicted churn rate: WARNING
High-risk percentage: OK
Population size: OK

Create a dataframe named:

"monitoring_summary"

with columns:

- metric
- previous_value
- current_value
- percentage_change
- threshold
- status

Display it.

8. Prediction Distribution Monitoring

Create a simple table comparing risk-band distribution:

- Low
- Medium
- High

For both previous and current runs show:

- count
- percentage of total

Also calculate the change in percentage points.

Do not create complex statistical tests yet.

9. Optional Visualizations

Create simple charts using built-in pandas/matplotlib only.

Create separate charts for:

1. Previous vs current risk-band percentages
2. Previous vs current predicted churn rate
3. Previous vs current average churn probability

Keep the charts simple and readable.

10. Save Monitoring Results

Save the monitoring summary to:

"Output_Metrics/prediction_monitoring_summary_<current_scoring_date>.csv"

Do not overwrite unrelated files.

Print the saved path.

11. Explain Future Production Monitoring

Add a Markdown section explaining that production prediction monitoring could later be automated after every scheduled scoring run.

Possible future actions include:

- write monitoring metrics to a Delta table
- create dashboards
- configure Databricks SQL alerts
- send notifications
- trigger model investigation when thresholds are breached

Do not implement alerts or notifications in this POC.

12. Final Summary

Print:

- Previous scoring run
- Current scoring run
- Previous predicted churn rate
- Current predicted churn rate
- Previous average churn probability
- Current average churn probability
- Previous High-risk percentage
- Current High-risk percentage
- Number of WARNING statuses

Print:

"Step 10 completed successfully. Prediction monitoring has been demonstrated."

Important Requirements

- Do not retrain any model.
- Do not create new model versions.
- Do not modify aliases.
- Do not implement feature drift yet.
- Do not implement performance monitoring yet.
- Use simple POC thresholds only.
- Clearly identify simulated data if a previous historical scoring file is unavailable.
- Add simple Markdown explanations before each major section.
