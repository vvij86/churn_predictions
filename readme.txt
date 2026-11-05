SELECT
    accountID,
    COUNT(DISTINCT fundID) AS fund_count
FROM edgeSource.accountSummary
GROUP BY accountID
HAVING COUNT(DISTINCT fundID) > 1
ORDER BY fund_count DESC, accountID;
