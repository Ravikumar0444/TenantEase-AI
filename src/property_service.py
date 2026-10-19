from database.db import get_connection
import sqlite3

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

        # Active tenants
        total_active_tenants = connection.execute(
            """
            SELECT COUNT(*)
            FROM tenants
            WHERE is_active = 1
            """
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

        # Rent collected for October 2026
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
        "total_active_tenants": total_active_tenants,
        "total_rooms": total_rooms,
        "occupied_rooms": occupied_rooms,
        "vacant_rooms": vacant_rooms,
        "expected_rent": expected_rent,
        "rent_collected": rent_collected,
        "outstanding_rent": outstanding_rent,
    }

def get_tenant_payment_records():
    """Return October 2026 outstanding payment records for active tenants."""

    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT
                t.tenant_id,
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
              AND t.is_active = 1
              AND p.amount_due > p.amount_paid
            ORDER BY p.due_date ASC
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
    Add a tenant to a vacant room and create the initial rent payment.
    """

    from datetime import date

    tenant_name = tenant_name.strip()
    email = email.strip() or None
    phone = phone.strip() or None

    # Validate tenant name.
    if not tenant_name:
        return False, "Tenant name is required."

    # Validate lease dates.
    try:
        start_date = (
            date.fromisoformat(str(lease_start))
            if lease_start
            else None
        )

        end_date = (
            date.fromisoformat(str(lease_end))
            if lease_end
            else None
        )

    except (ValueError, TypeError):
        return False, "Invalid lease date. Please use YYYY-MM-DD format."

    if start_date and end_date and end_date < start_date:
        return False, "Lease end date cannot be before lease start date."

    try:
        with get_connection() as connection:

            # Check whether the selected room exists.
            room = connection.execute(
                """
                SELECT room_id, status, monthly_rent
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

            # Add the tenant.
            cursor = connection.execute(
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
                    start_date.isoformat() if start_date else None,
                    end_date.isoformat() if end_date else None,
                ),
            )

            tenant_id = cursor.lastrowid

            # Mark the room as occupied.
            connection.execute(
                """
                UPDATE rooms
                SET status = 'occupied'
                WHERE room_id = ?
                """,
                (room_id,),
            )

            # Create the initial rent payment for the lease start month.
            if start_date:
                rent_month = start_date.strftime("%Y-%m")
                monthly_rent = float(room["monthly_rent"])

                connection.execute(
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
                    VALUES (?, ?, ?, 0, ?, NULL, 'pending')
                    """,
                    (
                        tenant_id,
                        rent_month,
                        monthly_rent,
                        start_date.isoformat(),
                    ),
                )

        return True, (
            f"Tenant '{tenant_name}' added successfully, "
            "and the initial rent payment record was created."
            if start_date
            else f"Tenant '{tenant_name}' added successfully. "
                 "No rent payment was created because the lease start date is missing."
        )

    except sqlite3.IntegrityError as error:
        return False, f"Could not add tenant: {error}"

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

def get_all_tenants(include_inactive=False):
    """Return tenant records, optionally including inactive tenants."""

    query = """
        SELECT
            t.tenant_id,
            t.tenant_name,
            t.email,
            t.phone,
            t.lease_start,
            t.lease_end,
            t.is_active,
            t.room_id,
            r.room_number,
            r.monthly_rent,
            r.status AS room_status,
            p.property_name
        FROM tenants AS t
        JOIN rooms AS r
            ON t.room_id = r.room_id
        JOIN properties AS p
            ON r.property_id = p.property_id
    """

    if not include_inactive:
        query += " WHERE t.is_active = 1"

    query += " ORDER BY t.tenant_name"

    with get_connection() as connection:
        rows = connection.execute(query).fetchall()

    return [dict(row) for row in rows]

def delete_tenant(tenant_id):
    """
    Remove a tenant only when no payment records reference them.
    Preserve financial history and release the room when possible.
    """

    with get_connection() as connection:
        tenant = connection.execute(
            """
            SELECT tenant_id, tenant_name, room_id
            FROM tenants
            WHERE tenant_id = ?
            """,
            (tenant_id,),
        ).fetchone()

        if tenant is None:
            return False, "Tenant not found."

        payments = connection.execute(
            """
            SELECT
                COUNT(*) AS payment_count,
                COALESCE(SUM(amount_due - amount_paid), 0)
                    AS total_outstanding
            FROM payments
            WHERE tenant_id = ?
            """,
            (tenant_id,),
        ).fetchone()

        if payments["total_outstanding"] > 0:
            return (
                False,
                "This tenant has outstanding rent. "
                "Please settle the balance before deletion.",
            )

        if payments["payment_count"] > 0:
            return (
                False,
                "This tenant has payment history and cannot be "
                "permanently deleted. Use tenant deactivation "
                "to preserve financial records.",
            )

        connection.execute(
            """
            DELETE FROM tenants
            WHERE tenant_id = ?
            """,
            (tenant_id,),
        )

        connection.execute(
            """
            UPDATE rooms
            SET status = 'vacant'
            WHERE room_id = ?
            """,
            (tenant["room_id"],),
        )

    return True, f"Tenant '{tenant['tenant_name']}' deleted successfully."

def deactivate_tenant(tenant_id):
    """Deactivate a tenant while preserving their payment history."""

    with get_connection() as connection:
        tenant = connection.execute(
            """
            SELECT tenant_id, tenant_name, room_id, is_active
            FROM tenants
            WHERE tenant_id = ?
            """,
            (tenant_id,),
        ).fetchone()

        if tenant is None:
            return False, "Tenant not found."

        if tenant["is_active"] == 0:
            return False, "This tenant is already inactive."

        payments = connection.execute(
            """
            SELECT
                COALESCE(SUM(amount_due - amount_paid), 0)
                    AS total_outstanding
            FROM payments
            WHERE tenant_id = ?
            """,
            (tenant_id,),
        ).fetchone()

        if payments["total_outstanding"] > 0:
            return (
                False,
                "This tenant has outstanding rent. "
                "Please settle the balance before deactivation.",
            )

        connection.execute(
            """
            UPDATE tenants
            SET is_active = 0
            WHERE tenant_id = ?
            """,
            (tenant_id,),
        )

        connection.execute(
            """
            UPDATE rooms
            SET status = 'vacant'
            WHERE room_id = ?
            """,
            (tenant["room_id"],),
        )

    return True, (
        f"Tenant '{tenant['tenant_name']}' deactivated successfully. "
        "Payment history has been preserved."
    )

def get_all_properties():
    """Return all properties from the database."""
    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT
                property_id,
                property_name,
                address,
                city,
                property_type
            FROM properties
            ORDER BY property_name
            """
        ).fetchall()

    return [dict(row) for row in rows]


def add_property(property_name, address, city, property_type="Residential"):
    """Add a new property to the database."""
    property_name = property_name.strip()
    address = address.strip()
    city = city.strip()
    property_type = property_type.strip()

    if not property_name or not address or not city:
        return False, "Property name, address, and city are required."

    try:
        with get_connection() as connection:
            connection.execute(
                """
                INSERT INTO properties (
                    property_name,
                    address,
                    city,
                    property_type
                )
                VALUES (?, ?, ?, ?)
                """,
                (property_name, address, city, property_type),
            )

        return True, f"Property '{property_name}' added successfully."

    except sqlite3.Error as error:
        return False, f"Could not add property: {error}"


def update_property(
    property_id,
    property_name,
    address,
    city,
    property_type="Residential",
):
    """Update an existing property's details."""
    property_name = property_name.strip()
    address = address.strip()
    city = city.strip()
    property_type = property_type.strip()

    if not property_name or not address or not city:
        return False, "Property name, address, and city are required."

    try:
        with get_connection() as connection:
            cursor = connection.execute(
                """
                UPDATE properties
                SET property_name = ?,
                    address = ?,
                    city = ?,
                    property_type = ?
                WHERE property_id = ?
                """,
                (
                    property_name,
                    address,
                    city,
                    property_type,
                    property_id,
                ),
            )

            if cursor.rowcount == 0:
                return False, "Property not found."

        return True, f"Property '{property_name}' updated successfully."

    except sqlite3.Error as error:
        return False, f"Could not update property: {error}"


def delete_property(property_id):
    """
    Delete a property only when it has no associated rooms.
    Properties with rooms must be handled safely first.
    """
    try:
        with get_connection() as connection:
            property_row = connection.execute(
                """
                SELECT property_id, property_name
                FROM properties
                WHERE property_id = ?
                """,
                (property_id,),
            ).fetchone()

            if property_row is None:
                return False, "Property not found."

            room_count = connection.execute(
                """
                SELECT COUNT(*)
                FROM rooms
                WHERE property_id = ?
                """,
                (property_id,),
            ).fetchone()[0]

            if room_count > 0:
                return (
                    False,
                    f"Cannot delete '{property_row['property_name']}' "
                    f"because it has {room_count} associated room(s). "
                    "Preserve its records and remove or archive the "
                    "property only through a safe workflow.",
                )

            connection.execute(
                """
                DELETE FROM properties
                WHERE property_id = ?
                """,
                (property_id,),
            )

        return (
            True,
            f"Property '{property_row['property_name']}' deleted successfully.",
        )

    except sqlite3.Error as error:
        return False, f"Could not delete property: {error}"

def get_property_room_summary(property_id):
    """Return total, occupied, and vacant room counts for a property."""
    with get_connection() as connection:
        row = connection.execute(
            """
            SELECT
                COUNT(*) AS total_rooms,
                SUM(CASE WHEN status = 'occupied' THEN 1 ELSE 0 END)
                    AS occupied_rooms,
                SUM(CASE WHEN status = 'vacant' THEN 1 ELSE 0 END)
                    AS vacant_rooms
            FROM rooms
            WHERE property_id = ?
            """,
            (property_id,),
        ).fetchone()

    total = row["total_rooms"] or 0
    occupied = row["occupied_rooms"] or 0
    vacant = row["vacant_rooms"] or 0

    occupancy_rate = (occupied / total * 100) if total else 0

    return {
        "total_rooms": total,
        "occupied_rooms": occupied,
        "vacant_rooms": vacant,
        "occupancy_rate": round(occupancy_rate, 1),
    }    

def add_room(property_id, room_number, monthly_rent):
    """Add a vacant room to an existing property."""

    room_number = str(room_number).strip()

    if not room_number:
        return False, "Room number is required."

    try:
        monthly_rent = float(monthly_rent)

        if monthly_rent <= 0:
            return False, "Monthly rent must be greater than zero."

    except (TypeError, ValueError):
        return False, "Please enter a valid monthly rent."

    try:
        with get_connection() as connection:

            # Verify that the property exists.
            property_row = connection.execute(
                "SELECT property_name FROM properties WHERE property_id = ?",
                (property_id,)
            ).fetchone()

            if property_row is None:
                return False, "Selected property does not exist."

            # Insert the room as vacant.
            connection.execute(
                """
                INSERT INTO rooms (
                    property_id,
                    room_number,
                    monthly_rent,
                    status
                )
                VALUES (?, ?, ?, 'vacant')
                """,
                (property_id, room_number, monthly_rent)
            )

        return True, f"Room {room_number} added successfully!"

    except sqlite3.IntegrityError:
        return False, (
            f"Room {room_number} already exists in this property."
        )

    except sqlite3.Error as error:
        return False, f"Database error: {error}"