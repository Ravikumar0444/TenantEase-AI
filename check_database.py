from database.db import get_connection

with get_connection() as connection:

    tables = [
        "properties",
        "rooms",
        "tenants",
        "payments",
    ]

    for table in tables:
        result = connection.execute(
            f"SELECT COUNT(*) FROM {table}"
        ).fetchone()[0]

        print(f"{table}: {result} records")

    print("\nOctober 2026 payments:")

    results = connection.execute(
        """
        SELECT
            t.tenant_name,
            p.amount_due,
            p.amount_paid,
            p.status
        FROM payments p
        JOIN tenants t
            ON p.tenant_id = t.tenant_id
        WHERE p.rent_month = ?
        ORDER BY t.tenant_name
        """,
        ("2026-10",),
    ).fetchall()

    for row in results:
        print(
            f"{row['tenant_name']}: "
            f"Due ₹{row['amount_due']:.0f}, "
            f"Paid ₹{row['amount_paid']:.0f}, "
            f"Status: {row['status']}"
        )