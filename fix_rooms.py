from database.db import get_connection


def fix_vacant_rooms():
    with get_connection() as connection:
        # Find rooms that have no tenant assigned.
        rooms = connection.execute(
            """
            SELECT room_id, room_number
            FROM rooms
            WHERE NOT EXISTS (
                SELECT 1
                FROM tenants
                WHERE tenants.room_id = rooms.room_id
            )
            """
        ).fetchall()

        # Mark only unassigned rooms as vacant.
        connection.execute(
            """
            UPDATE rooms
            SET status = 'vacant'
            WHERE NOT EXISTS (
                SELECT 1
                FROM tenants
                WHERE tenants.room_id = rooms.room_id
            )
            """
        )

        print("Rooms marked as vacant:")
        for room in rooms:
            print(dict(room))

        # Display all room statuses.
        updated_rooms = connection.execute(
            """
            SELECT room_id, room_number, status
            FROM rooms
            ORDER BY room_id
            """
        ).fetchall()

        print("\nCurrent room statuses:")
        for room in updated_rooms:
            print(dict(room))


if __name__ == "__main__":
    fix_vacant_rooms()