Once the Bronze views are ready in Databricks, your ML flow can move from direct UAT-table prototyping into a proper repeatable pipeline.

At a high level, I would structure it like this:

1. Validate Bronze views

confirm all required source tables/columns are present

check row counts, date coverage, keys, nulls, and business-rule fields

confirm Bronze matches what you already explored in UAT



2. Build Silver / cleaned modelling inputs

standardize column names and data types

apply data-quality rules

resolve account/member/customer mappings

normalize dates and sentinel values

create reusable cleaned source views



3. Rebuild the base historical dataset on Databricks

one row per account_id + as_of_date

apply eligibility

death/internal-transfer exclusions

create future churn target

parameterize FeatureStartDate, AsOfDate, and outcome dates



4. Feature engineering

account/tenure/product features

contribution and money-flow features

rollover/withdrawal features

web/helpline/workflow engagement

campaign/event features

Qualtrics CSAT/VoC features when available

missing-value treatment and feature validation



5. Generate historical training snapshots

run the same logic for quarterly AsOfDates

append the snapshots into one historical modelling dataset

keep point-in-time safety for every feature



6. Train / validation / test split

use time-based splitting

keep final holdout period untouched

avoid random split as the primary approach



7. Model development

baseline Logistic Regression

Decision Tree / Random Forest

HistGradientBoosting / XGBoost if supported

compare AUC, recall, precision, F1, etc.



8. Tune and select the model

hyperparameter tuning

class-imbalance handling if required

threshold tuning

select champion model



9. Explainability and business validation

global feature importance

account-level churn drivers

validate whether drivers make business sense

check for leakage



10. MLflow / MLOps



log runs, parameters, features, metrics

register model

version champion/challenger

promote through DEV → Stage → Prod


11. Scoring pipeline



build latest scoring dataset using the same feature definitions

score active accounts

produce churn probability, risk band, drivers, model version


12. Power BI / downstream output



publish the agreed scoring output

account/member IDs

churn probability

risk band

primary/additional drivers

retention category

FUM/business fields

recommended action if required


13. Monitoring and retraining



monitor model performance and data drift

track scoring volumes and feature distributions

define retraining cadence

revalidate when strategic data replaces tactical sources


So your immediate sequence after Bronze is ready should basically be:

> Bronze validation → Silver/cleaned inputs → base historical dataset → feature engineering → historical snapshots → model training/validation → MLOps → scoring/output.



And because you already did a lot of tactical exploration directly on UAT, much of that work should help you validate the Bronze mapping faster rather than starting from zero.
