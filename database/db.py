import sqlite3
from pathlib import Path

# Project directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Database file location
DATABASE_PATH = BASE_DIR / "tenantease.db"

# SQL schema location
SCHEMA_PATH = BASE_DIR / "database" / "schema.sql"


def get_connection():
    """Create and return a SQLite database connection."""

    connection = sqlite3.connect(DATABASE_PATH)

    # Return database rows that can be accessed by column name.
    connection.row_factory = sqlite3.Row

    # Enable foreign-key validation.
    connection.execute("PRAGMA foreign_keys = ON")

    return connection


def initialize_database():
    """Create database tables if they do not exist."""

    with get_connection() as connection:
        schema = SCHEMA_PATH.read_text(encoding="utf-8")
        connection.executescript(schema)


if __name__ == "__main__":
    initialize_database()
    print(f"Database initialized: {DATABASE_PATH}")