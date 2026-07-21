Yes. Use this prompt in Copilot:

Create a new Python file named:

create_logistic_model_visuals.py

Use these existing files:

logistic_regression_metrics.csv
logistic_regression_test_predictions.csv
logistic_regression_churn_drivers.csv
logistic_regression_top_churn_drivers.csv

Create beginner-friendly statistical visualizations for the Logistic Regression churn model so that a non-technical stakeholder can understand the results.

Requirements:

1. Read all available input CSV files and validate the required columns.


2. Create and save the following charts as separate PNG files:



01_confusion_matrix.png
02_roc_curve.png
03_precision_recall_curve.png
04_model_metrics_summary.png
05_top_behavioural_churn_drivers.png
06_churn_probability_distribution.png
07_threshold_precision_recall.png

3. Confusion matrix:



Show:

Correctly predicted non-churn

False churn alerts

Missed churn cases

Correctly predicted churn


Display both count and percentage inside each cell.

Use business-friendly labels instead of only TN, FP, FN and TP.

Add a subtitle explaining:

missed churn cases are actual churn accounts predicted as retained;

false alerts are retained accounts predicted as churn.



4. ROC curve:



Use actual_target and churn_probability.

Plot the no-skill diagonal.

Display the ROC-AUC value clearly.

Add a simple explanation in the title or subtitle:

“Higher AUC means better separation between churn and non-churn accounts.”



5. Precision–Recall curve:



Use actual_target and churn_probability.

Display Average Precision / PR-AUC.

Include the churn prevalence baseline.

Add a simple explanation:

“This chart is especially useful because churn cases are less common.”



6. Model metrics summary:



Create a bar chart for:

ROC-AUC

PR-AUC

Accuracy

Precision

Recall

F1-score


Show the metric value above each bar.

Add a plain-English note below the chart:

Precision = how reliable the churn alerts are

Recall = how many actual churn cases were identified

F1-score = balance between precision and recall



7. Top behavioural churn drivers:



Use only rows where driver_group = "Behavioural driver".

Exclude product_id and scheme_id associations.

Show the top 15 features by absolute_coefficient.

Use a horizontal bar chart.

Clearly show whether each feature:

increases churn risk;

reduces churn risk.


Replace technical column names with readable labels, for example:

partial_withdrawal_count_12m → Partial withdrawal frequency

days_since_last_partial_withdrawal_12m → Time since last partial withdrawal

account_txn_count_12m → Account transaction frequency

reversal_txn_count_12m → Reversal transaction frequency


Add a footnote:

“These are model associations, not confirmed business causes.”



8. Churn probability distribution:



Show separate probability distributions for:

actual non-churn accounts;

actual churn accounts.


Mark the default decision threshold of 0.50.

Add a plain-English explanation:

“Accounts to the right of the threshold are classified as churn.”



9. Threshold precision-recall chart:



Calculate precision, recall and F1-score across thresholds from 0.10 to 0.90.

Plot all three lines.

Mark the current threshold of 0.50.

Highlight the threshold with the highest F1-score.

Print the best F1 threshold and corresponding precision, recall and F1-score.


10. Use clear titles, large fonts and readable labels suitable for PowerPoint or Confluence.


11. Do not use unexplained abbreviations in chart titles.


12. Add a short business interpretation below each chart where possible.


13. Save all charts in a new folder:



model_visuals

14. Create a summary CSV named:



model_visuals_summary.csv

with:

chart_name
purpose
business_interpretation
output_file

15. Print a final summary listing all generated chart files.


16. Add clear comments and error handling.


17. Do not retrain the model.


18. Run using:



python create_logistic_model_visuals.py
