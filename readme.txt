SELECT
    CONVERT(VARCHAR(7), exitDateRecorded, 120) AS exit_month,
    fundID,
    COUNT(DISTINCT accountID) AS exit_accounts
FROM Edge.AccountSummary
WHERE databaseCode = 'ST000'
    AND exitType = 'Exit'
    AND exitDateRecorded >= '2026-01-01'
    AND exitDateRecorded < '2026-10-01'
GROUP BY
    CONVERT(VARCHAR(7), exitDateRecorded, 120),
    fundID
ORDER BY exit_month, exit_accounts DESC;
