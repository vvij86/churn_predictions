I have already generated an Excel workbook called:

model_scalability_benchmark.xlsx

It contains detailed timing and memory results for:

Logistic Regression

Decision Tree

Random Forest

XGBoost

HistGradientBoosting


The workbook has multiple runs for these dataset sizes:

Original dataset: approximately 793,915 rows

1,000,000 rows

1,500,000 rows

Other sizes if present


I need a brief, documentation-ready summary, not the full raw benchmark table.

Required output

Create a new Excel sheet called:

Documentation_Summary

Do not modify or delete the existing sheets.

1. Create a concise summary table

Create one row per model and dataset size using the average of all successful runs.

Include only these columns:

Dataset size
Model
Average preprocessing time (seconds)
Average training time (seconds)
Average prediction time (seconds)
Average total time (seconds)
Average peak memory (MB)
Status

Round timing values to 2 decimal places and memory values to the nearest whole MB.

Order the rows by:

1. Dataset size


2. Model name



2. Create a Random Forest focused table

Because Random Forest is the main focus of the scalability POC, create a second table called:

Random Forest Scalability Summary

Include:

Dataset size
Training rows
Test rows
Average preprocessing time
Average training time
Average prediction time
Average total time
Average peak memory
Training time increase versus original
Prediction time increase versus original

Calculate the increase versus the original dataset as both:

additional seconds;

percentage increase.


3. Create a short findings section

Below the tables, generate 5 to 7 concise findings suitable for the final POC document.

Cover:

how training time changed as rows increased;

how prediction time changed;

which model trained fastest;

which model predicted fastest;

whether Random Forest remained operationally practical;

whether memory use increased;

why these results are indicative only.


Use wording similar to:

> The benchmark used duplicated DEV records to simulate larger data volumes. Therefore, the results are valid for runtime and memory testing only and should not be used to assess model accuracy or production generalisation.



4. Create a small executive table

Create a third table with only one row per dataset size for Random Forest:

Dataset size
Average training time
Average prediction time
Average peak memory
Operational assessment

Use simple operational assessments such as:

Low impact

Manageable

Higher resource requirement

Requires production infrastructure testing


Base the assessment on the relative growth in runtime and memory, and state clearly that the assessment is provisional.

5. Add charts

Create only two charts:

1. Random Forest training time versus dataset size


2. Random Forest prediction time versus dataset size



Use averages from successful runs only.

6. Produce documentation text

Also create a plain-text file:

model_scalability_documentation_summary.txt

Include:

POC objective;

test approach;

dataset sizes;

brief Random Forest results;

comparison across models;

limitations;

recommendation.


Keep the text under 500 words and make it suitable for copying into the final model-evaluation document.

Important rules

Use only successful benchmark rows.

Average repeated runs before producing the summary.

Do not overwrite the original workbook.

Save the updated copy as:


model_scalability_benchmark_documentation.xlsx

Preserve all original sheets.

Add the new Documentation_Summary sheet at the beginning.

Do not change any source benchmark values.

Clearly state that the larger datasets were created using duplicated SonataODS DEV records.

Do not draw conclusions about accuracy from duplicated records.

Focus the final summary mainly on training time, prediction time and memory scalability.


At the end, explain:

1. which source columns were used;


2. how averages were calculated;


3. how failed runs were excluded;


4. where the new files were saved.

