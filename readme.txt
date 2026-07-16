Please correct the external rollover definition in Queries 4, 5 and 6.

External rollover must mean:

EXIT_TYPE.IS_ROLLOVER_FLAG = 'Y'
AND EXIT_TYPE.IS_INTERNAL_FLAG is not 'Y'
AND EXIT_TYPE.IS_DEATH_FLAG is not 'Y'

Do not treat every non-internal exit as an external rollover.

Regenerate only Queries 4, 5 and 6.
Do not regenerate the other queries.
