import pytest

from database.db import get_connection, initialize_database


@pytest.fixture(autouse=True)
def isolated_test_database(tmp_path, monkeypatch):
    """Give every test its own temporary database."""

    test_database = tmp_path / "test_tenantease.db"

    monkeypatch.setenv(
        "TENANTEASE_DB_PATH",
        str(test_database),
    )

    initialize_database()

    with get_connection() as connection:

        # Create sample properties.
        connection.executemany(
            """
            INSERT INTO properties (
                property_id,
                property_name,
                address,
                city,
                property_type
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            [
                (1, "Test Property A", "Address A", "Test City", "Apartment"),
                (2, "Test Property B", "Address B", "Test City", "Apartment"),
            ],
        )

        # Rooms 103 and 203 are vacant in the test database.
        connection.executemany(
            """
            INSERT INTO rooms (
                room_id,
                property_id,
                room_number,
                monthly_rent,
                status
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            [
                (1, 1, "103", 10000, "vacant"),
                (2, 2, "203", 12000, "vacant"),
            ],
        )

        # Create tenants for payment tests.
        # Each tenant has a separate room.
        connection.executemany(
            """
            INSERT INTO tenants (
                tenant_id,
                room_id,
                tenant_name,
                email,
                phone,
                lease_start,
                lease_end
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            [
                (
                    1, 1, "Priya Verma", "priya@example.com",
                    "9876543210", "2026-01-01", "2026-12-31"
                ),
                (
                    2, 2, "Amit Kumar", "amit@example.com",
                    "9876543211", "2026-01-01", "2026-12-31"
                ),
            ],
        )

        # October sample payments:
        # Total due = 82,000
        # Total paid = 34,000
        # Outstanding = 48,000
        connection.executemany(
            """
            INSERT INTO payments (
                tenant_id,
                rent_month,
                amount_due,
                amount_paid,
                due_date,
                payment_date,
                status
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            [
                (
                    1, "2026-10", 40000, 10000,
                    "2026-10-10", "2026-10-05", "partial"
                ),
                (
                    2, "2026-10", 42000, 24000,
                    "2026-10-15", "2026-10-12", "partial"
                ),
            ],
        )

        connection.commit()