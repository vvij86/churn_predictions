Hi Team,

We require read access to the Unity Catalog tables/views in the Mercer Wealth Europe DEV Databricks workspace for the Member Retention Analytics project.

Currently, the required tables/views are visible in Catalog Explorer, but data access is restricted. This is impacting ongoing ML development activities, including historical dataset preparation, feature engineering, and model development.

Access Requested:

- Catalog: "mer_wealth_dev"
- Schema: "mer_wealth_landing_edge"
- Permission: Read-only access to all required tables/views within the schema ("USE CATALOG", "USE SCHEMA", and "SELECT")
- Access Type: Group-based access

Databricks Group:
"mer_wealth_mscs_ds_dev"

Please grant the required permissions to this group so that all authorized ML development team members can access the relevant tables/views.

Project Details:

- Project Name: Member Retention Analytics
- App Short Key: MSECDP
- Planview Code: 1013599
- Workspace: Mercer Wealth Europe DEV (EU/UK)
- Workspace ID: 3997133087712069
- Environment: DEV

Business Impact:

The missing read permissions are blocking access to the required source data and impacting ongoing ML development and validation activities.

Request:

Kindly prioritize this request and grant the required group-level read permissions to the specified catalog and schema, including the underlying tables/views.

Thanks.
