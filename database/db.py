import os
import sqlite3
from pathlib import Path

# Project directory
BASE_DIR = Path(__file__).resolve().parent.parent

# SQL schema location
SCHEMA_PATH = BASE_DIR / "database" / "schema.sql"


def get_database_path():
    """
    Return the configured database path.

    The application uses tenantease.db by default.
    Tests can specify a separate database using TENANTEASE_DB_PATH.
    """
    configured_path = os.environ.get("TENANTEASE_DB_PATH")

    if configured_path:
        return Path(configured_path)

    return BASE_DIR / "tenantease.db"


def get_connection():
    """Create and return a SQLite database connection."""

    connection = sqlite3.connect(get_database_path())
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")

    return connection


def initialize_database():
    """Create database tables if they do not exist."""

    with get_connection() as connection:
        schema = SCHEMA_PATH.read_text(encoding="utf-8")
        connection.executescript(schema)


if __name__ == "__main__":
    initialize_database()
    print(f"Database initialized: {get_database_path()}")