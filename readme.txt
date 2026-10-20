Review the current behavioural_features_business_review.sql.
The previous update claimed that FundScope was applied using accountSummary.databaseCode, but I cannot find the actual hard-coded FundScope filter anywhere in the generated SQL.
Fix this now.
For every standalone query that uses edgeSource.accountSummary directly, explicitly add this predicate inside the actual WHERE clause:
AND a.databaseCode IN
(
    'MASTA',
    'MASTP',
    'MASTR',
    'MASTS',
    'MASTM',
    'MTAPD',
    'ST000',
    'MASTR_AP'
)
Use the correct table alias if it is not a.
For every standalone feature query whose source table does not contain databaseCode, add an eligible_accounts CTE inside that same standalone query using edgeSource.accountSummary, and include the exact same databaseCode IN (...) filter there.
Do not rely on comments, metadata, summary text or validation variables. The FundScope condition must appear in the executable SQL itself.
After updating, search the entire file and verify:
MASTA appears in the actual SQL
MASTP appears in the actual SQL
MASTR_AP appears in the actual SQL
every standalone query is scoped through accountSummary.databaseCode
there are zero references to MercerDM.span.fundList
there are zero references to #FundsInScope
Also add a final validation section that returns:
actual_fundscope_filter_present = YES
mercerdm_span_fundlist_reference_count = 0
fundsinscope_reference_count = 0
Do not just update comments. Update the executable SQL.
Do not change unrelated feature logic.
Stop after correcting behavioural_features_business_review.sql.
