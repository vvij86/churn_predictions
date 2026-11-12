Update only the Insurance Behaviour / Cover Position section in behavioural_features_business_review.sql.

Business review decision:
The client review document already marks the non-amount insurance features as acceptable/green. Do not introduce unnecessary REVIEW status for those features.

Keep these active features unchanged:
- has_death_cover_asof
- has_tpd_cover_asof
- has_ip_cover_asof
- insurance_cover_type_count_asof

De-scope only these amount features:
- death_cover_amount_asof
- tpd_cover_amount_asof
- ip_cover_amount_asof

Reason:
- The client comments specifically question whether Death, TPD and IP cover amounts provide meaningful behavioural importance.
- Live validation showed the amount fields are effectively redundant with the corresponding cover-presence flags and mainly represent product/financial cover position rather than behavioural activity.
- Therefore retain the cover-presence flags and the cover-type count, but remove the three monetary amount fields from the active Insurance feature output.

Requirements:
1. Modify only the Insurance Behaviour / Cover Position block.
2. Do not change any other feature section.
3. Preserve the existing point-in-time filtering:
   - effectiveDateFrom <= @AsOfDate
   - effectiveDateTo IS NULL OR effectiveDateTo > @AsOfDate
4. Preserve one row per accountID.
5. Preserve:
   - has_death_cover_asof
   - has_tpd_cover_asof
   - has_ip_cover_asof
   - insurance_cover_type_count_asof
6. Remove/de-scope from the final active SELECT:
   - death_cover_amount_asof
   - tpd_cover_amount_asof
   - ip_cover_amount_asof
7. Do not change the source table or insurance mapping logic unless required only to remove those output columns.
8. Validate after the change:
   - duplicate accountID count = 0
   - one row per accountID
   - post-AsOfDate rows entering feature logic = 0
   - all four retained insurance features still exist in final output
   - all three amount fields are no longer active in final output

Return only:
- exact SQL changes made
- final active Insurance feature list
- de-scoped feature list
- validation results
- PASS / FAIL

Do not modify any other feature block.
