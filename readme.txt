Use this Copilot prompt:

> Read member_retention_ml_copilot_instructions.md first and continue from the existing behavioural_features_business_review.sql.

Do not restart from scratch.

I want you to remove all usage of MercerDM.span.fundList from the standalone feature queries.

Important context:

- MercerDM.span.fundList is not part of the approved 15 ML source tables.
- tableau.fundListSource is part of the approved source scope, but it only provides dbCode.
- Therefore, do not try to recreate the old dbCode -> fundID mapping through MercerDM.span.fundList.
- Instead, restrict the population using the approved @FundScope database codes directly wherever accountSummary.databaseCode or another source-specific database code is available.

Use the same approved FundScope values from the business SQL:

'MASTA,MASTP,MASTR,MASTS,MASTM,MTAPD,ST000,MASTR_AP'

For each standalone query:

1. Remove:

FROM MercerDM.span.fundList

and any related:

#FundsInScope
fundID mapping
dbCode -> fundID lookup
CREATE INDEX on #FundsInScope
JOIN #FundsInScope

2. Do not introduce any replacement lookup table outside the approved source scope.

3. Where the query starts from edgeSource.accountSummary, apply FundScope directly using:

a.databaseCode IN
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

4. Where another source table does not contain databaseCode, scope it by first joining to eligible accounts from edgeSource.accountSummary using accountID, and apply the FundScope filter there.

Example pattern:

WITH eligible_accounts AS
(
    SELECT DISTINCT
        a.accountID
    FROM edgeSource.accountSummary a
    WHERE a.databaseCode IN
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
      AND a.fundJoinDate <= @AsOfDate
      AND (
          a.exitDateRecorded IS NULL
          OR a.exitDateRecorded > @AsOfDate
      )
      AND (
          a.dateOfDeath IS NULL
          OR a.dateOfDeath > @AsOfDate
      )
      AND COALESCE(a.deathIndicatorFlag, 0) = 0
)

Then join the feature source to:

INNER JOIN eligible_accounts ea
    ON ea.accountID = source.accountID

5. Each standalone query must remain independently runnable, so include its own:

- @AsOfDate
- @FeatureStartDate
- any recent/prior date parameters
- eligible-account/FundScope logic required by that query

Do not depend on a temp table or CTE created by a previous query.

6. Keep all existing approved rules unchanged:

- modelling grain is account + AsOfDate
- fundJoinDate <= @AsOfDate
- use exitDateRecorded, not exitDate
- exclude accounts already exited as of the snapshot
- retain death exclusion
- internal transfers are not churn
- no post-AsOfDate feature data
- no target leakage
- 36 months = overall training history
- 12 months = default feature window

7. Do not use tableau.fundListSource unless it is genuinely required for a feature already supported by that table. Do not use it merely to recreate the old MercerDM.span.fundList mapping.

8. In every feature comment block, replace any wording such as:

Fund Scope: Uses #FundsInScope / MercerDM.span.fundList

with:

Fund Scope: Restricted directly using approved accountSummary.databaseCode values from the business reference SQL

9. Search the entire file and confirm there are zero remaining references to:

MercerDM.span.fundList
#FundsInScope

Output a final validation result:

mercerdm_span_fundlist_reference_count = 0
fundsinscope_temp_reference_count = 0
fundscope_filter_method = accountSummary.databaseCode
fundscope_validation = PASS

10. Do not change unrelated feature logic, business mappings or existing feature names unless necessary to remove the MercerDM.span.fundList dependency.

11. Do not build the final consolidated modelling dataset.

12. Do not start model training.

Update only:

behavioural_features_business_review.sql

Stop after removing all MercerDM.span.fundList / #FundsInScope usage and validating that every standalone query still applies the approved FundScope correctly through accountSummary.databaseCode.
