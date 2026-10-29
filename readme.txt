Please make one small correction to the current reduced version of "behavioural_features_business_review.sql".

Retain the following two feature areas that were removed in the reduction pass:

1. Website login behaviour from campaign/event source
   
   - Keep the previously existing "website_login_*" features that were removed.
   - Preserve their existing 12-month / 90-day / 30-day windows exactly as implemented before removal.
   - Do not change their original source mapping or business logic.
   - These should remain because website-login behaviour is a useful digital engagement signal.

2. Insurance opt-in behaviour
   
   - Restore "insurance_opt_in_12m_flag".
   - Preserve its existing campaign/event source logic exactly as before.
   - Keep it because insurance opt-in represents a distinct member action/engagement signal, which is different from simply having active insurance cover.

Important:

- Do not make any other feature changes.
- Do not restore any other removed features.
- Do not change contribution, rollover, workflow, investment, insurance-as-of, third-party-authority or net-money-flow logic.
- Preserve all existing AsOfDate, point-in-time and leakage protections.
- Preserve 30-day / 90-day / 12-month windows already implemented.
- Recalculate and report:
  - final retained feature count
  - updated feature count by group
- Confirm only these two feature areas were restored.
