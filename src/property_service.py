from database.db import get_connection
import sqlite3
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

def add_tenant(
    tenant_name,
    email,
    phone,
    room_id,
    lease_start,
    lease_end,
):
    """
    Add a tenant to a vacant room.

    Returns:
        (True, success_message) if successful.
        (False, error_message) if unsuccessful.
    """

    tenant_name = tenant_name.strip()
    email = email.strip() or None
    phone = phone.strip() or None

    # Validate tenant name.
    if not tenant_name:
        return False, "Tenant name is required."

    # Validate lease dates.
    if lease_start and lease_end and lease_end < lease_start:
        return False, "Lease end date cannot be before lease start date."

    try:
        with get_connection() as connection:

            # Check whether the selected room exists.
            room = connection.execute(
                """
                SELECT room_id, status
                FROM rooms
                WHERE room_id = ?
                """,
                (room_id,),
            ).fetchone()

            if room is None:
                return False, "Selected room does not exist."

            # Check whether the room is vacant.
            if room["status"] != "vacant":
                return False, "This room is already occupied."

            # Insert tenant details.
            connection.execute(
                """
                INSERT INTO tenants (
                    room_id,
                    tenant_name,
                    email,
                    phone,
                    lease_start,
                    lease_end
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    room_id,
                    tenant_name,
                    email,
                    phone,
                    lease_start,
                    lease_end,
                ),
            )

            # Update the room status.
            connection.execute(
                """
                UPDATE rooms
                SET status = 'occupied'
                WHERE room_id = ?
                """,
                (room_id,),
            )

        return True, f"Tenant '{tenant_name}' added successfully!"

    except sqlite3.IntegrityError:
        return False, (
            "Could not add tenant. The room may already be assigned "
            "to another tenant."
        )

    except sqlite3.Error as error:
        return False, f"Database error: {error}"

def get_vacant_rooms():
    """Return all vacant rooms with their property names."""

    with get_connection() as connection:
        rooms = connection.execute(
            """
            SELECT
                r.room_id,
                r.room_number,
                r.monthly_rent,
                p.property_name
            FROM rooms AS r
            JOIN properties AS p
                ON r.property_id = p.property_id
            WHERE r.status = 'vacant'
            ORDER BY p.property_name, r.room_number
            """
        ).fetchall()

    return [dict(room) for room in rooms]

def get_all_tenants():
    """Return all registered tenants with their room and property details."""
    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT
                t.tenant_id,
                t.tenant_name,
                t.email,
                t.phone,
                t.lease_start,
                t.lease_end,
                r.room_number,
                r.monthly_rent,
                r.status AS room_status,
                p.property_name
            FROM tenants AS t
            JOIN rooms AS r
                ON t.room_id = r.room_id
            JOIN properties AS p
                ON r.property_id = p.property_id
            ORDER BY t.tenant_name
            """
        ).fetchall()

    return [dict(row) for row in rows]    