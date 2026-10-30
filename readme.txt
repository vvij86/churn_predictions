DECLARE @AsOfDate DATE = '2026-10-20';

DECLARE @FeatureStartDate DATE =
    DATEADD(DAY, 1, DATEADD(MONTH, -12, @AsOfDate));

WITH account_exit AS
(
    SELECT
        accountID,
        MIN(CAST(exitDate AS DATE)) AS exitDate
    FROM edgeSource.accountSummary
    WHERE exitDate IS NOT NULL
    GROUP BY accountID
)
SELECT
    CASE
        WHEN a.exitDate IS NULL
            THEN 'No recorded exit'

        WHEN CAST(ced.eventDate AS DATE) < a.exitDate
            THEN 'Before exit'

        WHEN CAST(ced.eventDate AS DATE) = a.exitDate
            THEN 'On exit date'

        ELSE 'After exit'
    END AS event_timing,

    COUNT(*) AS event_count,

    COUNT(DISTINCT ced.accountID) AS account_count,

    SUM(ced.eventAmount) AS total_amount

FROM edgeSource.campaignEventDetails ced

LEFT JOIN account_exit a
    ON ced.accountID = a.accountID

WHERE ced.eventID = 28
  AND ced.eventDate >= @FeatureStartDate
  AND ced.eventDate < DATEADD(DAY, 1, @AsOfDate)

GROUP BY
    CASE
        WHEN a.exitDate IS NULL
            THEN 'No recorded exit'
        WHEN CAST(ced.eventDate AS DATE) < a.exitDate
            THEN 'Before exit'
        WHEN CAST(ced.eventDate AS DATE) = a.exitDate
            THEN 'On exit date'
        ELSE 'After exit'
    END

ORDER BY event_count DESC;
