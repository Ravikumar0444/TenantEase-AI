import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "tenantease.db"


def migrate_room_reassignment():
    connection = sqlite3.connect(str(DB_PATH))

    try:
        connection.execute("PRAGMA foreign_keys = OFF")
        connection.execute("BEGIN")

        schema_row = connection.execute(
            """
            SELECT sql
            FROM sqlite_master
            WHERE type = 'table' AND name = 'tenants'
            """
        ).fetchone()

        if schema_row is None:
            raise RuntimeError("The tenants table was not found.")

        schema = schema_row[0]

        if "room_id INTEGER NOT NULL UNIQUE" not in schema:
            print("The room_id UNIQUE constraint was not found.")
            connection.rollback()
            return

        # Create the replacement table without UNIQUE on room_id.
        connection.execute(
            """
            CREATE TABLE tenants_new (
                tenant_id INTEGER PRIMARY KEY AUTOINCREMENT,
                room_id INTEGER NOT NULL,
                tenant_name TEXT NOT NULL,
                email TEXT,
                phone TEXT,
                lease_start DATE,
                lease_end DATE,
                is_active INTEGER NOT NULL DEFAULT 1
                    CHECK (is_active IN (0, 1)),
                FOREIGN KEY (room_id)
                    REFERENCES rooms(room_id)
            )
            """
        )

        # Copy every tenant record, including inactive status.
        connection.execute(
            """
            INSERT INTO tenants_new (
                tenant_id,
                room_id,
                tenant_name,
                email,
                phone,
                lease_start,
                lease_end,
                is_active
            )
            SELECT
                tenant_id,
                room_id,
                tenant_name,
                email,
                phone,
                lease_start,
                lease_end,
                is_active
            FROM tenants
            """
        )

        # Replace the old table.
        connection.execute("DROP TABLE tenants")
        connection.execute("ALTER TABLE tenants_new RENAME TO tenants")

        connection.commit()
        print("Migration completed successfully.")
        print("Tenant IDs and payment records were preserved.")

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


if __name__ == "__main__":
    migrate_room_reassignment()