SELECT
    ce.eventID,
    ce.eventName,
    COUNT(*) AS event_count,
    COUNT(DISTINCT ced.accountID) AS account_count,
    MIN(ced.eventDate) AS first_event_date,
    MAX(ced.eventDate) AS last_event_date
FROM edgeSource.campaignEventDetails ced
INNER JOIN edgeSource.campaignEvents ce
    ON ced.eventID = ce.eventID
WHERE ce.eventID IN (
    7,              -- INVESTMENT_SWITCH
    9, 10, 11, 12,  -- INFLOW
    14, 27, 28,     -- OUTFLOW
    13, 21, 25,     -- RETIREMENT_PATHWAY
    30              -- INSURANCE_CHANGE
)
GROUP BY
    ce.eventID,
    ce.eventName
ORDER BY
    ce.eventID;
