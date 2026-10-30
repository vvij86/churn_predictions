SELECT
    COUNT(*) AS total_accounts,
    SUM(CASE
        WHEN investment_switch_count_12m > 0
        THEN 1 ELSE 0
    END) AS accounts_with_investment_change,
    MAX(investment_switch_count_12m) AS max_switch_count,
    SUM(CASE
        WHEN recent_investment_switch_count_90d
             > investment_switch_count_12m
        THEN 1 ELSE 0
    END) AS invalid_recent_counts
FROM #behavioural_features;
