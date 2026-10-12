1. How much past member behaviour should we use to predict churn?
   Example: Previous 12 months before the AsOfDate.

2. At what point in time should we take the member snapshot for prediction — month-end, quarter-end, or year-end?
   Example: 31-Mar-2024, 30-Jun-2024, or 31-Dec-2024.

3. After the prediction date, how long should we observe the member to determine whether they churned?
   Example: 3 months after the AsOfDate.

4. Should the churn observation period start from the day after the prediction date?
   Example: AsOfDate 31-Mar-2024 → Outcome starts 01-Apr-2024.

5. Should newly joined accounts be included even if they have only a short history before the prediction date?
   Example: Include accounts with 1, 3, or 6 months of history, or allow no minimum tenure.

6. Should an account be included in modelling only when AccountSummary data is available, or should valid accounts without AccountSummary also be included?
   Example: Account exists but AccountSummary data is missing — include or exclude?
