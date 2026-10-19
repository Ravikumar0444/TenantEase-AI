import sqlite3
from pathlib import Path

# Use the same database file as database/db.py.
# This assumes the database file is named tenantease.db
# and is stored in the project root.
DB_PATH = Path(__file__).resolve().parent / "tenantease.db"


def migrate_tenant_deactivation():
    connection = sqlite3.connect(str(DB_PATH))

    try:
        columns = connection.execute(
            "PRAGMA table_info(tenants)"
        ).fetchall()

        if not columns:
            raise RuntimeError(
                f"No tenants table found in {DB_PATH}. "
                "Check the database path before continuing."
            )

        column_names = [column[1] for column in columns]

        if "is_active" not in column_names:
            connection.execute(
                """
                ALTER TABLE tenants
                ADD COLUMN is_active INTEGER NOT NULL DEFAULT 1
                CHECK (is_active IN (0, 1))
                """
            )
            print("Added is_active column.")
        else:
            print("is_active column already exists.")

        connection.commit()
        print("Migration completed successfully.")

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


if __name__ == "__main__":
    print(f"Database path: {DB_PATH}")
    migrate_tenant_deactivation()