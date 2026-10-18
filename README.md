TenantEase AI Assistant
AI-Powered Rental Property Management Proof of Concept

TenantEase AI Assistant is an independent AI/ML proof of concept designed to explore how artificial intelligence can improve rental property management workflows.

The application combines property and tenant information, rent collection analytics, payment tracking, and a Gemini-powered AI assistant in a single dashboard.

This project was developed as a technical assessment project for an AI/ML Engineer Intern role at Cynbit Technologies.

Disclaimer: This is an independently developed proof of concept. It is not an official TenantEase product or an integrated Cynbit Technologies system. The demonstration uses sample data and does not connect to real tenants or properties.

Features
1. Property Management Dashboard
View property and room statistics.
Track occupied and vacant rooms.
Review rental collection metrics.
Visualize important property management indicators.
2. Tenant and Payment Tracking
View tenant and property information.
Review rental payment records.
Identify pending and overdue payments.
Track outstanding rent balances.
3. Rent Intelligence
Calculate rent due, collected, and outstanding.
Review collection performance.
Identify tenants with unpaid balances.
Analyze payment information using predefined calculations.
4. Gemini-Powered AI Assistant
Ask natural-language questions about property and rental data.
Obtain contextual answers using the available application data.
Summarize rental collection and outstanding payments.
Generate insights to support property management decisions.
5. AI-Assisted Rent Reminders
Identify tenants who may require payment reminders.
Generate professional rent reminder drafts.
Review reminder details before using them.

Note: The application generates reminder drafts only. It does not automatically send emails, SMS messages, or WhatsApp messages.

Technology Stack
Component	Technology
Programming language	Python
User interface	Streamlit
Database	SQLite
AI integration	Google Gemini API
Data processing	Pandas
Data visualization	Plotly
Configuration management	python-dotenv
Testing	pytest
Project Architecture

The project is organized into separate components to make the code easier to understand, maintain, and extend.

TenantEase-AI/
│
├── app.py
├── requirements.txt
├── README.md
├── .env.example
├── .gitignore
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

The structure above represents the expected project organization. Adjust it if your actual files differ.

How to Run the Project
Prerequisites

Install the following before running the application:

Python 3.11 or newer, subject to compatibility with the installed dependencies.
pip.
A Google Gemini API key for AI-powered features.
Step 1: Clone the Repository

After uploading the project to GitHub, run:

git clone YOUR_GITHUB_REPOSITORY_URL
cd TenantEase-AI

Replace YOUR_GITHUB_REPOSITORY_URL with your actual repository URL.

If you already have the project locally, open a terminal in your existing project folder instead.

Step 2: Create and Activate a Virtual Environment

On Windows PowerShell:

python -m venv venv
.\venv\Scripts\Activate.ps1

If your virtual environment is already active, you can skip this step.

Step 3: Install Dependencies
python -m pip install -r requirements.txt
Step 4: Configure Environment Variables

Create a .env file in the project root.

Add the following configuration:

GEMINI_API_KEY=your_actual_gemini_api_key
GEMINI_MODEL=your_available_gemini_model

Replace the placeholder values with your actual API key and a model identifier available to your Gemini API account.

Keep your real .env file private. Never commit your API key to GitHub.

Step 5: Initialize the Database

The application uses SQLite to store demonstration property, room, tenant, and payment records.

If your repository does not include a preconfigured tenantease.db, initialize the database:

python -m database.db

Then populate it with demonstration data:

python -m database.seed

Run these commands only if they match the entry points implemented in your files. If your existing database is already initialized and seeded, do not recreate it unnecessarily.

Step 6: Launch the Application
streamlit run app.py

Streamlit should display a local URL in your terminal. Open that URL in your browser to use the application.

Step 7: Run the Tests

In a separate terminal, activate the virtual environment and run:

python -m pytest tests/ -v

The tests cover selected rental calculations, outstanding payments, overdue payment identification, vacant rooms, and reminder-related functionality.

Reports

The reports/ directory contains three assessment deliverables.

Report	Purpose
ai_opportunity_report.md	Identifies AI opportunities, business value, risks, and potential future applications.
technical_approach.md	Describes the architecture, technology stack, database, AI integration, and implementation approach.
evaluation_report.md	Documents tests, evaluation methods, limitations, and potential improvements.

These reports complement the working application by explaining the business problem, technical decisions, and evaluation strategy.

Limitations

This is a proof of concept, not a production-ready property management platform.

The application uses demonstration data rather than verified real-world property records.
AI responses depend on the data supplied to the model and may not always be correct.
Financial calculations depend on the accuracy and consistency of the underlying database records.
The application does not automatically send payment reminders.
No integration with an official TenantEase or Cynbit Technologies system is claimed.
Authentication, authorization, and production-grade multi-user access controls would require further development.
AI-generated outputs should be reviewed before being used for actual tenant communication or financial decisions.
Future Improvements

Potential improvements include:

Predicting late rent payments using historical payment data.
Adding secure authentication and role-based access control.
Integrating approved email or messaging services for reminders.
Improving AI response evaluation and factual consistency.
Adding audit logs and stronger data protection.
Deploying the application to a secure hosting environment.
Evaluating performance on a larger, representative dataset.
Security
Store API keys in environment variables.
Do not upload .env or other files containing secrets.
Use synthetic or anonymized data in public demonstrations.
Restrict access to tenant information in any future production deployment.
Review AI-generated content before relying on it.
Author

Developed as an independent AI/ML engineering proof of concept for a technical assessment.
