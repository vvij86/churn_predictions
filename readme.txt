SELECT
    DATE_TRUNC('MONTH', exitDateRecorded) AS exit_month,
    COUNT(DISTINCT accountID) AS exit_accounts
FROM mer_wealth_dev.mer_wealth_landing_edge.mscs_mrt_account_summary
WHERE exitDateRecorded >= '2025-10-01'
    AND exitDateRecorded < '2026-10-01'
    AND exitType = 'Exit'
    AND databaseCode IN (
        'MASTA', 'MASTP', 'MASTR', 'MASTS',
        'MASTM', 'MTAPD', 'ST000', 'MASTR_AP'
    )
GROUP BY DATE_TRUNC('MONTH', exitDateRecorded)
ORDER BY exit_month;
