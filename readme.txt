SELECT
    fundID,
    dbCode,
    mtNumber,
    subFund,
    fundName
FROM Edge.FundList
WHERE COALESCE(NULLIF(mtNumber, ''), subFund)
    IN ('MT888', 'MT999');


SELECT
    CAST(a.exitDateRecorded AS DATE) AS exit_date,
    a.fundID,
    f.fundName,
    COUNT(DISTINCT a.accountID) AS exit_accounts
FROM Edge.AccountSummary a
INNER JOIN Edge.FundList f
    ON a.fundID = f.fundID
WHERE a.databaseCode = 'ST000'
    AND a.exitType = 'Exit'
    AND a.exitDateRecorded >= '2026-03-01'
    AND a.exitDateRecorded < '2026-05-01'
GROUP BY
    CAST(a.exitDateRecorded AS DATE),
    a.fundID,
    f.fundName
ORDER BY exit_accounts DESC;
