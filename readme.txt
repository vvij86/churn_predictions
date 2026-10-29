Do not make any further SQL changes.

The feature count appears inconsistent.

Before restoring the requested features, the retained feature count was reported as 108.

Only these 5 features were restored:

- website_login_count_12m
- website_login_count_90d
- website_login_count_30d
- days_since_last_website_login
- insurance_opt_in_12m_flag

Therefore, if no other feature was restored or added, the expected final feature count should be 113, not 124.

Please re-check the feature count.

Important:

- Count ONLY the final feature columns returned by the final SELECT of each standalone feature query.
- Do NOT count:
  - CTE columns
  - intermediate/helper aliases
  - source columns
  - eligibility columns
  - calculated fields used only internally
  - accountID
  - AsOfDate
  - duplicated aliases appearing in multiple CTEs
  - comments/documentation feature names

For every standalone query, identify its final SELECT feature columns and count them exactly once.

Then provide:

1. Total final retained feature count
2. Feature count by feature group
3. List of final feature names under each group
4. Confirm whether the only restored features compared with the 108-feature version are the 5 listed above
5. If the total is not 113, explain exactly which additional final features account for the difference.

Do not edit "behavioural_features_business_review.sql" during this verification. This is a count/validation exercise only.
