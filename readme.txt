Ticket Title: Databricks ML Job Compute and Service Principal Setup – UK Workspace (Stage & Production)

**Project Details:**
- Project Name: Member Retention Analytics
- App Short Key: MSECDP
- Plan Item Code: 101588
- Environment: DEV, Stage & Production
- Workspace: UK Databricks

**Description:**

For the Member Retention Analytics ML project, we require the following Databricks infrastructure setup in the UK Workspace.

**Requirements:**

1. Configure Databricks Job Compute for Stage and Production environments with the appropriate ML Runtime.
2. Create environment-specific Service Principals for Stage and Production to be used as the Databricks Jobs Run As identity.
3. Grant the necessary Unity Catalog permissions to the respective Service Principals.
4. Enable automated ML model training, validation, and scoring through Databricks Jobs without dependency on interactive user clusters.
5. Ensure Stage supports automated validation, integration and pre-production testing.
6. Ensure Production supports automated model training and/or scoring with restricted interactive access.

**Reference:** The dedicated ML Runtime cluster is already available in the DEV environment.

Please review and implement the required configurations for Stage and Production.

I've included the project details from the Teams screenshot. Please verify the plan item code before submitting, as the image is slightly blurred.
