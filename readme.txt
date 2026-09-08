I am performing ML-focused exploratory data analysis for a customer churn / retention analytics project.

I need you to build a Python-based profiling and documentation solution for 17 SQL Server tables.

The goal is NOT to train a model yet. The goal is to identify and document potential churn-driver columns that may later be used for feature engineering and ML modelling.

Input files

The current VS Code workspace contains:

1. All_table_scripts.sql

Contains CREATE TABLE / DDL scripts for all required tables.

Use this file to identify:

table names

column names

column ordinal/order

data types

possible primary/foreign/business keys where identifiable




2. All_tables_null_or_blank_count.xlsx

Contains data-quality profiling for the tables/columns.

It includes information such as:

table name

column name

row count

null count

blank count where applicable

null percentage / blank percentage





Do not invent column metadata if it can be obtained from these files.

Tables in scope

Create one worksheet for each of these tables:

MERCEREDGE.EDGEPORTALSOURCE.CUSTOMERDETAILS

MERCEREDGE.EDGEPORTALSOURCE.ACCOUNTINSURANCE

MERCEREDGE.EDGEPORTALSOURCE.ACCOUNTMONEYINFLOW

MERCEREDGE.EDGEPORTALSOURCE.ACCOUNTROLLOVERPAYMENT

MERCEREDGE.EDGESOURCE.ACCOUNT

MERCEREDGE.EDGESOURCE.ACCOUNTENGAGEMENTHELPLINE

MERCEREDGE.EDGESOURCE.ACCOUNTENGAGEMENTWEB

MERCEREDGE.EDGESOURCE.ACCOUNTINVESTMENTS

MERCEREDGE.EDGESOURCE.ACCOUNTMONEYINFLOW

MERCEREDGE.EDGESOURCE.ACCOUNTNETMONEYFLOW

MERCEREDGE.EDGESOURCE.ACCOUNTROLLOVERPAYMENT

MERCEREDGE.EDGESOURCE.ACCOUNTSUMMARY

MERCEREDGE.EDGESOURCE.CRN

MERCEREDGE.EDGESOURCE.CUSTOMERMAPPING

MERCEREDGE.EDGESOURCE.CUSTOMERSUMMARY

MERCEREDGE.EDGESOURCE.THIRDPARTYAUTHORITY

MERCEREDGE.TABLEAU.FUNDLISTSOURCE


Optional SQL Server profiling

The Python solution may connect to SQL Server using Windows Authentication.

Do NOT hard-code passwords or credentials.

Use pyodbc and Windows Trusted Authentication.

Read configuration from environment variables such as:

SQL_SERVER

SQL_DATABASE


Example connection approach:

DRIVER={ODBC Driver 18 for SQL Server};SERVER=<server>;DATABASE=<database>;Trusted_Connection=yes;TrustServerCertificate=yes;

The script must still be able to generate the workbook using the SQL DDL and existing Excel profiling file even if the database connection is disabled.

Add a configuration variable:

ENABLE_DB_PROFILING = False

so that database profiling can be switched on later.

Database profiling

If ENABLE_DB_PROFILING=True, profile each column safely and efficiently.

Do NOT pull complete tables into pandas.

Use aggregate SQL queries wherever possible.

Capture, where practical:

total row count

null count

null percentage

blank percentage for text columns

approximate/distinct count

minimum and maximum for numeric/date columns

minimum and maximum date

3-5 representative sample values

potential constant columns

very high-cardinality columns

possible identifiers


Avoid expensive full-table scans where possible.

ML/churn assessment

For every column, assess its potential usefulness for customer churn prediction.

Create these columns in each worksheet:

1. Ordinal


2. Column Name


3. Data Type


4. Key Role


5. Feature Group


6. Useful for Churn


7. Decision


8. Reason


9. Data Quality Notes


10. Null %


11. Distinct Count


12. Sample Values


13. Leakage Risk


14. Recommended Action



Key Role values

Categorise where possible as:

Identifier

Primary Key

Foreign Key

Customer Key

Account Key

Status

Date

Numeric Measure

Category

Flag

Free Text

Contact Information

Unknown


Feature Group values

Assign meaningful churn-related groups such as:

Identification

Account / Product

Status / Lifecycle

Tenure

Demographics

Contributions / Money Inflow

Withdrawals / Money Outflow

Net Cashflow

Rollovers

Balance / FUM

Investments

Engagement - Web

Engagement - Helpline

Insurance

Communication

Customer Preferences

Third Party / Adviser

Geographic

Operational / Audit

Target / Outcome Related

Other


Useful for Churn

Allowed values:

Yes

Maybe

No


Decision

Allowed values:

Include

Consider

Skip

Investigate


Assessment rules

Use ML and business reasoning rather than simply marking every populated column as useful.

Examples:

IDs such as CUSTOMER_ID, ACCOUNT_ID, CRN:

normally Useful for Churn = No

Decision = Skip

but retain them for joining and traceability.


Names, email addresses, phone numbers and addresses:

do not use raw personally identifying values as model features.

however, derived indicators such as has_email, has_mobile may potentially be useful.


Status:

potentially useful but investigate carefully for target leakage.


Create/open/start dates:

useful for deriving tenure.


Birth date:

do not directly recommend raw date.

recommend deriving age/age band if appropriate.


Contribution/money-inflow fields:

generally potential churn drivers.

consider features such as frequency, amount, recency, change/trend, months since last contribution.


Withdrawal/rollover/net-money-flow fields:

potentially strong churn indicators.

assess carefully for target leakage depending on whether events occur before or after the prediction as-of date.


Web/helpline engagement:

potentially useful behavioural signals.

consider counts, recency and frequency.


Investments:

potentially useful for investment diversity, switching behaviour, balances or allocation changes.


Insurance:

potentially useful as product attachment / customer stickiness indicators.


Audit columns such as CREATED_BY, UPDATED_BY, LOAD_DATE, ETL timestamps:

normally Skip unless there is a clear business interpretation.


Columns with 100% nulls:

Skip.


Columns with extremely high nulls:

normally Consider or Skip depending on business importance.


Constant or near-constant columns:

normally Skip.


High-cardinality text columns:

normally Skip raw values.



Target leakage

This is very important.

Add a Leakage Risk value:

None

Low

Medium

High


Flag columns that appear to represent:

account closure

exit

rollover-out completion

termination

final withdrawal

post-exit status

cancellation

events occurring after churn


as potential leakage.

Explain in the Reason column that these variables may only be usable if their values are known BEFORE the ML prediction as_of_date.

Do not automatically recommend them simply because they are highly correlated with churn.

Data-quality notes

Combine the existing null/blank profiling with additional observations.

Examples:

Complete, no nulls

37% null

Mostly null

100% null - unusable

High cardinality

Constant value

Date coverage requires validation

Categorical values need mapping

Free-text field


Recommended Action

Give a concise next action such as:

Use directly

Derive tenure

Derive age

Derive presence flag

Aggregate over 3/6/12 months

Calculate recency

Calculate frequency

Calculate trend

Calculate count

Calculate amount

Validate against as_of_date

Investigate business definition

Join key only

Exclude from ML


Workbook requirements

Generate:

MercerEdge_ML_Churn_Driver_EDA.xlsx

Create:

one Overview worksheet

one worksheet per source table


The Overview sheet should contain:

Table Name

Total Columns

Include

Consider

Investigate

Skip

Yes

Maybe

No

High Leakage Risk Columns

Important Feature Groups

General Comments


Format the workbook professionally using openpyxl.

Use:

frozen header row

filters

wrapped text

sensible column widths

conditional fill colours for Yes / Maybe / No

conditional fill colours for Include / Consider / Skip / Investigate

highlight High leakage risk


Important constraint

This is an ML feature discovery / EDA workbook, not a final feature-selection decision.

Therefore:

Do not claim a column is definitely predictive without statistical/model evidence.

Use phrases such as potential churn driver, candidate feature, requires validation.

Do not invent business definitions.

If the meaning of a column is unclear, set:

Useful for Churn = Maybe

Decision = Investigate

Reason = Business definition required



Code structure

Please create clean reusable Python scripts, preferably:

config.py

parse_ddl.py

load_data_quality.py

profile_sql_tables.py

assess_churn_features.py

generate_eda_workbook.py

run_eda.py


Before writing code, first inspect All_table_scripts.sql and All_tables_null_or_blank_count.xlsx and explain the structure you detected.

Then implement the solution.

Finally run the code locally and validate that:

all 17 tables are represented

every DDL column appears in its table worksheet

null percentages match the source profiling workbook

no duplicate columns are generated

the Overview counts reconcile with individual worksheets.
