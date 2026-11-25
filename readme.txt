Follow ".github/copilot-instructions.md" and "AGENTS.md".

Review the newly created "ml_mscs_mrt_historical_coverage.py" and its integration with the modified feature modules.

Confirm the following:

- Historical coverage is not incorrectly determined by an individual account's first transaction or activity date.
- Account eligibility continues to use fundJoinDate and existing approved base population rules.
- reportingDate is not used for as-of-date filtering.
- Newly joined accounts remain eligible.
- Partial historical windows are correctly distinguished from completely unavailable windows.
- Earliest source event date is not treated as proof of continuous source coverage.
- AccountEngagementWeb features remain NULL when the source is empty.
- No permanent table writes occur during the proposed manual validation.

Report any issues with exact file and line references.

Do not modify any files or execute any code.
