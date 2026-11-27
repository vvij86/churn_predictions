SELECT
    DATEFROMPARTS(
        YEAR(exitDate),
        MONTH(exitDate),
        1
    ) AS month_start,
    COUNT(DISTINCT accountID) AS exit_account_count
FROM edgeSource.AccountSummary
WHERE exitDate >= '2024-01-01'
  AND exitDate < '2026-11-01'
  AND exitType = 'Exit'
GROUP BY
    YEAR(exitDate),
    MONTH(exitDate)
ORDER BY month_start;



SELECT
    fundID,
    DATEFROMPARTS(
        YEAR(exitDate),
        MONTH(exitDate),
        1
    ) AS month_start,
    COUNT(DISTINCT accountID) AS exit_account_count
FROM edgeSource.AccountSummary
WHERE exitDate >= '2026-01-01'
  AND exitDate < '2026-11-01'
  AND exitType = 'Exit'
GROUP BY
    fundID,
    YEAR(exitDate),
    MONTH(exitDate)
ORDER BY fundID, month_start;
