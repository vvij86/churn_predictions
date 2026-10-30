DECLARE @AsOfDate DATE = '2026-10-20';

DECLARE @FeatureStartDate DATE =
    DATEADD(DAY, 1, DATEADD(MONTH, -12, @AsOfDate));

SELECT
    ce.eventID,
    ce.eventName,

    COUNT(*) AS total_events,

    SUM(CASE
        WHEN a.exitDate IS NOT NULL
         AND CAST(ced.eventDate AS DATE) =
             CAST(a.exitDate AS DATE)
        THEN 1 ELSE 0
    END) AS events_on_exit_date,

    SUM(CASE
        WHEN a.exitDate IS NOT NULL
         AND ced.eventDate < a.exitDate
        THEN 1 ELSE 0
    END) AS events_before_exit,

    SUM(CASE
        WHEN a.exitDate IS NOT NULL
         AND ced.eventDate > a.exitDate
        THEN 1 ELSE 0
    END) AS events_after_exit

FROM edgeSource.campaignEventDetails ced

INNER JOIN edgeSource.campaignEvents ce
    ON ced.eventID = ce.eventID

LEFT JOIN edgeSource.accountSummary a
    ON ced.accountID = a.accountID

WHERE ce.eventID IN (14, 27, 28)
  AND ced.eventDate >= @FeatureStartDate
  AND ced.eventDate < DATEADD(DAY, 1, @AsOfDate)

GROUP BY
    ce.eventID,
    ce.eventName

ORDER BY ce.eventID;
