During ML historical churn validation, I identified significant bulk exits under ST000 during March and April 2026.

Further investigation revealed that these exits are largely associated with Payment to ATO, particularly:

- Inactive Low Balance Account – 27,629 accounts
- Trustee Voluntary Payment – 5,723 accounts

These payment records have internalTransferFlag = 0.

Could you please confirm whether ATO-related account closures should be considered churn or excluded from our ML churn definition, as these may represent regulatory or administrative exits rather than voluntary member exits?
