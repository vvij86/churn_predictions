SELECT
    DATE_FORMAT(exitDateRecorded, 'yyyy-MM') AS exit_month,
    exitType,
    COUNT(DISTINCT accountID) AS account_count
FROM mer_wealth_dev.mer_wealth_landing_edge.mscs_mrt_account_summary
WHERE databaseCode = 'ST000'
    AND exitDateRecorded >= '2026-01-01'
    AND exitDateRecorded < '2026-10-01'
GROUP BY
    DATE_FORMAT(exitDateRecorded, 'yyyy-MM'),
    exitType
ORDER BY exit_month, exitType;
