import os
import json
import re
from datetime import date
from dotenv import load_dotenv
from google import genai
from src.property_service import (
    get_dashboard_metrics,
    get_all_tenants,
)
from src.rent_service import (
    get_collection_summary,
    get_overdue_payments,
    get_vacant_rooms,
    get_tenant_payment_history,
    get_tenant_by_name,
)

load_dotenv()


def get_gemini_client():
    """Create a Gemini client using the API key from .env."""

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY is missing. "
            "Add it to your .env file."
        )

    return genai.Client(api_key=api_key)


def detect_reporting_month(question):
    """
    Detect a month such as October 2026 or 2026-10.
    Defaults to the current month when none is specified.
    """

    question_lower = question.lower()

    iso_match = re.search(
        r"\b(20\d{2})-(0[1-9]|1[0-2])\b",
        question_lower,
    )

    if iso_match:
        return f"{iso_match.group(1)}-{iso_match.group(2)}"

    month_names = {
        "january": "01",
        "february": "02",
        "march": "03",
        "april": "04",
        "may": "05",
        "june": "06",
        "july": "07",
        "august": "08",
        "september": "09",
        "october": "10",
        "november": "11",
        "december": "12",
    }

    for month_name, month_number in month_names.items():
        match = re.search(
            rf"\b{month_name}\s+(20\d{{2}})\b",
            question_lower,
        )

        if match:
            return f"{match.group(1)}-{month_number}"

    today = date.today()
    return today.strftime("%Y-%m")


def classify_question(question):
    """
    Select the relevant category using simple keyword matching.
    This avoids unnecessary database queries.
    """

    text = question.lower()

    categories = []

    if any(
        word in text
        for word in [
            "overdue",
            "late payment",
            "late payments",
            "past due",
            "who hasn't paid",
            "who has not paid",
        ]
    ):
        categories.append("overdue")

    if any(
        word in text
        for word in [
            "vacant",
            "available room",
            "available rooms",
            "empty room",
            "empty rooms",
        ]
    ):
        categories.append("vacant_rooms")

    if any(
        word in text
        for word in [
            "collection",
            "collected",
            "outstanding",
            "rent summary",
            "financial performance",
            "collection rate",
            "total rent",
        ]
    ):
        categories.append("rent_collection")

    if any(
        word in text
        for word in [
            "dashboard",
            "property performance",
            "overall performance",
            "how many properties",
            "occupancy",
        ]
    ):
        categories.append("dashboard")

    if not categories:
        categories = [
            "dashboard",
            "rent_collection",
            "overdue",
            "vacant_rooms",
        ]

    return categories


def get_property_context(question):
    """
    Retrieve verified information relevant to a question.
    All factual records come from the existing database services.
    """

    reporting_month = detect_reporting_month(question)
    categories = classify_question(question)

    context = {
        "reporting_month": reporting_month,
        "question_categories": categories,
    }

    if "dashboard" in categories:
        context["dashboard_metrics"] = get_dashboard_metrics()

    if "rent_collection" in categories:
        context["rent_collection"] = get_collection_summary(
            reporting_month
        )

    if "overdue" in categories:
        context["overdue_payments"] = get_overdue_payments()

    if "vacant_rooms" in categories:
        context["vacant_rooms"] = get_vacant_rooms()

    return context

def get_tenant_context(tenant_id):
    """Retrieve tenant details and payment history."""

    if not isinstance(tenant_id, int) or tenant_id <= 0:
        return {
            "error": "Please provide a valid positive tenant ID."
        }

    from database.db import get_connection

    # First, verify that the tenant exists.
    with get_connection() as connection:
        tenant_row = connection.execute(
            """
            SELECT tenant_id, tenant_name, is_active
            FROM tenants
            WHERE tenant_id = ?
            """,
            (tenant_id,),
        ).fetchone()

    if tenant_row is None:
        return {
            "tenant_id": tenant_id,
            "message": f"No tenant exists with ID {tenant_id}."
        }

    tenant = dict(tenant_row)

    # Retrieve the tenant's payment history.
    history = get_tenant_payment_history(tenant_id)

    total_due = sum(
        float(payment["amount_due"])
        for payment in history
    )

    total_paid = sum(
        float(payment["amount_paid"])
        for payment in history
    )

    total_outstanding = sum(
        max(
            0,
            float(payment["amount_due"])
            - float(payment["amount_paid"]),
        )
        for payment in history
    )

    return {
        "tenant_id": tenant["tenant_id"],
        "tenant_name": tenant["tenant_name"],
        "is_active": bool(tenant["is_active"]),
        "status": (
            "Active" if tenant["is_active"] else "Inactive"
        ),
        "payment_history": history,
        "total_due": round(total_due, 2),
        "total_paid": round(total_paid, 2),
        "total_outstanding": round(total_outstanding, 2),
        "message": (
            "Payment history retrieved successfully."
            if history
            else "This tenant exists but has no payment history."
        ),
    }

def get_direct_tenant_history_answer(tenant_id):
    """Answer tenant payment-history questions directly from SQLite."""

    from database.db import get_connection

    with get_connection() as connection:
        tenant_row = connection.execute(
            """
            SELECT tenant_id, tenant_name, is_active
            FROM tenants
            WHERE tenant_id = ?
            """,
            (tenant_id,),
        ).fetchone()

    if tenant_row is None:
        return f"No tenant exists with ID {tenant_id}."

    tenant = dict(tenant_row)
    history = get_tenant_payment_history(tenant_id)

    status = "Active" if tenant["is_active"] else "Inactive"

    lines = [
        f"### Payment History: {tenant['tenant_name']}",
        f"- Tenant ID: {tenant_id}",
        f"- Tenant status: {status}",
    ]

    if not history:
        lines.append("- No payment records were found for this tenant.")
        return "\n".join(lines)

    total_due = sum(float(p["amount_due"]) for p in history)
    total_paid = sum(float(p["amount_paid"]) for p in history)
    total_outstanding = sum(
        max(
            0.0,
            float(p["amount_due"]) - float(p["amount_paid"]),
        )
        for p in history
    )

    lines.extend([
        "",
        "| Rent Month | Amount Due | Amount Paid | Outstanding | Status |",
        "|---|---:|---:|---:|---|",
    ])

    for payment in history:
        due = float(payment["amount_due"])
        paid = float(payment["amount_paid"])
        outstanding = max(0.0, due - paid)

        lines.append(
            f"| {payment['rent_month']} "
            f"| ₹{due:,.2f} "
            f"| ₹{paid:,.2f} "
            f"| ₹{outstanding:,.2f} "
            f"| {payment['status']} |"
        )

    lines.extend([
        "",
        f"**Total rent due:** ₹{total_due:,.2f}",
        f"**Total rent paid:** ₹{total_paid:,.2f}",
        f"**Total outstanding:** ₹{total_outstanding:,.2f}",
    ])

    return "\n".join(lines)

def find_tenant_context(tenant_name):
    """Retrieve tenant details and payment history."""

    tenants = get_tenant_by_name(tenant_name)

    if not tenants:
        return {
            "message": f"No tenant found matching '{tenant_name}'."
        }

    results = []

    for tenant in tenants:
        history = get_tenant_payment_history(
            tenant["tenant_id"]
        )

        outstanding = sum(
            max(
                0,
                float(payment["amount_due"])
                - float(payment["amount_paid"]),
            )
            for payment in history
        )

        results.append({
            "tenant": tenant,
            "payment_history": history,
            "total_outstanding": round(outstanding, 2),
        })

    return {"matches": results}

def get_direct_property_answer(question):
    """Answer basic property and room questions directly from SQLite."""

    from database.db import get_connection

    text = question.lower().strip()

    with get_connection() as connection:

        # Property count
        if any(phrase in text for phrase in [
            "how many properties",
            "number of properties",
            "total properties",
            "count properties",
        ]):
            count = connection.execute(
                "SELECT COUNT(*) FROM properties"
            ).fetchone()[0]

            return f"**Total properties:** {count}"

        # Total, occupied, and vacant rooms
        if any(phrase in text for phrase in [
            "room occupancy",
            "occupancy rate",
            "how many rooms",
            "room count",
            "occupied and vacant",
            "occupied rooms",
            "vacant rooms",
            "how many occupied",
            "how many vacant",
        ]):

            row = connection.execute(
                """
                SELECT
                    COUNT(*) AS total_rooms,
                    COALESCE(
                        SUM(CASE WHEN status = 'occupied'
                            THEN 1 ELSE 0 END), 0
                    ) AS occupied_rooms,
                    COALESCE(
                        SUM(CASE WHEN status = 'vacant'
                            THEN 1 ELSE 0 END), 0
                    ) AS vacant_rooms
                FROM rooms
                """
            ).fetchone()

            total = row["total_rooms"]
            occupied = row["occupied_rooms"]
            vacant = row["vacant_rooms"]

            occupancy = (
                occupied / total * 100 if total else 0
            )

            return (
                "### Room Occupancy Summary\n\n"
                f"- **Total Rooms:** {total}\n"
                f"- **Occupied Rooms:** {occupied}\n"
                f"- **Vacant Rooms:** {vacant}\n"
                f"- **Occupancy Rate:** {occupancy:.1f}%"
            )

        # List properties
        if any(phrase in text for phrase in [
            "list properties",
            "show properties",
            "all properties",
            "property names",
        ]):
            rows = connection.execute(
                """
                SELECT
                    p.property_name,
                    p.city,
                    COUNT(r.room_id) AS total_rooms,
                    COALESCE(
                        SUM(CASE WHEN r.status = 'occupied'
                            THEN 1 ELSE 0 END), 0
                    ) AS occupied_rooms,
                    COALESCE(
                        SUM(CASE WHEN r.status = 'vacant'
                            THEN 1 ELSE 0 END), 0
                    ) AS vacant_rooms
                FROM properties p
                LEFT JOIN rooms r
                    ON p.property_id = r.property_id
                GROUP BY p.property_id, p.property_name, p.city
                ORDER BY p.property_name
                """
            ).fetchall()

            if not rows:
                return "No properties are currently registered."

            lines = ["### Property Overview", ""]

            for row in rows:
                lines.append(
                    f"- **{row['property_name']}** ({row['city']})"
                    f" — Total rooms: {row['total_rooms']},"
                    f" Occupied: {row['occupied_rooms']},"
                    f" Vacant: {row['vacant_rooms']}"
                )

            return "\n".join(lines)

    return None

def ask_tenantease_ai(question):
    """Answer property-management questions using database context."""

    if not question or not question.strip():
        return "Please enter a question."

    normalized_question = question.lower().strip()
    
    # Answer basic property and room questions directly from SQLite.
    try:
        direct_answer = get_direct_property_answer(
            normalized_question
        )

        if direct_answer is not None:
            return direct_answer

    except Exception as error:
        print(f"Direct property answer error: {error}")

    # Handle tenant-list questions directly from the database.
    tenant_list_phrases = [
        "list all tenants",
        "give me the names of the tenants",
        "give me tenant names",
        "show all tenants",
        "show me all tenants",
        "who are the tenants",
        "names of all tenants",
        "list registered tenants",
    ]

    if any(
        phrase in normalized_question
        for phrase in tenant_list_phrases
    ):
        try:
            return get_tenant_list_answer()
        except Exception as error:
            print(f"Tenant list error: {error}")
            return "Unable to retrieve tenant records from the database."
        
    # Answer tenant payment-history questions directly from SQLite.
    history_question = any(
        phrase in normalized_question
        for phrase in [
            "payment history",
            "payment details",
            "rent history",
            "rent details",
        ]
    )

    tenant_match = re.search(
        r"\btenant\s*(?:id)?\s*#?\s*(\d+)\b",
        question,
        re.IGNORECASE,
    )

    if history_question and tenant_match:
        tenant_id = int(tenant_match.group(1))
        return get_direct_tenant_history_answer(tenant_id)
    
    try:
        # Build the property context before adding tenant information.
        context = get_property_context(question)

        # Add tenant payment history when a tenant ID is supplied.
        tenant_match = re.search(
            r"\btenant\s*(?:id)?\s*#?\s*(\d+)\b",
            question,
            re.IGNORECASE,
        )

        if tenant_match:
            tenant_id = int(tenant_match.group(1))
            context["tenant_details"] = get_tenant_context(tenant_id)

        # Add tenant details when the question contains a tenant name.
        tenant_name = extract_tenant_name(question)

        if tenant_name:
            context["tenant_details"] = find_tenant_context(
                tenant_name
            )

        # Check whether Gemini is configured.
        model_name = os.getenv("GEMINI_MODEL")

        if not model_name:
            return (
                "GEMINI_MODEL is missing from your .env file. "
                "Set it to a model available to your API key."
            )

        client = get_gemini_client()

        prompt = f"""
You are TenantEase AI, a property-management assistant.

Answer the user's question using the supplied database context.

RULES:
1. Use database records as the source of truth.
2. Never invent tenant names, property details, or financial amounts.
3. Clearly state when information is unavailable.
4. Use Indian rupees (₹) for financial figures.
5. Explain calculations when useful.
6. Distinguish paid, partially paid, and unpaid rent.
7. Do not claim to have sent reminders or completed payments.
8. Never reveal API keys or secrets.
9. The database contains fictional demonstration data.
10. An empty result is not automatically an error.
11. If the question is unrelated to the supplied data, explain
    what property-management questions you can answer.

VERIFIED DATABASE CONTEXT:
{json.dumps(context, indent=2, default=str)}

USER QUESTION:
{question}
"""

        response = client.models.generate_content(
            model=model_name,
            contents=prompt,
        )

        if response.text:
            return response.text

        return "The AI returned an empty response. Please try again."

    except Exception as error:
        import traceback

        print("\n========== TENANTEASE AI ERROR ==========")
        print(f"Error type: {type(error).__name__}")
        print(f"Error message: {error}")
        traceback.print_exc()
        print("=========================================\n")

        error_text = str(error).lower()

        if (
            "503" in error_text
            or "unavailable" in error_text
        ):
            return (
                "⚠️ **Gemini is temporarily unavailable.**\n\n"
                "Your database is still available, but this "
                "question requires the AI service.\n\n"
                "Please try again in a few minutes, or ask a "
                "direct question such as:\n"
                "- How many properties do I have?\n"
                "- How many rooms are occupied and vacant?\n"
                "- List all properties."
            )

        return (
            f"⚠️ **AI Assistant error:** "
            f"{type(error).__name__}: {error}\n\n"
            "Please check the terminal for additional details."
        )
        
def generate_rent_reminder(payment_details):
    """
    Generate a rent reminder draft for manager review.
    This function does not send messages.
    """

    if not payment_details:
        return "No outstanding payments were found for this tenant."

    try:
        client = get_gemini_client()

        model_name = os.getenv("GEMINI_MODEL")

        if not model_name:
            return "GEMINI_MODEL is missing from your .env file."

        prompt = f"""
Draft a polite, professional rent reminder.

Use only the following verified payment information:
{json.dumps(payment_details, indent=2, default=str)}

Requirements:
- Mention the tenant by name if provided.
- Mention the outstanding amount in Indian rupees.
- Mention the rent month and due date if available.
- Be respectful and professional.
- Do not invent fees, penalties, or legal consequences.
- Do not claim payment has been received.
- Include a subject line and message body.
- The property manager must review the draft.
- Do not send the message.
"""

        response = client.models.generate_content(
            model=model_name,
            contents=prompt,
        )

        return response.text or "Gemini returned an empty response."

    except Exception as error:
        print(f"Reminder generation error: {error}")

        return (
            "Unable to generate the reminder. "
            "Check the application logs."
        )

def extract_tenant_name(question):
    """Extract a tenant name from common question formats."""

    patterns = [
        r"(?:payment history|payment details)\s+for\s+(.+)",
        r"(?:find|search for)\s+tenant\s+(.+)",
        r"(?:details|contact details)\s+for\s+tenant\s+(.+)",
        r"(?:show|find)\s+tenant\s+(.+)",
    ]

    for pattern in patterns:
        match = re.search(
            pattern,
            question.strip(),
            re.IGNORECASE,
        )

        if match:
            name = match.group(1).strip()

            # Remove common trailing question words and punctuation.
            name = re.sub(
                r"\s+(?:please|thanks)$",
                "",
                name,
                flags=re.IGNORECASE,
            )

            return name.rstrip("?.! ")

    return None    

def generate_tenant_rent_reminder(tenant_id):
    """
    Generate a rent reminder from verified tenant payment records.
    Does not send an email or message.
    """

    if not isinstance(tenant_id, int) or tenant_id <= 0:
        return "Please provide a valid tenant ID."

    tenants = get_tenant_by_name("")

    # Retrieve the tenant directly by ID.
    from database.db import get_connection

    with get_connection() as connection:
        row = connection.execute(
            """
            SELECT
                t.tenant_id,
                t.tenant_name,
                t.email,
                t.phone,
                p.property_name,
                r.room_number
            FROM tenants t
            JOIN rooms r ON t.room_id = r.room_id
            JOIN properties p ON r.property_id = p.property_id
            WHERE t.tenant_id = ?
            """,
            (tenant_id,),
        ).fetchone()

    if not row:
        return f"No tenant found with ID {tenant_id}."

    tenant = dict(row)

    history = get_tenant_payment_history(tenant_id)

    outstanding_payments = [
        payment
        for payment in history
        if float(payment["amount_due"])
        > float(payment["amount_paid"])
    ]

    if not outstanding_payments:
        return "No outstanding payments were found for this tenant."

    payment_details = {
        "tenant_id": tenant["tenant_id"],
        "tenant_name": tenant["tenant_name"],
        "property_name": tenant["property_name"],
        "room_number": tenant["room_number"],
        "outstanding_payments": outstanding_payments,
    }

    return generate_rent_reminder(payment_details)

def get_tenant_list_answer():
    """Create an accurate tenant list directly from database records."""

    tenants = get_all_tenants()

    if not tenants:
        return "No tenants are currently registered in the database."

    lines = ["### Registered Tenants", ""]

    for tenant in tenants:
        lines.append(
            f"- **{tenant['tenant_name']}** — "
            f"{tenant['property_name']}, "
            f"Room {tenant['room_number']}"
        )

    lines.append("")
    lines.append(f"**Total registered tenants: {len(tenants)}**")

    return "\n".join(lines)