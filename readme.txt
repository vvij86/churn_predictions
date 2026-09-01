You can create an ADO Task like this:

Title:
Investigate Databricks ML Cluster Runtime and Library Compatibility

Description:
Investigate the feasibility of using a Databricks ML cluster/runtime instead of the current job cluster for the ML workload.

The investigation should:

Identify the Databricks Runtime ML version currently/appropriately used in the AU environment.

Identify the key ML libraries/packages pre-installed with that runtime.

Validate whether the required libraries support the ML algorithms evaluated in the POC.

Identify any additional libraries that would need to be installed separately.

Compare the suitability of an ML cluster vs the current job cluster for the ML development/training workload.

Document findings and recommendation.


Definition of Done / Acceptance Criteria:

1. Databricks ML Runtime version for the AU environment is identified.


2. Pre-installed ML libraries and relevant versions are documented.


3. Library compatibility is validated against the POC algorithms, such as Logistic Regression, Random Forest, Decision Tree, HistGradientBoosting and XGBoost.


4. Any missing/additional library requirements are identified.


5. Benefits/limitations of using the ML cluster instead of the job cluster are documented.


6. A recommendation is provided on whether the ML cluster/runtime can be used for the upcoming ML development.



For estimation, since this is mainly an investigation/spike-type task, I would initially suggest 6 hours / 1 day.
