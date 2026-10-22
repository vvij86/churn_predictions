Read MemberRetention_01-AccountBase_v006.sql and identify the exact logic used to derive IsTransitionedMemberExit.
I want to understand whether this exclusion can be implemented using only the approved 15 ML source tables, or whether it depends on any additional tables/columns outside that scope.
Please do the following:
Extract the complete IsTransitionedMemberExit logic exactly as used in the business SQL.
List every table, temp table, alias and source column required to calculate it.
Trace each required field back to its original physical source table.
Clearly separate:
fields available from the approved 15 ML source tables
fields coming from additional/out-of-scope sources
fields derived through temp tables or joins
Specifically identify the source of:
sub_fund
ExitDateMetric
memberSource
Check whether an equivalent field already exists in any of the approved 15 tables, especially:
edgeSource.accountSummary
edgeSource.customerMapping
edgeSource.customerSummary
tableau.fundListSource
Do not invent an alternative implementation. If the exact business rule cannot be reproduced using the approved 15 tables, clearly state which additional source/table is required.
Explain whether this rule should be applied:
while building the eligible account population,
while creating target_churn,
or both.
Explain how the transitioned-member exclusion should be applied to the standalone feature queries without using IsTransitionedMemberExit as a predictive feature.
Keep the response concise and provide a final table with:
Required Field | Original Source | In Approved 15 Tables? | Alternative Available? | Needed for Exact Rule?
Do not modify any SQL file. I only need analysis of the existing business SQL.
