from database.db import get_connection
from datetime import date

def get_tenants_needing_reminders(as_of=None):
    """
    Return active tenants with outstanding rent,
    including payments that are not overdue yet.
    """

    query = """
        SELECT
            t.tenant_id,
            t.tenant_name,
            t.email,
            p.rent_month,
            p.amount_due,
            p.amount_paid,
            (p.amount_due - p.amount_paid) AS outstanding_amount,
            p.due_date,
            p.status,
            pr.property_name,
            r.room_number
        FROM payments p
        JOIN tenants t
            ON p.tenant_id = t.tenant_id
        JOIN rooms r
            ON t.room_id = r.room_id
        JOIN properties pr
            ON r.property_id = pr.property_id
        WHERE t.is_active = 1
          AND p.amount_due > p.amount_paid
        ORDER BY p.due_date ASC
    """

    with get_connection() as connection:
        rows = connection.execute(query).fetchall()

    return [dict(row) for row in rows]

def generate_reminder_details(tenant_id):
    """
    Retrieve the outstanding payment details for one tenant.
    """

    query = """
        SELECT
            t.tenant_name,
            t.email,
            p.rent_month,
            p.amount_due,
            p.amount_paid,
            (p.amount_due - p.amount_paid) AS outstanding_amount,
            p.due_date,
            pr.property_name,
            r.room_number
        FROM payments p
        JOIN tenants t
            ON p.tenant_id = t.tenant_id
        JOIN rooms r
            ON t.room_id = r.room_id
        JOIN properties pr
            ON r.property_id = pr.property_id
        WHERE t.tenant_id = ?
          AND p.amount_paid < p.amount_due
        ORDER BY p.due_date ASC
    """

    with get_connection() as connection:
        rows = connection.execute(query, (tenant_id,)).fetchall()

    return [dict(row) for row in rows]