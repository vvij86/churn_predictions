/* Investment Switch */

SUM(
    CASE
        WHEN event_category = 'INVESTMENT_SWITCH'
        THEN 1 ELSE 0
    END
) AS investment_switch_count_12m,

SUM(
    CASE
        WHEN event_category = 'INVESTMENT_SWITCH'
         AND eventDate >= @Recent90Start
        THEN 1 ELSE 0
    END
) AS recent_investment_switch_count_90d,

DATEDIFF(
    DAY,
    MAX(
        CASE
            WHEN event_category = 'INVESTMENT_SWITCH'
            THEN eventDate
        END
    ),
    @AsOfDate
) AS days_since_last_investment_switch
