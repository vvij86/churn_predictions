## Logging and Exception Handling

- Use Python `logging` for pipeline execution/status messages.
- Use `logger.info()` for normal progress.
- Use `logger.warning()` for non-fatal data-quality concerns.
- Use `logger.exception()` inside exception handlers to preserve full stack traces.
- Re-raise critical exceptions so Databricks jobs fail correctly.
- Never silently swallow exceptions.
- Missing required columns, invalid modelling grain, null keys, or leakage validation failures must raise explicit exceptions.
- Do not use MLflow autologging for feature-engineering/base-population files.
- MLflow autologging should be used later for model training/evaluation where appropriate.
