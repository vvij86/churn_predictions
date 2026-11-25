SELECT
    DATE_TRUNC('MONTH', exitDateRecorded) AS exit_month,
    COUNT(DISTINCT accountID) AS exit_accounts
FROM mer_wealth_dev.mer_wealth_landing_edge.mscs_mrt_account_summary
WHERE LOWER(TRIM(exitType)) = 'exit'
    AND TO_DATE(exitDateRecorded) >= '2025-01-01'
    AND databaseCode IN (
        'MASTA', 'MASTP', 'MASTR', 'MASTS',
        'MASTM', 'MTAPD', 'ST000', 'MASTR_AP'
    )
GROUP BY DATE_TRUNC('MONTH', exitDateRecorded)
ORDER BY exit_month;
