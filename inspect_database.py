import sqlite3
from database.db import DATABASE_PATH

connection = sqlite3.connect(DATABASE_PATH)

print("\n========== DATABASE TABLES ==========")

tables = connection.execute(
    "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
).fetchall()

for table in tables:
    table_name = table[0]

    print(f"\nTable: {table_name}")

    columns = connection.execute(
        f"PRAGMA table_info('{table_name}')"
    ).fetchall()

    for column in columns:
        print(f"  Column: {column[1]} | Type: {column[2]}")

    count = connection.execute(
        f'SELECT COUNT(*) FROM "{table_name}"'
    ).fetchone()[0]

    print(f"  Total records: {count}")

connection.close()

print("\n========== INSPECTION COMPLETE ==========")