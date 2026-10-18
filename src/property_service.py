from database.db import get_connection


def get_dashboard_metrics():
    """Calculate key property and rental metrics."""

    with get_connection() as connection:

        # Total properties
        total_properties = connection.execute(
            "SELECT COUNT(*) FROM properties"
        ).fetchone()[0]

        # Total rooms
        total_rooms = connection.execute(
            "SELECT COUNT(*) FROM rooms"
        ).fetchone()[0]

        # Occupied rooms
        occupied_rooms = connection.execute(
            """
            SELECT COUNT(*)
            FROM rooms
            WHERE status = 'occupied'
            """
        ).fetchone()[0]

        # Vacant rooms
        vacant_rooms = connection.execute(
            """
            SELECT COUNT(*)
            FROM rooms
            WHERE status = 'vacant'
            """
        ).fetchone()[0]

        # Expected monthly rent from occupied rooms
        expected_rent = connection.execute(
            """
            SELECT COALESCE(SUM(monthly_rent), 0)
            FROM rooms
            WHERE status = 'occupied'
            """
        ).fetchone()[0]

        # Total rent collected for October 2026
        rent_collected = connection.execute(
            """
            SELECT COALESCE(SUM(amount_paid), 0)
            FROM payments
            WHERE rent_month = ?
            """,
            ("2026-10",),
        ).fetchone()[0]

        # Outstanding rent for October 2026
        outstanding_rent = connection.execute(
            """
            SELECT COALESCE(SUM(amount_due - amount_paid), 0)
            FROM payments
            WHERE rent_month = ?
            """,
            ("2026-10",),
        ).fetchone()[0]

    return {
        "total_properties": total_properties,
        "total_rooms": total_rooms,
        "occupied_rooms": occupied_rooms,
        "vacant_rooms": vacant_rooms,
        "expected_rent": expected_rent,
        "rent_collected": rent_collected,
        "outstanding_rent": outstanding_rent,
    }


def get_tenant_payment_records():
    """Return tenant payment records for October 2026."""

    with get_connection() as connection:

        rows = connection.execute(
            """
            SELECT
                t.tenant_name,
                pr.property_name,
                r.room_number,
                p.rent_month,
                p.amount_due,
                p.amount_paid,
                (p.amount_due - p.amount_paid) AS outstanding_amount,
                p.due_date,
                p.status
            FROM payments p
            JOIN tenants t
                ON p.tenant_id = t.tenant_id
            JOIN rooms r
                ON t.room_id = r.room_id
            JOIN properties pr
                ON r.property_id = pr.property_id
            WHERE p.rent_month = ?
            ORDER BY p.due_date
            """,
            ("2026-10",),
        ).fetchall()

    return [dict(row) for row in rows]