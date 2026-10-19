import sqlite3
from pathlib import Path

db_path = Path(__file__).resolve().parent / "tenantease.db"

connection = sqlite3.connect(str(db_path))

try:
    result = connection.execute(
        """
        SELECT sql
        FROM sqlite_master
        WHERE type = 'table' AND name = 'tenants'
        """
    ).fetchone()

    if result:
        print("Current tenants table schema:")
        print(result[0])
    else:
        print("Tenants table not found.")

finally:
    connection.close()