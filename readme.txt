SELECT
    jobSourceDescription,
    jobDescription,
    COUNT(*) AS row_count,
    COUNT(DISTINCT accountID) AS account_count
FROM edgeSource.accountEngagementWorkflow
GROUP BY
    jobSourceDescription,
    jobDescription
ORDER BY
    row_count DESC;
