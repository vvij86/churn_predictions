Review ONLY the Workflow Behaviour section in "behavioural_features_business_review.sql".

Do NOT change the SQL yet.

Use the existing live database connection pattern from "sample.py" and validate the current Workflow features against live source data.

The Workflow categories currently identified are:

- "MEMBER_DETAIL_CHANGE"
- "BENEFICIARY_ACTIVITY"
- "MEMBER_INQUIRY_SERVICE"
- "COMPLAINT_ESCALATION"

Current live validation already showed approximately:

- MEMBER_DETAIL_CHANGE: 324,438 rows / 575 distinct accounts
- BENEFICIARY_ACTIVITY: 3,547 rows / 3,428 distinct accounts
- MEMBER_INQUIRY_SERVICE: 24 rows / 6 distinct accounts
- COMPLAINT_ESCALATION: 12 rows / 5 distinct accounts

Tasks:

1. Identify the exact output feature columns currently generated from each of the above Workflow categories.

2. For every feature, report:
   
   - source workflow value / description used
   - 12-month account coverage
   - 90-day account coverage if applicable
   - whether it overlaps with another existing feature block
   - business interpretation in simple terms
   - recommendation: "KEEP", "REVIEW", or "DE-SCOPE"

3. Specifically check "MEMBER_DETAIL_CHANGE" for overlap with any existing:
   
   - contact-detail
   - account administration
   - member-detail
   - helpline
     features.
   
   Do not assume that its high row count means it is useful. Check whether the same small set of accounts is generating many repeated operational updates.

4. For "BENEFICIARY_ACTIVITY", confirm exactly what behaviour it represents from the source values and whether it is sufficiently distinct from other beneficiary-related features already present elsewhere in the SQL.

5. For "MEMBER_INQUIRY_SERVICE", confirm the actual source descriptions/events that map into this category and explain why coverage is very low.

6. For "COMPLAINT_ESCALATION", explicitly apply the earlier business concern from the Helpline review:
   complaints captured in these operational sources may represent only a small subset of all complaints.
   
   Check:
   
   - exact source values being mapped
   - number of distinct accounts
   - whether the signal is too sparse to be relied on as a standalone ML feature
   - whether a broader complaint source may be required later

7. Validate technical integrity:
   
   - no records after "@AsOfDate"
   - no records before "@FeatureStartDate"
   - final output grain remains one row per "accountID"
   - final duplicate "accountID" count = 0

8. Do NOT remove any Workflow feature in this step.

Return a concise decision table like:

Workflow category| Current feature(s)| Coverage| Overlap concern| Recommendation| Reason

Then provide a short final recommendation:

- which features are safe to KEEP
- which should remain under REVIEW
- which are candidates for DE-SCOPE

Do not modify any non-Workflow section.
Do not change Website Engagement.
Do not infer business meaning from feature names alone; base conclusions on actual source values and live data.
