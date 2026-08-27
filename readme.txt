Copilot Prompt — Step 9: Schedule Batch Scoring with Databricks Jobs

Create a new Databricks notebook named:

"09_schedule_batch_scoring_poc.ipynb"

This notebook should document and validate the scheduling approach for the existing batch-scoring process.

Current State

The following POC steps are already completed:

- Model registered in Unity Catalog
- Version 1 = Champion
- Version 2 = Candidate
- Batch scoring using "@Champion"
- Scoring output saved to:

"superdata_au_dev.mlops.churn_scoring_output_poc"

Existing batch scoring notebook:

"07_batch_scoring_using_champion_alias"

Purpose

Demonstrate how batch scoring can be automated using Databricks Jobs / Workflows instead of being manually executed.

The actual schedule should be configured through the Databricks Jobs UI.

Do not create a production scheduling framework.

Step 9 - Schedule Batch Scoring

Create a Markdown heading:

"# Step 9 - Schedule Batch Scoring Using Databricks Jobs"

Explain in simple terms:

- Batch scoring currently runs manually.
- Databricks Jobs can automatically execute the scoring notebook on a defined schedule.
- The scheduled job will load the current "Champion" model alias each time it runs.
- This means the scoring job does not need to be modified when the Champion model version changes.

1. Explain Scheduled Scoring Flow

Add a simple Markdown flow:

"Latest Scoring Dataset → Champion Model → Batch Scoring → Unity Catalog Output Table"

Then:

"Databricks Job Schedule → Automatically repeats the above process"

Explain that the scoring frequency depends on business requirements.

For this POC, use a monthly schedule as an example.

Add this note:

POC Note: Monthly scoring is used only as an example. The actual production frequency should be agreed with the business and downstream consumers.

2. Identify Notebook to Schedule

Use the existing notebook:

"07_batch_scoring_using_champion_alias"

Explain that this notebook:

- loads the Champion model
- performs predictions
- creates account-level scoring output

Also mention that if the full production flow must include writing results to Unity Catalog, the scoring and output-write logic can later be combined into one production scoring notebook.

Do not modify Step 7 automatically.

3. Databricks Jobs UI Instructions

Create a Markdown section named:

"## Create the Databricks Job"

Provide these manual UI steps:

1. Open Jobs & Pipelines in Databricks.

2. Select Jobs.

3. Click Create Job.

4. Give the job a meaningful name:
   
   "superannuation_churn_batch_scoring_poc"

5. Create a task named:
   
   "churn_batch_scoring"

6. Select task type:
   
   "Notebook"

7. Select the existing notebook:
   
   "07_batch_scoring_using_champion_alias"

8. Select an available compute option.
   
   Prefer Serverless if it is permitted and compatible with the notebook.

9. Save the task.

4. Configure Schedule

Add a Markdown section explaining how to configure the trigger/schedule.

For this POC, suggest:

"Monthly"

Explain that an example could be the first day of every month.

Do not force an exact production date/time.

Explain that Databricks allows:

- Daily
- Weekly
- Monthly
- Cron-based schedules

Mention that the production schedule should align with when the latest scoring features become available.

5. Test Using Run Now

Explain that before relying on the schedule, the user should click:

"Run now"

This validates that the notebook can execute successfully as a Databricks Job.

After execution, verify:

- Job status = Succeeded
- Notebook task completed
- Start time
- End time
- Duration
- Logs/output are available

6. Verify Batch Output

After the Job completes, verify that scoring output was generated.

If using the existing Step 7 notebook, verify the generated scoring output file.

Also explain that in the production flow the preferred output should be a Unity Catalog table such as:

"superdata_au_dev.mlops.churn_scoring_output_poc"

Do not automatically overwrite or change the current table in this notebook.

7. Explain Champion Alias Benefit

Add a Markdown section explaining this important MLOps concept:

The scheduled job should load:

"models:/superdata_au_dev.mlops.superannuation_churn_model@Champion"

and should NOT hardcode:

"Version 1"

Example:

Today:

"Champion → Version 1"

Later:

"Champion → Version 2"

The scheduled scoring notebook still uses:

"@Champion"

so no notebook or Job configuration change is required.

8. Add Optional Job Parameters Concept

Add a Markdown-only section explaining that in future the scoring notebook can accept parameters such as:

- scoring_date
- input_table
- output_table
- model_alias
- environment

Do not implement complex parameterization in this POC.

Explain that parameters make the same scoring notebook reusable across DEV/TEST/PROD.

9. Failure and Retry Concept

Add a short Markdown section explaining that Databricks Jobs supports:

- retries
- timeout settings
- notifications
- failure alerts

For this POC, do not configure complex alerting.

State that these settings should be finalized during production implementation.

10. What to Capture for POC Evidence

Add a Markdown checklist of evidence to capture after creating the Job:

- Job name
- Task name
- Scheduled notebook
- Selected compute
- Trigger/schedule
- Successful Run Now execution
- Run status
- Run duration
- Output generated successfully

11. Final Summary

Add a final Markdown summary:

"Step 9 demonstrates that the churn batch-scoring process can be automated using Databricks Jobs. The scoring notebook uses the Champion model alias, allowing future model promotion without changing the scheduled job."

Add this note:

POC Note: Scheduling frequency, compute configuration, retry policy, notifications, and production dependencies are not final and should be agreed during actual implementation.

Do not create:

- monitoring logic
- retraining logic
- rollback logic
- additional model versions

Keep this notebook focused only on the scheduling concept and manual Databricks Job configuration.
