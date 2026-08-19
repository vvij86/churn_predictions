import importlib
import sys

libraries = {
    "pandas": "pandas",
    "numpy": "numpy",
    "sklearn": "scikit-learn",
    "mlflow": "mlflow",
    "xgboost": "xgboost",
    "hyperopt": "hyperopt",
    "pyspark": "pyspark",
    "joblib": "joblib",
    "psutil": "psutil"
}

print("Python:", sys.version)
print("-" * 70)

for module_name, display_name in libraries.items():
    try:
        module = importlib.import_module(module_name)
        version = getattr(module, "__version__", "installed - version unavailable")
        print(f"PASS  {display_name:<20} {version}")
    except Exception as e:
        print(f"FAIL  {display_name:<20} {type(e).__name__}: {e}")
