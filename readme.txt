The SQL Server connection is working successfully in sample.py.
Please reuse the same database connection logic from sample.py for all Phase 2 profiling scripts.
Do not create a different connection approach.
Specifically:
reuse the existing .env values
reuse pyodbc
reuse Windows Trusted Authentication
reuse the same ODBC driver logic
reuse the same server/database environment variables
reuse the same connection string construction
Refactor the working connection code from sample.py into a reusable helper function/module if needed, and make all Phase 2 SQL profiling code call that shared connection function.
Do not change the working connection settings unless necessary.
Before continuing Phase 2 profiling, run a simple connection test using the reused function and confirm it succeeds.
