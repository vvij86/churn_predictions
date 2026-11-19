We request the creation of a new Databricks ML Runtime cluster with dedicated group access in the Mercer Wealth Europe DEV (EU/UK) workspace to support ongoing ML development activities for the Member Retention Analytics project.

Previously, the cluster "mer_dev_wealth_SaiBeera_MRA_single_user_cluster" was configured with dedicated group access and renamed to "mer_wealth_dev_mra_ml_shared_cluster". The group "mer_wealth_mscs_ds_dev" was granted Can Restart permission.

However, the existing cluster has now expired due to inactivity and is no longer available. Hence, we request a new ML Runtime cluster with a similar configuration and dedicated group access.

Requested Configuration:

- Cluster Type: Databricks ML Runtime
- Access Mode: Dedicated
- Dedicated Group: "mer_wealth_mscs_ds_dev"
- Required Permission: Can Restart
- Proposed Cluster Name: "mer_wealth_dev_mra_ml_shared_cluster" (subject to name availability)
- Workspace: Mercer Wealth Europe DEV (EU/UK)

Project Details:

- Project Name: Member Retention Analytics
- App Short Key: MSECDP
- Planview Code: 1013599
- Workspace ID: 3997133087712069
- Environment: DEV

Business Impact:

The ML Runtime cluster is required for feature engineering, model training, evaluation, and other ML development activities. The unavailability of the cluster is impacting ongoing development.

Request:

Kindly provision a new ML Runtime cluster with dedicated access for the "mer_wealth_mscs_ds_dev" group and grant the necessary restart permissions on priority.
