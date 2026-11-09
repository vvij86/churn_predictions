Hi Sai,

Please find below a quick summary of the Databricks ML Runtime cluster provisioning in DEV, based on ADO Task 2901214.

1. Initial investigation (3–7 Sep):
Raised ServiceNow incident INC11134129 with AWS Databricks Support to check ML Runtime cluster availability. Support confirmed that no existing ML Runtime cluster was available in the AU/EU workspaces and advised coordinating with the workspace administrators.

2. Admin coordination (8–15 Sep):
Raised additional requests INC111183527 and INC111163243 to identify the relevant workspace administrators and initiate cluster provisioning. Contacted the EU workspace admin (Pooja Sharma), who involved Mukesh and Hema for further review.

3. Access restrictions (20–23 Sep):
Databricks Support clarified the Dedicated access mode requirement. We initially proceeded with dedicated single-user ML compute, which was created on 23 Sep.

4. Group-access requirement:
Since multiple team members required access, a separate ADO Story (2968887) was created to track dedicated group-access ML Runtime provisioning.

5. Final status:
The ML Runtime cluster was subsequently provisioned in DEV with dedicated group access, and sanity checks were completed successfully.

Timeline: The initial investigation started on 3 Sep, and single-user compute was created by 23 Sep (20 calendar days). The exact end-to-end duration for group-access provisioning is subject to confirmation of its completion date.

Key challenges: No existing ML Runtime compute, identification of the correct workspace administrators, and clarification of access mode and group-access requirements.

ADO Reference: Task 2901214 and Story 2968887.
