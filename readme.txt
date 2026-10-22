Overview

This document lists the behavioural features identified for the Member Retention ML model for business review and confirmation.

Feature engineering converts member and account data into meaningful behavioural indicators that can be used by the ML model to identify accounts at risk of churn. These features capture patterns such as member engagement, contribution behaviour, money flow, rollover activity, investment activity and other account-level behaviours.

The features will be calculated for each monthly pipeline run using information available up to the relevant snapshot/AsOfDate. The ML model will use these engineered features as inputs to generate account-level churn probability, risk classification and key churn drivers.

Feature versions will be maintained based on changes to the feature calculation logic so that the features used by each model version remain traceable and reproducible. The engineered features and their versions will be stored and managed as part of the Databricks MLOps process for model training, validation and scoring.
