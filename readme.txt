# ============================================================
# Databricks Library Availability Check
# For ML / Data Science / MLOps Development
# ============================================================

import importlib
import sys
import pandas as pd

# ------------------------------------------------------------
# List of required libraries
# key   = import name used in Python
# value = package / purpose description
# ------------------------------------------------------------

libraries_to_check = {
    # Core Python / Data Analysis
    "pandas": "Data analysis and tabular data handling",
    "numpy": "Numerical computing",
    
    # Visualization
    "matplotlib": "Basic plotting and charts",
    "seaborn": "Advanced statistical visualization",
    
    # Machine Learning
    "sklearn": "Scikit-learn ML algorithms, preprocessing and metrics",
    "xgboost": "Gradient boosting ML model",
    "lightgbm": "LightGBM gradient boosting model",
    
    # MLOps / Experiment Tracking
    "mlflow": "MLflow tracking, model registry and model logging",
    
    # Hyperparameter Tuning
    "hyperopt": "Hyperparameter tuning",
    "optuna": "Hyperparameter optimization alternative",
    
    # Model Explainability
    "shap": "SHAP model explainability",
    "lime": "LIME local model explainability",
    
    # Statistics / Scientific Computing
    "scipy": "Scientific computing",
    "statsmodels": "Statistical modelling",
    
    # Data Quality / Validation
    "great_expectations": "Data quality validation",
    
    # Imbalanced Data Handling
    "imblearn": "Imbalanced-learn for SMOTE and class imbalance handling",
    
    # Databricks / Spark
    "pyspark": "Apache Spark Python API",
    "databricks": "Databricks SDK / utilities if installed",
    
    # Utility
    "joblib": "Model serialization and parallel processing",
    "cloudpickle": "Python object serialization",
}

# ------------------------------------------------------------
# Function to check library availability
# ------------------------------------------------------------

def check_library(import_name, purpose):
    try:
        module = importlib.import_module(import_name)
        
        version = getattr(module, "__version__", "Version not available")
        
        return {
            "Library Import Name": import_name,
            "Purpose": purpose,
            "Available": "Yes",
            "Version": version,
            "Status": "Ready to use"
        }
    
    except ImportError:
        return {
            "Library Import Name": import_name,
            "Purpose": purpose,
            "Available": "No",
            "Version": "-",
            "Status": "Needs installation"
        }

# ------------------------------------------------------------
# Run check
# ------------------------------------------------------------

results = []

for import_name, purpose in libraries_to_check.items():
    results.append(check_library(import_name, purpose))

library_status_df = pd.DataFrame(results)

# ------------------------------------------------------------
# Display result as table in Databricks
# ------------------------------------------------------------

display(library_status_df)

# ------------------------------------------------------------
# Optional summary
# ------------------------------------------------------------

available_count = (library_status_df["Available"] == "Yes").sum()
missing_count = (library_status_df["Available"] == "No").sum()

print("Library Check Summary")
print("---------------------")
print(f"Total libraries checked : {len(library_status_df)}")
print(f"Available libraries     : {available_count}")
print(f"Missing libraries       : {missing_count}")
