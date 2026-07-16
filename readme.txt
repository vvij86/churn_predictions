The profiling confirms that ROLLOVER.PARTIAL_FULL_FLAG is NULL for all
3,179,576 rows, so it cannot be used.

For Version 1, I want to investigate whether EXIT_TYPE can identify:
- full rollover out
- partial rollover out
- internal transfer
- account closure due to full exit
- death-related exits

Please generate read-only SQL profiling queries that:

1. List every distinct ROLLOVER.EXIT_TYPE_ID.
2. Join to EXIT_TYPE and display all relevant code, description and
   death-indicator columns.
3. Show rollover row count and distinct account count for every exit type.
4. Show minimum and maximum DATE_RECEIVED for every exit type.
5. Show the distribution by year for every exit type.
6. Search descriptions for words such as:
   FULL, PARTIAL, ROLLOVER, TRANSFER, CLOSURE, WITHDRAWAL and DEATH.
7. Do not assume which values mean full or partial.
8. Clearly separate data findings from items requiring BA or SME confirmation.
9. Do not generate the final training dataset SQL yet.
