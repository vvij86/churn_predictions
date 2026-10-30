DECLARE @AsOfDate DATE = '2026-10-20';

DECLARE @FeatureStartDate DATE =
    DATEADD(DAY, 1, DATEADD(MONTH, -12, @AsOfDate));

SELECT
    ce.eventID,
    ce.eventName,
    COUNT(*) AS event_count,
    COUNT(DISTINCT ced.accountID) AS account_count,
    COUNT(ced.eventAmount) AS amount_available_count,
    MIN(ced.eventAmount) AS min_amount,
    MAX(ced.eventAmount) AS max_amount,
    SUM(ced.eventAmount) AS total_amount
FROM edgeSource.campaignEventDetails ced
INNER JOIN edgeSource.campaignEvents ce
    ON ced.eventID = ce.eventID
WHERE ce.eventID IN (14, 27, 28)
  AND ced.eventDate >= @FeatureStartDate
  AND ced.eventDate < DATEADD(DAY, 1, @AsOfDate)
GROUP BY
    ce.eventID,
    ce.eventName
ORDER BY ce.eventID;
