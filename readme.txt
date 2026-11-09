Update only the Helpline "ROLLOVER_CONSOLIDATION_INTENT" logic in "behavioural_features_business_review.sql".

Do not modify any other Helpline feature and do not modify any other feature block.

We validated the live "inquiryDescription" values and found that the existing broad logic using:

- "LIKE '%Roll out%'"
- "LIKE '%Choice%'"
- "LIKE '%Consolidat%'"

is too broad.

The live values included:

- "Choice of Fund"
- "Benefit Payment / Choice / Portability"
- "Choice/Consolidate Super"
- "MST good choices"
- "Investment Choice - change"
- "Consolidation Inbound"
- "Investment Choice advice"
- "Consolidation Outbound"

Based on this validation:

1. Remove generic matching on "%Choice%".

2. Do not treat these as rollover/consolidation exit intent:
   
   - "Choice of Fund"
   - "MST good choices"
   - "Investment Choice - change"
   - "Investment Choice advice"
   - "Consolidation Inbound"

3. Treat "Consolidation Outbound" as a valid strong rollover/consolidation exit-intent signal.

4. Treat "Choice/Consolidate Super" as a valid rollover/consolidation intent signal for now.

5. Do not include "Benefit Payment / Choice / Portability" in this feature yet because its meaning is ambiguous and requires separate business confirmation.

6. If there are genuine source values containing explicit "Roll out" wording, retain those as valid exit-intent matches.

7. Replace the current broad text logic with a controlled rule similar to:

- exact "inquiryDescription = 'Consolidation Outbound'"
- exact "inquiryDescription = 'Choice/Consolidate Super'"
- OR explicit "inquiryDescription LIKE '%Roll out%'"

Do not use generic "%Choice%".
Do not use generic "%Consolidat%" without excluding inbound/non-exit values.

8. Keep the existing features:
   
   - "rollover_consolidation_inquiry_count_12m"
   - "recent_rollover_consolidation_inquiry_count_90d"
   - "recent_rollover_inquiry_flag_30d"

9. Preserve:
   
   - existing 12-month feature window
   - 90-day logic
   - 30-day logic
   - source date <= "@AsOfDate"
   - one row per "accountID"

10. Add:

"-- BUSINESS REVIEW CHANGE - LIVE DATA VALIDATED"

around the modified Point 4 logic.

After updating, run live validation using the existing DB connection pattern from "sample.py".

Validate and report:

- number of accounts with rollover/consolidation intent > 0
- distinct "inquiryDescription" values captured by the new rule
- top 20 raw matching records
- confirm "Consolidation Inbound" count captured = 0
- confirm "Investment Choice - change" count captured = 0
- confirm "Investment Choice advice" count captured = 0
- confirm "MST good choices" count captured = 0
- confirm "Choice of Fund" count captured = 0
- confirm duplicate accountID count in the final Helpline aggregation = 0
- confirm source records after "@AsOfDate" = 0

Do not make any other SQL changes.

At the end provide:

- exact old rule
- exact new rule
- captured distinct inquiry values
- excluded distinct inquiry values
- PASS / REVIEW / FAIL result
