# 46. Transitioned Member Exit Exclusion

Business has confirmed that transitioned-member exits must be excluded from normal churn modelling because these exits are caused by transition/migration activity and may skew the churn model.

Reuse the approved `IsTransitionedMemberExit` logic from the business reference SQL.

Rules:

- `IsTransitionedMemberExit = 1` -> exclude from normal churn modelling population / target creation.
- Do not treat transitioned-member exits as ordinary churn.
- Do not use `IsTransitionedMemberExit` as a predictive feature.
- Apply this exclusion together with the existing:
  - internal transfer exclusion
  - death-related exit exclusion

Use the exact business reference logic for determining `IsTransitionedMemberExit`.

Do not simplify or invent alternate transition rules unless explicitly confirmed by business.
