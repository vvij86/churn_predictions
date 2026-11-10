Update ONLY the Workflow Behaviour section in "behavioural_features_business_review.sql".

Based on the completed live-data validation, de-scope the generic Workflow feature group from the active ML output.

The validation confirmed that the generic "meaningful_workflow_*" features aggregate the same four Workflow categories already reviewed:

- MEMBER_DETAIL_CHANGE
- BENEFICIARY_ACTIVITY
- MEMBER_INQUIRY_SERVICE
- COMPLAINT_ESCALATION

The live data showed:

- MEMBER_DETAIL_CHANGE = 324,438 events across 575 accounts and is dominated by repetitive operational/contact-admin updates.
- BENEFICIARY_ACTIVITY overlaps strongly with the retained Campaign/Event beneficiary feature.
- MEMBER_INQUIRY_SERVICE is extremely sparse.
- COMPLAINT_ESCALATION is extremely sparse and represents incomplete complaint coverage.

Therefore the generic Workflow aggregate indirectly reintroduces the same de-scoped/overlapping signals and should not remain active.

De-scope these generic Workflow output features:

- meaningful_workflow_count_12m
- meaningful_workflow_active_days_12m
- days_since_last_meaningful_workflow
- recent_meaningful_workflow_count_90d
- recent_meaningful_workflow_count_30d
- completed_meaningful_workflow_count_12m
- open_meaningful_workflow_count_asof

Requirements:

1. Do not delete the SQL logic completely.

2. Comment/de-scope the features from the active final Workflow output so they remain available as reference code.

3. Add a short comment such as:
   
   "-- BUSINESS REVIEW: De-scoped from ML output because the generic Workflow aggregate is dominated by repetitive operational/admin activity and reintroduces categories already de-scoped or captured elsewhere."

4. Keep the existing category-specific de-scoped Workflow logic unchanged.

5. Do not modify any non-Workflow feature section.

6. Do not modify Website Engagement.

7. Preserve the account-level grain: one row per accountID.

8. Validate after the change:
   
   - no records after @AsOfDate
   - no records before @FeatureStartDate
   - duplicate accountID count = 0
   - none of the generic Workflow features appear in the active final output
   - none of the category-specific de-scoped Workflow features appear in the active final output

Return:

- PASS / REVIEW / FAIL
- exact Workflow features de-scoped
- confirmation that no other feature block was changed.
