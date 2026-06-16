Please find my response below for Q4 and Q5.

1. Name of the metric for which this information is needed

This information is needed for the Retention Rate ML/AI use case, mainly for:

- Retention Rate - Member
- Retention Rate - FUM

2. Design of the solution

The solution will use historical member/account data over the rolling 12-month period as input.

The input data may include account status, account closure/exits, rollover out details, FUM/account balance, dormant/inactive status, and related member/account attributes.

This information will be used to create the ML target label for retention/churn prediction:

- Retained: member/account remains with Mercer at the end of 12 months and has FUM
- Not retained/churn: full rollover out or account closure due to full exit
- Churn risk/FUM leakage: partial rollover out, where the member/account remains but part of FUM is lost
- Dormant/inactive: retained if still with Mercer and has FUM
- Death: to be handled based on the business rule, either excluded as natural attrition or treated as not retained only if account/FUM is fully exited

3. Expected output of the solution

The expected ML output will be at the confirmed measurement level, mainly account level as per the BRS metric table, with possible output columns such as:

- Member ID
- Account ID
- Retention/churn prediction label
- Churn probability/risk score
- Retention category
- Key contributing factors/drivers
- FUM at start of period
- FUM at end of period
- FUM retained/lost indicator

I will use this understanding to draft the FRS.
