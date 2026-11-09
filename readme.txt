Please correct only the duplicate-account validation. Do not modify any feature SQL.

The previous result showed:

duplicate accountID count = 373,528

but also stated that the final Campaign/Event aggregation contains exactly one row per accountID.

These two statements need to be reconciled.

Validate duplicates ONLY on the FINAL Campaign/Event account-level aggregate after all Campaign/Event rows have been grouped by accountID.

Do NOT count repeated accountIDs in the raw campaign_event_base/event-level CTE, because multiple events per account are expected before aggregation.

Run a check equivalent to:

SELECT accountID, COUNT() AS row_count
FROM <final_campaign_account_level_result>
GROUP BY accountID
HAVING COUNT() > 1;

Report only:

- raw/event-level repeated accountIDs = X  -- informational only
- final aggregated duplicate accountIDs = X
- final Campaign/Event grain = one row per accountID: YES / NO
- PASS / FAIL

PASS only when final aggregated duplicate accountIDs = 0.

Do not change the SQL.
