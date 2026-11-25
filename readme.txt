SELECT
    r.paymentType,
    r.paymentDescription,
    r.internalTransferFlag,
    COUNT(DISTINCT a.accountID) AS account_count
FROM Edge.AccountSummary a
INNER JOIN Edge.AccountRolloverPayment r
    ON a.accountID = r.accountID
WHERE a.databaseCode = 'ST000'
    AND a.exitType = 'Exit'
    AND a.exitDateRecorded >= '2026-03-01'
    AND a.exitDateRecorded < '2026-05-01'
    AND r.paymentType = 'Payment to ATO'
    AND CONVERT(VARCHAR(7), a.exitDateRecorded, 120)
        = CONVERT(VARCHAR(7), r.processedDate, 120)
GROUP BY
    r.paymentType,
    r.paymentDescription,
    r.internalTransferFlag
ORDER BY account_count DESC;
