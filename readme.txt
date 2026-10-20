Read member_retention_ml_copilot_instructions.md and continue from the existing behavioural_features_business_review.sql. Do not restart from scratch and do not regenerate unrelated logic.
Update all standalone feature queries so that the modelling/account population is restricted using the same FundScope / FundsInScope logic from MemberRetention_01-AccountBase_v006.sql.
Important:
Reuse the exact approved @FundScope / #FundsInScope logic from the business SQL.
Do not invent a new fund list.
Do not use a separate manual databaseCode NOT IN (...) exclusion list if the approved business SQL already defines the in-scope funds.
Apply the in-scope fund filter consistently to every standalone feature query where account population is involved.
Keep all existing approved rules unchanged:
fundJoinDate <= @AsOfDate
use exitDateRecorded, not exitDate
exclude accounts already exited by AsOfDate
apply death exclusion
apply internal-transfer rules where relevant
keep point-in-time safety
Each standalone query must remain independently runnable, so include the minimum required FundScope/FundsInScope setup inside that query block rather than relying on a temp table created by a previous query.
Also add this to each query comment block:
Fund Scope: Uses approved FundsInScope logic from MemberRetention_01-AccountBase_v006.sql
Finally, validate that no unrelated databaseCode/fund records are included and summarize any queries where the business FundScope could not be applied directly.
