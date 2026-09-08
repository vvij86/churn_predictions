import os
import pyodbc
from dotenv import load_dotenv

# Load values from .env
load_dotenv()

SQL_SERVER = os.getenv("SQL_SERVER")
SQL_DATABASE = os.getenv("SQL_DATABASE")
SQL_DRIVER = os.getenv("SQL_DRIVER", "ODBC Driver 18 for SQL Server")

print("Server:", SQL_SERVER)
print("Database:", SQL_DATABASE)
print("Driver:", SQL_DRIVER)

print("\nAvailable ODBC drivers:")
print(pyodbc.drivers())

connection_string = (
    f"DRIVER={{{SQL_DRIVER}}};"
    f"SERVER={SQL_SERVER};"
    f"DATABASE={SQL_DATABASE};"
    "Trusted_Connection=yes;"
    "TrustServerCertificate=yes;"
)

try:
    print("\nTrying SQL Server connection...")

    conn = pyodbc.connect(connection_string, timeout=10)

    print("SUCCESS: Connected to SQL Server.")

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            @@SERVERNAME AS ServerName,
            DB_NAME() AS DatabaseName,
            SYSTEM_USER AS LoggedInUser
    """)

    row = cursor.fetchone()

    print("\nConnection details:")
    print("Server Name :", row.ServerName)
    print("Database    :", row.DatabaseName)
    print("Windows User:", row.LoggedInUser)

    cursor.execute("SELECT GETDATE()")
    print("SQL Server Time:", cursor.fetchone()[0])

    cursor.close()
    conn.close()

except Exception as e:
    print("\nFAILED: Could not connect to SQL Server.")
    print("Error:")
    print(e)
