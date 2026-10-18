from database.db import get_connection

with get_connection() as connection:
    rows = connection.execute(
        """
        SELECT
            r.room_number,
            r.status,
            t.tenant_name
        FROM rooms AS r
        LEFT JOIN tenants AS t
            ON r.room_id = t.room_id
        WHERE r.room_number IN ('103', '203')
        ORDER BY r.room_number
        """
    ).fetchall()

    for row in rows:
        print(dict(row))