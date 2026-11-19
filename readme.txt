Update the existing file:

"ml_mscs_mrt_base_population.py"

Do not change the existing business logic, source mappings, filtering logic, validation rules, modelling grain, or output DataFrame.

Add production-style logging and exception handling only.

Requirements:

1. Use Python's built-in "logging" module.

2. Create a module-level logger:

"logger = logging.getLogger(__name__)"

Configure logging so INFO-level messages are visible in Databricks job output.

3. Replace normal pipeline-status "print()" statements with appropriate logging calls:

- "logger.info()" for normal progress and validation metrics
- "logger.warning()" for non-fatal data-quality observations
- "logger.error()" only when appropriate
- "logger.exception()" inside exception handlers

4. Keep schema/sample display functionality where it is useful for development, but use logging for execution/status messages.

5. Add clear INFO logging for major stages such as:

- starting base population build
- loading "mscs_mrt_account_summary"
- source schema validation
- source field mapping
- applying historical/date filters
- applying eligibility/deceased filtering
- applying deterministic point-in-time selection
- building "base_population_df"
- starting validation
- validation metrics
- successful completion

6. Wrap major functions with appropriate exception handling.

For example:

- source loading failure
- missing mandatory source columns
- transformation/build failure
- validation failure

7. Use "logger.exception()" so the full stack trace appears in Databricks job logs.

Example pattern:

try:
    ...
except Exception:
    logger.exception("Failed to build base population")
    raise

8. Always re-raise critical exceptions.

Do not silently catch or suppress errors.

Databricks jobs must fail correctly when critical pipeline logic fails.

9. For required-column validation, raise a clear exception such as:

"ValueError" or "RuntimeError"

with the missing column names included in the message.

10. Keep existing critical validation failures.

The following conditions must still fail the job:

- duplicate "account_id + as_of_date" > 0
- null "account_id" > 0
- null "as_of_date" > 0

Log the validation failure before raising the exception.

11. Log the final validation metrics clearly, including:

- total row count
- distinct account_id count
- distinct account_id + as_of_date count
- duplicate count
- null account_id count
- null as_of_date count
- minimum as_of_date
- maximum as_of_date

12. Do not add MLflow autologging to this file.

This is a feature/base-population pipeline, not a model-training file.

MLflow autologging will be introduced later during model training/evaluation.

13. Do not change:

- source catalog
- source schema
- source table
- historical start date
- AsOfDate logic
- field mappings
- existing business rules
- final grain
- final DataFrame name

Final DataFrame must remain:

"base_population_df"

14. Keep the code simple and Databricks-friendly.

Do not create a custom external log file on local disk.

Logs should appear naturally in Databricks job/run output.

15. After refactoring, ensure the existing output/validation results remain functionally unchanged.
