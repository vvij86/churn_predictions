I already have the churn modelling dataset exported from SQL Server as a CSV file with headers.

The file name is:

dataset.csv

dataset.csv contains the final output of the validated churn dataset query.

Create a beginner-friendly Python script using pandas to validate this file.

Requirements:

1. Keep the file path in an editable variable:



csv_file = r"dataset.csv"

2. Read the CSV using the existing headers.


3. Print:

row count

column count

all column names

first five rows

data types



4. Show null count and null percentage for every column.


5. Check whether account_id contains duplicates or null values.


6. Display target_churn counts and percentages.


7. Confirm that target_churn contains only 0 and 1.


8. Identify constant columns.


9. Identify columns with more than 80% null values.


10. Check numeric columns for infinite values.


11. Show the total memory usage of the dataframe.


12. Save the validation summary as:



churn_dataset_validation_summary.csv

Do not train or evaluate any ML model yet.

Add clear comments and explain how to run the script from VS Code.
