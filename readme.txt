SELECT
    CONVERT(VARCHAR(7), exitDateRecorded, 120) AS exit_month,
    exitType,
    COUNT(DISTINCT accountID) AS account_count
FROM Edge.AccountSummary
WHERE databaseCode = 'ST000'
    AND exitDateRecorded >= '2026-01-01'
    AND exitDateRecorded < '2026-10-01'
GROUP BY
    CONVERT(VARCHAR(7), exitDateRecorded, 120),
    exitType
ORDER BY exit_month, exitType;
