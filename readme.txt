Create the following child task under the ADO story “Enable Group Based Dedicated ML Runtime cluster/environment”.

### Task Title

Request and Provision Dedicated Databricks ML Runtime Cluster with Group Access – EU/UK DEV

### Description

Raise and coordinate a ServiceNow request with the Databricks platform team to provision a new dedicated ML Runtime cluster for the Member Retention Analytics project in the EU/UK DEV workspace.

The previously configured cluster `mer_wealth_dev_mra_ml_shared_cluster` (renamed from `mer_dev_wealth_SaiBeera_MRA_single_user_cluster`) has expired due to inactivity and is no longer available.

**Activities:**
1. Raise a new ServiceNow request for ML Runtime cluster provisioning.
2. Attach the previous cluster provisioning email chain for reference.
3. Request Dedicated access mode for the existing ML group `mer_wealth_mscs_ds_dev`.
4. Request Can Restart permission for the group.
5. Coordinate with the platform team until the cluster is provisioned.
6. Validate cluster visibility, startup, ML Runtime availability, and group access.
7. Update the ServiceNow and ADO tickets with the outcome.

**Project Details:**
- Project: Member Retention Analytics
- App Short Key: MSECDP
- Planview Code: 1013599
- Workspace: Mercer Wealth Europe DEV (EU/UK)
- Workspace ID: 3997133087712069

### Acceptance Criteria

- New Databricks ML Runtime cluster is provisioned in the EU/UK DEV workspace.
- Dedicated group access is configured for `mer_wealth_mscs_ds_dev`.
- Required Can Restart permissions are granted.
- Authorized ML group members can access and start the cluster.
- Basic ML Runtime and notebook execution are successfully validated.
- ServiceNow request and ADO task are updated with the provisioning details and validation results.

ADO Link Type: Select Child (as shown in your screenshot).

Suggested State: In Progress

Comment (optional): ServiceNow request initiated for provisioning a new dedicated ML Runtime cluster with group access. Previous cluster configuration and email chain will be provided for reference.
