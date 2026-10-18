# TenantEase AI Assistant 🏠🤖

### AI-Powered Rental Property Management Assistant

TenantEase AI Assistant is an independent AI/ML proof of concept designed to explore how Artificial Intelligence can simplify rental property management.

The application combines property management, tenant information, rent collection analytics, payment tracking, and a Gemini-powered AI assistant in a single interactive dashboard.

This project was developed as part of an AI/ML Engineer Intern technical assessment for Cynbit Technologies.

> **Disclaimer:** This is an independently developed proof of concept inspired by rental property management workflows. It is not an official TenantEase product and is not integrated with Cynbit Technologies' systems. The application uses demonstration data.

---

## 🚀 Key Features

### 1. Property Management Dashboard
- View property and room statistics.
- Track occupied and vacant rooms.
- Monitor rental collection metrics.
- Visualize important property management indicators.

### 2. Tenant Management
- View tenant and property information.
- Access tenant payment records.
- Track rental payment status.
- Identify tenants with outstanding balances.

### 3. Rent Intelligence
- Calculate total rent due, collected, and outstanding.
- Analyze rent collection performance.
- Identify overdue payments.
- Track vacant rooms and their associated rental information.

### 4. Gemini-Powered AI Assistant
- Ask questions about available property and rental data.
- Receive natural-language summaries of rent collection.
- Identify tenants with outstanding payments.
- Generate insights to support property management decisions.

### 5. AI-Assisted Rent Reminders
- Identify tenants who may require rent reminders.
- Generate professional rent reminder drafts using AI.
- Review reminder content before using it.

**Note:** The application generates reminder drafts but does not automatically send emails, SMS messages, or WhatsApp messages.

---

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core application logic |
| Streamlit | Interactive web interface |
| SQLite | Database for properties, rooms, tenants, and payments |
| Google Gemini API | AI-powered question answering and reminder generation |
| Pandas | Data processing |
| Plotly | Data visualization |
| python-dotenv | Environment variable management |
| pytest | Automated testing |

---

## 📁 Project Structure

```text
TenantEase-AI/
│
├── app.py
├── requirements.txt
├── README.md
├── .env.example
├── .gitignore
├── tenantease.db
│
├── database/
│   ├── __init__.py
│   ├── db.py
│   ├── schema.sql
│   └── seed.py
│
├── src/
│   ├── __init__.py
│   ├── property_service.py
│   ├── rent_service.py
│   ├── reminder_service.py
│   └── ai_assistant.py
│
├── tests/
│   ├── test_rent_service.py
│   └── test_reminder_service.py
│
├── reports/
│   ├── ai_opportunity_report.md
│   ├── technical_approach.md
│   └── evaluation_report.md
│
└── .streamlit/
    └── config.toml