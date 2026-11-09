Do not modify the SQL.

Investigate why the validated "ROLLOVER_CONSOLIDATION_INTENT" rule currently produces 0 accounts for the "@AsOfDate" feature window.

Using the live database, check these accepted source patterns separately:

- "inquiryDescription = 'Consolidation Outbound'"
- "inquiryDescription = 'Choice/Consolidate Super'"
- "inquiryDescription LIKE '%Roll out%'"

For each pattern return:

1. Total record count across all available history.
2. Distinct account count across all available history.
3. Earliest "callDate".
4. Latest "callDate".
5. Record count within the current 12-month feature window for "@AsOfDate = '2024-12-31'".
6. Distinct account count within that same 12-month window.
7. Show up to 20 raw records with:
   - accountID
   - callDate
   - outcomeDescription
   - inquiryDescription

Also check coverage across the available historical period / multiple possible AsOfDate years or months, so we can understand whether this feature has useful historical variation rather than judging it from only the 31-Dec-2024 snapshot.

Do not broaden the rule and do not reintroduce generic "%Choice%" or "%Consolidat%".

At the end explain whether the zero coverage is because:

A. valid events exist but fall outside the current 12-month window,
B. valid events are extremely rare,
C. the accepted values do not actually exist in the source,
or
D. there is an issue in the feature SQL.

Do not make SQL changes yet.
