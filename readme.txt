Yes — Sai’s message is basically giving you the recommended temporary approach.

He is saying:

Long term: create a project-specific Okta/Databricks group and use Dedicated access assigned to that group.

For now in DEV: use Dedicated access with a single user, until the group is created/enabled.

Once the group is ready, the access should be moved/provided to the group rather than keeping separate single-user access.


His key line is:

> “yes only dev... but we need to be given to group”



So when you reply to Mukesh, you can say something like:

> Hi Mukesh,

Thanks for the clarification.

As per the Databricks documentation, Dedicated access mode supports assignment to either a single user or a group. We are planning to raise a request for a project-specific Okta/Databricks group.

Until the group is created and Dedicated group access is enabled, could we please proceed with Dedicated single-user access for DEV? Once the group is available, we would like the ML compute access to be provided to that group.

Please let us know if this approach is feasible.

Thanks,
Vijay



That matches Sai’s direction well.
