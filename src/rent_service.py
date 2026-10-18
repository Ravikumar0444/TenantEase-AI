from datetime import date, timedelta

from database.db import get_connection


def get_outstanding_rent(rent_month=None):
    """
    Calculate unpaid rent for a particular month.

    Outstanding rent = Amount due - Amount paid.
    """

    with get_connection() as connection:

        if rent_month:
            query = """
                SELECT
                    COALESCE(SUM(amount_due - amount_paid), 0)
                    AS outstanding_rent
                FROM payments
                WHERE rent_month = ?
            """

            result = connection.execute(
                query, (rent_month,)
            ).fetchone()

        else:
            query = """
                SELECT
                    COALESCE(SUM(amount_due - amount_paid), 0)
                    AS outstanding_rent
                FROM payments
                WHERE amount_paid < amount_due
            """

            result = connection.execute(query).fetchone()

    return float(result["outstanding_rent"])


def get_overdue_payments(as_of=None):
    if as_of is None:
        as_of = date.today()

    as_of = as_of.isoformat()

    query = """
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
        WHERE p.due_date < ?
          AND p.amount_paid < p.amount_due
        ORDER BY p.due_date ASC
    """

    with get_connection() as connection:
        rows = connection.execute(query, (as_of,)).fetchall()

    return [dict(row) for row in rows]

def get_upcoming_payments(days=7, as_of=None):
    """
    Find unpaid balances due between today and the next
    specified number of days, inclusive.
    """

    if days < 0:
        raise ValueError("days cannot be negative")

    if as_of is None:
        as_of = date.today()

    start_date = as_of.isoformat()
    end_date = (as_of + timedelta(days=days)).isoformat()

    with get_connection() as connection:

        rows = connection.execute(
            """
            SELECT
                t.tenant_name,
                p.property_name,
                r.room_number,
                pay.rent_month,
                pay.amount_due,
                pay.amount_paid,
                (pay.amount_due - pay.amount_paid)
                    AS outstanding_amount,
                pay.due_date
            FROM payments pay
            JOIN tenants t
                ON pay.tenant_id = t.tenant_id
            JOIN rooms r
                ON t.room_id = r.room_id
            JOIN properties p
                ON r.property_id = p.property_id
            WHERE pay.due_date BETWEEN ? AND ?
              AND pay.amount_paid < pay.amount_due
            ORDER BY pay.due_date ASC
            """,
            (start_date, end_date),
        ).fetchall()

    return [dict(row) for row in rows]


def get_collection_summary(rent_month):
    """
    Summarise rent due, rent collected, outstanding rent,
    and collection percentage for a particular month.
    """

    with get_connection() as connection:

        result = connection.execute(
            """
            SELECT
                COALESCE(SUM(amount_due), 0) AS total_due,
                COALESCE(SUM(amount_paid), 0) AS total_paid,
                COALESCE(
                    SUM(amount_due - amount_paid), 0
                ) AS outstanding
            FROM payments
            WHERE rent_month = ?
            """,
            (rent_month,),
        ).fetchone()

    total_due = float(result["total_due"])
    total_paid = float(result["total_paid"])
    outstanding = float(result["outstanding"])

    collection_rate = (
        total_paid / total_due * 100
        if total_due > 0
        else 0.0
    )

    return {
        "rent_month": rent_month,
        "total_due": total_due,
        "total_paid": total_paid,
        "outstanding": outstanding,
        "collection_rate": round(collection_rate, 2),
    }


def get_tenant_payment_history(tenant_id):
    """
    Retrieve the payment history for one tenant.
    """

    with get_connection() as connection:

        rows = connection.execute(
            """
            SELECT
                rent_month,
                amount_due,
                amount_paid,
                (amount_due - amount_paid)
                    AS outstanding_amount,
                due_date,
                payment_date,
                status
            FROM payments
            WHERE tenant_id = ?
            ORDER BY rent_month DESC
            """,
            (tenant_id,),
        ).fetchall()

    return [dict(row) for row in rows]


def get_vacant_rooms():
    """
    Return all vacant rooms and their property details.
    """

    with get_connection() as connection:

        rows = connection.execute(
            """
            SELECT
                p.property_name,
                p.city,
                r.room_number,
                r.monthly_rent
            FROM rooms r
            JOIN properties p
                ON r.property_id = p.property_id
            WHERE r.status = 'vacant'
            ORDER BY p.property_name, r.room_number
            """
        ).fetchall()

    return [dict(row) for row in rows]