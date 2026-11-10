Update ONLY the Workflow Behaviour section in behavioural_features_business_review.sql.

Do not change Helpline, Campaign/Event, Website Engagement, or any other feature block.

We have completed live validation of the current Workflow features. Apply the following conservative changes based on the validated results.

1. DE-SCOPE MEMBER_DETAIL_CHANGE
Reason:
- 324,438 rows but only 575 distinct accounts.
- 569 accounts have repeated updates.
- Average rows per account ~564; max rows per account 4,689.
- Mostly operational values such as Update Contact Details / Update Communication Preferences.
- This is repetitive administration activity, not a strong retention signal.

Therefore:
- Remove/comment out member_detail_change_count_12m from active ML output.
- Preserve the existing mapping logic as commented reference code.
- Add a comment:
  -- BUSINESS REVIEW: De-scoped because activity is dominated by repeated operational contact/admin updates and is not a strong standalone retention signal.

2. DE-SCOPE MEMBER_INQUIRY_SERVICE
Reason:
- Only 24 rows across 6 distinct accounts.
- Very sparse coverage.
- This is not sufficient as a standalone ML behavioural feature.

Therefore:
- Remove/comment out member_inquiry_service_count_12m.
- Remove/comment out recent_member_inquiry_service_count_90d.
- Preserve mapping logic for future review.
- Add a comment explaining low coverage.

3. DE-SCOPE COMPLAINT_ESCALATION
Reason:
- Only 12 rows across 5 distinct accounts.
- This matches the earlier Helpline business concern that the available complaint data represents only a small subset of overall complaints.
- Do not treat this source as complete complaint coverage.

Therefore:
- Remove/comment out complaint_escalation_count_12m.
- Remove/comment out recent_complaint_escalation_count_90d.
- Preserve the mapping logic as commented reference.
- Add comment:
  -- BUSINESS REVIEW: De-scoped because Workflow complaint/escalation coverage is extremely sparse and represents only a subset of complaint activity. Broader complaint data may be required later.

4. BENEFICIARY_ACTIVITY
Live validation showed:
- 3,547 workflow rows.
- 3,428 distinct accounts.
- 3,382 of the 3,428 workflow beneficiary accounts overlap with the existing Campaign/Event beneficiary feature.
- Therefore this is meaningful activity but largely duplicated by the already-retained Campaign/Event beneficiary feature.

Since Campaign/Event beneficiary_event_count_12m is already retained, de-scope the Workflow beneficiary feature to avoid duplicated ML evidence.

Therefore:
- Remove/comment out beneficiary_change_count_12m from active Workflow output.
- Preserve the mapping logic for traceability.
- Add comment:
  -- BUSINESS REVIEW: De-scoped from Workflow because the same beneficiary behaviour is already captured by the retained Campaign/Event beneficiary feature; avoiding duplicate ML signal.

Important:
- Do NOT remove the source CTE mappings completely. Comment/de-scope the output features so the logic remains traceable for future review.
- Do NOT modify the Campaign/Event beneficiary feature.
- Do NOT modify Website Engagement.
- Do NOT modify any date-window logic.
- Keep @FeatureStartDate, @AsOfDate, and recent-window logic unchanged.
- Final Workflow grain must remain one row per accountID.
- Do not introduce any post-AsOfDate data.
- Do not change eligibility logic.

After making the change, run live validation and report only:

1. post-AsOfDate rows entering Workflow feature logic = X
2. pre-FeatureStartDate rows entering Workflow feature logic = X
3. final aggregated duplicate accountID count = X
4. final Workflow grain one row per accountID = YES/NO
5. confirm these features are NOT active:
   - member_detail_change_count_12m
   - member_inquiry_service_count_12m
   - recent_member_inquiry_service_count_90d
   - complaint_escalation_count_12m
   - recent_complaint_escalation_count_90d
   - beneficiary_change_count_12m
6. confirm the Campaign/Event beneficiary_event_count_12m remains active and unchanged.
7. PASS / REVIEW / FAIL

Also show exactly which Workflow SQL lines/features were changed.
