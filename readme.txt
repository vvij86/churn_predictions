I am now starting Phase 2 of ML-focused data exploration for customer churn / retention analytics.

Phase 1 is already complete and validated.

The current workspace already contains:

All_table_scripts.sql

All_tables_null_or_blank_count.xlsx

MercerEdge_ML_Churn_Driver_EDA.xlsx

existing Python scripts created for Phase 1

.env file with SQL Server configuration

Windows Authentication based SQL connectivity


Phase 1 has already confirmed:

all 17 tables are present

all DDL columns are captured

no source columns are missing

Overview counts reconcile

every source column has a Phase 1 churn assessment


Do NOT rebuild Phase 1 from scratch.

The goal of Phase 2 is to profile actual database values and validate the Phase 1 feature assessments using real data evidence.

This is still exploratory analysis.

Do NOT train any ML model yet.

Important approach

Use the existing Phase 1 workbook as the baseline.

Create a NEW workbook:

MercerEdge_ML_Churn_Driver_EDA_Phase2.xlsx

Do not overwrite the Phase 1 workbook.

Preserve all Phase 1 columns and assessments.

Add Phase 2 profiling fields and recommendations based on actual SQL Server data.

Database connection

Use the existing .env configuration.

Use:

ENABLE_DB_PROFILING=True

Connect to SQL Server using:

pyodbc

Windows Trusted Authentication

existing SQL_SERVER

existing SQL_DATABASE

existing SQL_DRIVER


Do not hard-code credentials.

Do not pull complete tables into pandas.

Use SQL aggregate queries and small sample queries wherever possible.

The profiling must be efficient and safe for large tables.

Tables in scope

Profile the same 17 tables used in Phase 1.

Use the Phase 1 workbook / existing code to determine the exact list.

Do not add or remove tables.

Phase 2 profiling required for every column

For every source column, capture where technically appropriate:

1. Row Count


2. Null Count


3. Null %


4. Blank Count


5. Blank %


6. Distinct Count


7. Approximate Cardinality %


8. Sample Values


9. Minimum Value


10. Maximum Value


11. Mean


12. Median


13. Standard Deviation


14. Zero Count


15. Zero %


16. Negative Count


17. Minimum Date


18. Maximum Date


19. Date Coverage Observation


20. Constant / Near Constant Flag


21. Cardinality Level


22. Potential Data Quality Issue


23. Phase 2 Usability


24. Phase 2 Recommendation


25. Phase 2 Reason



Only calculate metrics that are meaningful for the datatype.

For example:

numeric columns:

min

max

mean

median where practical

standard deviation

zero count

negative count


date/datetime columns:

minimum date

maximum date

null %

distinct count

date coverage


categorical/text columns:

distinct count

cardinality %

5-10 representative values

blank %

top values where practical


identifiers:

distinct count

uniqueness %

null %

but do not recommend them as predictive features simply because they are unique



Sample values

Capture only a small number of representative values.

Do NOT export full data.

For text/category columns, capture approximately 5-10 distinct non-null values.

Avoid exposing unnecessary raw PII.

For columns such as:

customer name

email

phone

postal address

identifiers


do NOT put actual sensitive values into the workbook.

Instead use safe descriptions such as:

Values present

Mostly unique

Format resembles email

Format resembles phone

High-cardinality identifier


Do not expose personal data unnecessarily.

Distinct count and cardinality

Calculate:

Cardinality % = Distinct Count / Non-Null Row Count * 100

Classify Cardinality Level as:

Constant

Very Low

Low

Medium

High

Very High


Use sensible rules.

Examples:

1 distinct value → Constant

very few categories → Low

nearly unique values → Very High


Do not automatically reject high-cardinality numeric measures or dates.

Interpret them based on business meaning.

Constant and near-constant columns

Flag:

constant columns

near-constant categorical columns

columns dominated by one value


These may have little predictive value.

Do not remove them from the workbook.

Mark them for review or exclusion.

Date profiling

For every date/datetime column:

Capture:

Min Date

Max Date

Null %

distinct date count where appropriate


Add a Date Coverage Observation such as:

Good historical coverage

Only recent/current records

Limited historical coverage

Future dates detected

Mostly null

Requires temporal validation


Do NOT infer usefulness solely from min/max date.

Remember that churn modelling must avoid future information.

Actual value validation

Use Phase 2 to validate whether Phase 1 assumptions were reasonable.

Examples:

If Phase 1 says:

activityType -> Maybe / Investigate

then inspect real categories and update the Phase 2 recommendation based on actual values.

If Phase 1 says:

annualPremium -> Yes

validate whether:

it has sufficient non-null coverage

it is mostly zero

it has meaningful variation

it contains extreme values

it appears useful as a raw or derived feature


If Phase 1 says:

status -> Yes

inspect the actual status values and assess whether any status appears to represent churn itself.

Leakage assessment

Re-evaluate leakage risk using actual data values and date coverage.

Pay particular attention to fields related to:

closure

exit

termination

cancellation

inactive status

rollover-out completion

full withdrawal

account balance at exit

post-exit status

final transaction

future-dated records


Do NOT use any value that is only available after churn.

Add:

Phase 2 Leakage Observation

with values such as:

No obvious leakage

Potential leakage

High leakage risk

Requires as_of_date validation

Appears post-outcome

Timing unclear


Phase 2 usability

For every column assign one:

Confirmed Candidate

Candidate with Transformation

Investigate Further

Exclude

Join Key Only


This must be based on:

Phase 1 reasoning

actual data quality

actual value variation

cardinality

date coverage

leakage risk

business interpretability


Phase 2 recommendation examples

Use recommendations such as:

Use directly

Use after encoding

Derive tenure

Derive age

Derive presence flag

Aggregate over time

Calculate recency

Calculate frequency

Calculate trend

Calculate rolling amount

Convert to category

Combine rare categories

Investigate business meaning

Validate against as_of_date

Join key only

Exclude due to 100% null

Exclude due to constant value

Exclude due to leakage

Exclude raw PII

Consider derived indicator only


Important ML principle

Do NOT say a feature is predictive simply because it has good data quality.

Phase 2 is validating whether a source column is technically and logically usable.

Actual predictive power will only be established later during modelling/statistical analysis.

Use wording such as:

suitable candidate

potential churn driver

requires transformation

requires temporal validation

requires business validation

technically usable

not suitable as raw feature


Workbook structure

Create:

MercerEdge_ML_Churn_Driver_EDA_Phase2.xlsx

Include:

1. Overview


2. Validation


3. one worksheet for each of the 17 tables



Preserve the original Phase 1 columns.

Append Phase 2 columns after them.

Recommended Phase 2 columns:

Distinct Count

Cardinality %

Cardinality Level

Sample Values / Value Pattern

Min Value

Max Value

Mean

Median

Std Dev

Zero Count

Zero %

Negative Count

Min Date

Max Date

Date Coverage Observation

Constant / Near Constant

Potential Data Quality Issue

Phase 2 Leakage Observation

Phase 2 Usability

Phase 2 Recommendation

Phase 2 Reason


Use Not applicable where a metric does not make sense for the datatype.

Do not use misleading zeros for non-applicable metrics.

Overview worksheet

Update the Overview so it includes Phase 2 summary information per table.

Include:

Table Name

Total Columns

Confirmed Candidate

Candidate with Transformation

Investigate Further

Exclude

Join Key Only

Constant Columns

100% Null Columns

High Cardinality Columns

High Leakage Risk Columns

Limited Date Coverage Columns

Key Candidate Feature Groups

General Phase 2 Comments


Calculate all counts programmatically.

Do not hard-code them.

Validation worksheet

Validate:

1. all 17 tables still exist


2. every Phase 1 source column still exists


3. no Phase 1 column is dropped


4. Phase 2 output row count equals Phase 1 row count for every table


5. no duplicate rows are introduced


6. all Phase 2 Usability fields are populated


7. all Phase 2 Recommendation fields are populated


8. all Overview counts reconcile


9. all SQL profiling failures are reported clearly



If a SQL query fails for a specific column:

do not remove the column

populate:

Profiling failed

include the error category in Potential Data Quality Issue


continue profiling the remaining columns


Performance requirements

Avoid inefficient querying.

Where possible:

combine multiple aggregate metrics into one SQL query per table

avoid one full table scan per metric

do not use SELECT *

do not load millions of rows into pandas

use SQL-side aggregation

use small TOP queries only for representative values

quote identifiers safely

handle reserved words and special characters correctly


Print progress such as:

Profiling table 3/17: EDGESOURCE.ACCOUNTENGAGEMENTWEB

and show runtime per table.

Before profiling

First inspect the existing Phase 1 workbook and existing scripts.

Print:

Table Name | Phase 1 Column Count | DB Accessible | Profiling Status

Confirm all 17 tables are reachable.

Do not start Phase 2 workbook generation until the table accessibility check is complete.

Final validation

At completion, print a summary such as:

tables profiled

columns profiled

profiling failures

confirmed candidates

candidates requiring transformation

investigate further

exclusions

join-key-only columns

high leakage risk columns

Phase 2 workbook path


Do not consider Phase 2 complete unless all 17 tables and all Phase 1 columns are represented in the Phase 2 workbook.
