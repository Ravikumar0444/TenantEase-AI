import sqlite3
from database.db import get_connection, initialize_database


def seed_database():
    """Insert fictional sample data into the database."""

    initialize_database()

    with get_connection() as connection:

        # Prevent duplicate sample data if this script is rerun.
        existing = connection.execute(
            "SELECT COUNT(*) FROM properties"
        ).fetchone()[0]

        if existing > 0:
            print("Sample data already exists. Skipping insertion.")
            return

        # --------------------------------------------------
        # 1. Properties
        # --------------------------------------------------

        properties = [
            (
                "Green Valley Apartments",
                "12 Park Street",
                "Ghaziabad",
                "Residential"
            ),
            (
                "Sunrise Residency",
                "25 Market Road",
                "Noida",
                "Residential"
            ),
            (
                "Lakeview Homes",
                "8 Lake Road",
                "Delhi",
                "Residential"
            ),
        ]

        connection.executemany(
            """
            INSERT INTO properties
            (property_name, address, city, property_type)
            VALUES (?, ?, ?, ?)
            """,
            properties,
        )

        # --------------------------------------------------
        # 2. Rooms
        # --------------------------------------------------

        rooms = [
            (1, "101", 10000, "occupied"),
            (1, "102", 12000, "occupied"),
            (1, "103", 9000, "vacant"),
            (2, "201", 15000, "occupied"),
            (2, "202", 11000, "occupied"),
            (2, "203", 13000, "vacant"),
            (3, "301", 18000, "occupied"),
            (3, "302", 16000, "occupied"),
        ]

        connection.executemany(
            """
            INSERT INTO rooms
            (property_id, room_number, monthly_rent, status)
            VALUES (?, ?, ?, ?)
            """,
            rooms,
        )

        # --------------------------------------------------
        # 3. Tenants
        # --------------------------------------------------

        tenants = [
            (1, "Rahul Sharma", "rahul@example.com",
             "9000000001", "2026-01-01", "2026-12-31"),

            (2, "Priya Verma", "priya@example.com",
             "9000000002", "2026-02-01", "2027-01-31"),

            (4, "Amit Kumar", "amit@example.com",
             "9000000003", "2026-03-01", "2027-02-28"),

            (5, "Neha Singh", "neha@example.com",
             "9000000004", "2026-04-01", "2027-03-31"),

            (7, "Arjun Patel", "arjun@example.com",
             "9000000005", "2026-01-01", "2026-12-31"),

            (8, "Sneha Gupta", "sneha@example.com",
             "9000000006", "2026-05-01", "2027-04-30"),
        ]

        connection.executemany(
            """
            INSERT INTO tenants
            (room_id, tenant_name, email, phone, lease_start, lease_end)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            tenants,
        )

        # --------------------------------------------------
        # 4. Rent payments
        # --------------------------------------------------

        payments = [
            # tenant_id, month, due, paid, due_date, payment_date, status

            (1, "2026-10", 10000, 10000,
             "2026-10-05", "2026-10-04", "paid"),

            (2, "2026-10", 12000, 5000,
             "2026-10-05", "2026-10-06", "partial"),

            (3, "2026-10", 15000, 0,
             "2026-10-05", None, "overdue"),

            (4, "2026-10", 11000, 11000,
             "2026-10-05", "2026-10-05", "paid"),

            (5, "2026-10", 18000, 0,
             "2026-10-05", None, "overdue"),

            (6, "2026-10", 16000, 8000,
             "2026-10-05", "2026-10-07", "partial"),

            # Historical records for payment-pattern analysis.
            (1, "2026-09", 10000, 10000,
             "2026-09-05", "2026-09-05", "paid"),

            (2, "2026-09", 12000, 12000,
             "2026-09-05", "2026-09-08", "paid"),

            (3, "2026-09", 15000, 15000,
             "2026-09-05", "2026-09-04", "paid"),
        ]

        connection.executemany(
            """
            INSERT INTO payments
            (
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
            payments,
        )

    print("Sample data inserted successfully!")


if __name__ == "__main__":
    seed_database()