import os
import json

from dotenv import load_dotenv
from google import genai

from src.property_service import get_dashboard_metrics
from src.rent_service import (
    get_collection_summary,
    get_overdue_payments,
    get_vacant_rooms,
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


def get_property_context():
    """Retrieve verified information from our SQLite database."""

    metrics = get_dashboard_metrics()

    collection = get_collection_summary("2026-10")

    overdue_payments = get_overdue_payments()

    vacant_rooms = get_vacant_rooms()

    context = {
        "reporting_month": "October 2026",
        "dashboard_metrics": metrics,
        "rent_collection": collection,
        "overdue_payments": overdue_payments,
        "vacant_rooms": vacant_rooms,
    }

    return context


def ask_tenantease_ai(question):
    """Answer a property-management question using database context."""

    if not question or not question.strip():
        return "Please enter a question."

    try:
        client = get_gemini_client()

        context = get_property_context()

        prompt = f"""
You are TenantEase AI Assistant, a helpful property-management assistant.

Your job is to answer questions about rental properties, tenants,
rent collection, outstanding balances, overdue payments, and vacant rooms.

IMPORTANT RULES:
1. Use only the supplied database context for factual answers.
2. Never invent tenant names, payment amounts, or property details.
3. If the context does not contain the requested information, say so.
4. Clearly distinguish paid, partially paid, and unpaid rent.
5. Use Indian rupees (₹) for financial amounts.
6. The supplied financial report is for October 2026.
7. The sample data is fictional and intended for demonstration.
8. Do not claim that you have sent messages, reminders, or payments.
9. Be concise, professional, and helpful.

VERIFIED DATABASE CONTEXT:
{json.dumps(context, indent=2, default=str)}

USER QUESTION:
{question}
"""

        model_name = os.getenv("GEMINI_MODEL")

        if not model_name:
            return (
                "GEMINI_MODEL is missing from your .env file. "
                "Set it to a model available to your API key."
            )

        response = client.models.generate_content(
            model=model_name,
            contents=prompt,
        )

        if response.text:
            return response.text

        return "The AI returned an empty response. Please try again."

    except Exception as error:
        print(f"TenantEase AI error: {error}")

        return (
            "Sorry, I couldn't generate an answer right now. "
            "Check your API configuration, model availability, "
            "internet connection, and API quota."
        )

def generate_rent_reminder(payment_details):
    """
    Use Gemini to draft a polite rent reminder.
    This function generates text only; it does not send messages.
    """

    if not payment_details:
        return "No outstanding payments were found for this tenant."

    try:
        client = get_gemini_client()

        prompt = f"""
Draft a polite, professional rent reminder for a tenant.

Use only the supplied information:
{json.dumps(payment_details, indent=2, default=str)}

Requirements:
- Mention the tenant by name.
- Mention the outstanding amount in Indian rupees.
- Mention the relevant rent month and due date.
- Keep the tone respectful and non-threatening.
- Do not invent late fees, penalties, or legal consequences.
- Do not claim that payment has already been made.
- Provide a short subject line and email body.
- This is a draft for a property manager to review.
- Do not send the message.
"""

        model_name = os.getenv("GEMINI_MODEL")

        if not model_name:
            return "GEMINI_MODEL is missing from your .env file."

        response = client.models.generate_content(
            model=model_name,
            contents=prompt,
        )

        return response.text or "Gemini returned an empty response."

    except Exception as error:
        print(f"Reminder generation error: {error}")
        return "Unable to generate the reminder. Check the application logs."    