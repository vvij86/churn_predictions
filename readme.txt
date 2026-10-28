Title: Validate Prerequisites for Stage and Production ML Environments

Description:

Verify the prerequisites required for deploying Databricks ML notebooks and jobs in Stage and Production environments, including ML runtime availability, required permissions, service principal configuration, and GitHub CI/CD setup.

Acceptance Criteria:

1. Validate ML runtime and compute prerequisites for Stage and Production.
2. Verify service principal access and required permissions.
3. Confirm GitHub CI/CD deployment prerequisites.
4. Identify and document any gaps or dependencies before deployment.
5. Confirm readiness to proceed with ML job deployment in Stage and Production.




Comment:

As per AWS team confirmation (INC11450677), the required infrastructure prerequisites are available except for job cluster creation, which will be handled through GitHub CI/CD deployment. A separate task has been created for prerequisite validation before deployment. Closing this task as the environment setup prerequisites have been addressed.








