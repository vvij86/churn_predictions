Got it. Since the user story already exists, you can split the 3-day exploration work into smaller ADO tasks like this:

Task	Description	Estimate

1. MercerEdgeDB Table & Schema Review	Review the identified MercerEdgeDB tables, understand columns, data types, row volumes, primary/join keys, and table relationships.	6 hrs
2. MercerEdgeDB Data Quality & Historical Coverage Analysis	Check nulls, duplicates, value distributions, date coverage, and whether the available history is sufficient for churn modelling.	6 hrs
3. Churn Driver Identification & Documentation	Identify potential churn-driver columns/features from the explored tables and document findings, assumptions, and recommended fields for feature engineering.	6 hrs


Total = 18 hours = 3 days.

A simple sequence is:

Schema/relationships → Data quality/history → Churn-driver identification/documentation

That division is cleaner for ADO than creating one 18-hour task.
