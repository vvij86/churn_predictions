SELECT
    databaseCode,
    DATE_FORMAT(exitDateRecorded, 'yyyy-MM') AS exit_month,
    COUNT(DISTINCT accountID) AS exit_accounts
FROM mer_wealth_dev.mer_wealth_landing_edge.mscs_mrt_account_summary
WHERE exitDateRecorded >= '2026-01-01'
    AND exitDateRecorded < '2026-10-01'
    AND exitType = 'Exit'
GROUP BY
    databaseCode,
    DATE_FORMAT(exitDateRecorded, 'yyyy-MM')
ORDER BY databaseCode, exit_month;
