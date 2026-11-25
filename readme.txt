SELECT
    DATE_TRUNC('MONTH', processedDate) AS rollover_month,
    COUNT(DISTINCT accountID) AS rollover_accounts
FROM mer_wealth_dev.mer_wealth_landing_edge.mscs_mrt_account_rollover_payment
WHERE processedDate >= '2025-10-01'
    AND processedDate < '2026-10-01'
    AND paymentType IN (
        'Rollover to External Fund',
        'Rollover/Transfer to Annuity'
    )
    AND COALESCE(CAST(partialWithdrawalFlag AS BOOLEAN), FALSE) = FALSE
    AND COALESCE(CAST(internalTransferFlag AS BOOLEAN), FALSE) = FALSE
    AND paymentAmount <> 0
GROUP BY DATE_TRUNC('MONTH', processedDate)
ORDER BY rollover_month;
