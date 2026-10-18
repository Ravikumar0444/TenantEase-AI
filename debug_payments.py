from database.db import get_connection

with get_connection() as connection:
    rows = connection.execute("""
        SELECT
            t.tenant_name,
            p.rent_month,
            p.amount_due,
            p.amount_paid,
            p.due_date,
            p.status
        FROM payments p
        JOIN tenants t ON p.tenant_id = t.tenant_id
        WHERE t.tenant_name = 'Amit Kumar'
    """).fetchall()

    for row in rows:
        print(dict(row))


from datetime import date
from src.rent_service import get_overdue_payments

print("\nOverdue payments as of 2026-10-19:")

for payment in get_overdue_payments(as_of=date(2026, 10, 19)):
    print(
        payment["tenant_name"],
        "| Due:", payment["amount_due"],
        "| Paid:", payment["amount_paid"],
        "| Outstanding:", payment["outstanding_amount"]
    )        
