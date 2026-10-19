from database.db import get_connection

with get_connection() as connection:
    rows = connection.execute(
        """
        SELECT
            tenant_id,
            tenant_name,
            is_active
        FROM tenants
        ORDER BY tenant_id
        """
    ).fetchall()

    print("\nTENANTS IN DATABASE")
    print("-" * 50)

    for row in rows:
        print(
            f"ID: {row['tenant_id']} | "
            f"Name: {row['tenant_name']} | "
            f"Active: {row['is_active']}"
        )