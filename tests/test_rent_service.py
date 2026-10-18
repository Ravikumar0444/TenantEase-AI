from datetime import date

from src.rent_service import (
    get_outstanding_rent,
    get_overdue_payments,
    get_collection_summary,
    get_vacant_rooms,
)


def test_october_outstanding_rent():
    """
    The October sample payments have:
    Total due = 82,000
    Total paid = 34,000
    Outstanding = 48,000
    """

    result = get_outstanding_rent("2026-10")

    assert result == 48000


def test_october_collection_summary():

    result = get_collection_summary("2026-10")

    assert result["total_due"] == 82000
    assert result["total_paid"] == 34000
    assert result["outstanding"] == 48000

    assert result["collection_rate"] == round(
        34000 / 82000 * 100, 2
    )


def test_overdue_payments_as_of_october_19():
    from datetime import date

    result = get_overdue_payments(
        as_of=date(2026, 10, 19)
    )

    tenant_names = {
        payment["tenant_name"]
        for payment in result
    }

    # Priya has an outstanding balance after the due date.
    assert "Priya Verma" in tenant_names

    # Amit has an unpaid October payment in the actual database.
    assert "Amit Kumar" in tenant_names

    # Every returned record must have an outstanding balance.
    for payment in result:
        assert payment["amount_paid"] < payment["amount_due"]
        assert payment["due_date"] < "2026-10-19"

def test_vacant_rooms():

    result = get_vacant_rooms()

    assert len(result) == 2

    room_numbers = {
        room["room_number"]
        for room in result
    }

    assert room_numbers == {"103", "203"}