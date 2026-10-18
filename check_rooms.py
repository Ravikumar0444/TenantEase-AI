from database.db import get_connection

with get_connection() as connection:
    rooms = connection.execute(
        """
        SELECT room_number, status
        FROM rooms
        ORDER BY room_number
        """
    ).fetchall()

    for room in rooms:
        print(dict(room))