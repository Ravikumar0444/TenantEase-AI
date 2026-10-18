from src.reminder_service import (
    get_tenants_needing_reminders,
    generate_reminder_details,
)


def test_reminder_records_have_outstanding_balances():
    records = get_tenants_needing_reminders()

    for record in records:
        assert record["amount_paid"] < record["amount_due"]


def test_reminder_records_contain_required_fields():
    records = get_tenants_needing_reminders()

    if records:
        required_fields = {
            "tenant_id",
            "tenant_name",
            "rent_month",
            "amount_due",
            "amount_paid",
            "outstanding_amount",
            "due_date",
        }

        assert required_fields.issubset(records[0].keys())


def test_generate_reminder_details_for_existing_tenant():
    records = get_tenants_needing_reminders()

    if records:
        tenant_id = records[0]["tenant_id"]

        details = generate_reminder_details(tenant_id)

        assert len(details) > 0

        for payment in details:
            assert payment["tenant_id"] if "tenant_id" in payment else True
            assert payment["amount_paid"] < payment["amount_due"]