# TenantEase AI Assistant 🏠🤖

### AI-Powered Rental Property Management Assistant

TenantEase AI Assistant is an AI/ML proof of concept that explores how Artificial Intelligence can improve rental property management workflows.

The application combines property management, tenant information, rent collection analytics, payment tracking, and a Google Gemini-powered AI assistant in an interactive dashboard.

The goal is to demonstrate how AI and data-driven insights can help property managers understand rental performance, identify outstanding payments, and simplify routine communication.

**Project Type:** AI/ML Engineering Proof of Concept  
**Interface:** Streamlit  
**Programming Language:** Python  
**Database:** SQLite  
**AI Integration:** Google Gemini API  

> **Disclaimer:** This is an independently developed proof of concept for an AI/ML Engineer Intern technical assessment at Cynbit Technologies. It is not an official TenantEase product and is not integrated with Cynbit Technologies' systems. The application uses demonstration data.

## 🚀 Live Demo

**Try TenantEase AI Assistant:** [Open the Live Application](https://tenantease-assistant.streamlit.app/)

> **Note:** This is a demonstration application. It uses demonstration data, and AI-powered features require valid Google Gemini API configuration. Availability of AI responses depends on the API service and account quota.

---

## 📌 Table of Contents

- [Project Overview](#-project-overview)
- [Key Features](#-key-features)
- [Technology Stack](#-technology-stack)
- [Project Architecture](#-project-architecture)
- [Installation and Setup](#-installation-and-setup)
- [Running the Application](#-running-the-application)
- [Running Tests](#-running-tests)
- [AI Integration Workflow](#-ai-integration-workflow)
- [Assessment Reports](#-assessment-reports)
- [Limitations](#-limitations)
- [Future Improvements](#-future-improvements)
- [Security and Privacy](#-security-and-privacy)

---

## 🎯 Project Overview

Managing rental properties involves tracking tenants, monitoring payments, identifying overdue rent, and communicating with tenants.

These activities can become difficult when property information and payment records are maintained separately.

TenantEase AI Assistant demonstrates a centralized approach to these workflows using Python, SQLite, Streamlit, and generative AI.

The application combines traditional database queries and Python-based financial calculations with an AI assistant that can answer questions using the available application data.

### Project Objectives

- Centralize rental property and tenant information.
- Monitor rent collection and outstanding payments.
- Identify overdue payments and vacant rooms.
- Use natural-language questions to explore rental information.
- Generate professional rent reminder drafts with AI.
- Demonstrate practical AI integration in a Python application.

---

## 🚀 Key Features

### 1. Property Management Dashboard

- View property and room statistics.
- Track occupied and vacant rooms.
- Review rental collection metrics.
- Visualize important property management indicators.

### 2. Tenant Management

- View tenant and property information.
- Access tenant payment records.
- Track rental payment status.
- Identify tenants with outstanding balances.

### 3. Rent Intelligence

- Calculate rent due, collected, and outstanding.
- Review rent collection performance.
- Identify overdue payments.
- Retrieve information about vacant rooms.
- Support data-driven rental management decisions.

### 4. Gemini-Powered AI Assistant

- Ask natural-language questions about available property and rental data.
- Receive summaries of rental collection performance.
- Identify tenants with outstanding payments.
- Generate contextual answers using information retrieved from the application database.
- Explore rental information without manually reviewing every record.

### 5. AI-Assisted Rent Reminders

- Identify tenants who may require payment reminders.
- Retrieve relevant tenant and payment information.
- Generate professional reminder drafts using Gemini.
- Allow the user to review the generated content.

**Important:** The application generates reminder drafts only. It does not automatically send emails, SMS messages, or WhatsApp messages.

---

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core application logic and data processing |
| Streamlit | Interactive web application |
| SQLite | Storage for properties, rooms, tenants, and payment records |
| Google Gemini API | Natural-language question answering and reminder generation |
| Pandas | Data processing and tabular operations |
| Plotly | Interactive charts and visualizations |
| python-dotenv | Loading environment variables |
| pytest | Automated testing |

---

## 🏗️ Project Architecture

The application follows a modular structure that separates the user interface, database operations, business logic, AI integration, and testing.

```text
TenantEase-AI/
│
├── app.py
├── requirements.txt
├── README.md
├── .env
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
```

*This tree describes the intended project organization. Update it if the actual files in your repository differ.*

### Architecture Components

**Presentation Layer — Streamlit**

Provides the interactive dashboard, navigation, data displays, charts, and AI chat interface.

**Database Layer — SQLite**

Stores structured information about properties, rooms, tenants, and rent payments.

**Business Logic Layer — Python**

Contains functions for retrieving property information, calculating outstanding rent, summarizing collections, and identifying overdue payments.

**AI Layer — Google Gemini API**

Receives a user question and relevant application context, then generates a natural-language response.

**Testing Layer — pytest**

Tests selected business logic and reminder-related functionality.

---

## ⚙️ Installation and Setup

Follow these instructions to run the project on your local computer.

### Prerequisites

Install the following:

- Python 3.11 or newer, compatible with the project's dependencies.
- pip package manager.
- A Google Gemini API key for AI-powered features.
- Git, if you want to clone the repository.

### Step 1: Obtain the Project

If the project is hosted on GitHub:

```bash
git clone https://github.com/Ravikumar0444/TenantEase-AI
cd TenantEase-AI
```

Alternatively, open your existing `TenantEase-AI` project folder in VS Code.

### Step 2: Create a Virtual Environment

On Windows PowerShell:

```powershell
python -m venv venv
```

Activate the environment:

```powershell
.\venv\Scripts\Activate.ps1
```

If PowerShell prevents script execution, review your execution policy or use another supported activation method. Do not change system-wide security settings unnecessarily.

### Step 3: Install Dependencies

Run:

```powershell
python -m pip install -r requirements.txt
```

This installs the packages listed in `requirements.txt`.

### Step 4: Configure Environment Variables

Create a file named `.env` in the project's root directory.

Add:

```env
GEMINI_API_KEY=your_actual_gemini_api_key
GEMINI_MODEL=your_available_gemini_model
```

Replace the placeholder values with your actual Gemini API key and a model identifier available to your account.

Keep your real `.env` file private.

The `.env.example` file should contain placeholders only, for example:

```env
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=your_available_gemini_model
```

**Never commit your actual API key to GitHub.**

### Step 5: Initialize the Database

The application uses SQLite for storing demonstration data.

If the database has not been initialized, run:

```powershell
python -m database.db
```

To populate it with demonstration records, run:

```powershell
python -m database.seed
```

These commands assume that the scripts support module execution.

If your database is already initialized and populated, skip this step. Do not recreate the database unnecessarily, as doing so could affect existing records.

### Step 6: Start the Application

Run:

```powershell
streamlit run app.py
```

Streamlit will display a local URL in your terminal, typically:

```text
http://localhost:8501
```

Open the displayed URL in your browser to access the application.

---

## ☁️ Deployment

TenantEase AI Assistant is deployed using Streamlit Community Cloud.

### Configuration

Configure the following secrets in your Streamlit app settings:

- `GEMINI_API_KEY`: Your Google Gemini API key.
- `GEMINI_MODEL`: A model identifier supported by your API key.

Example configuration:

```toml
GEMINI_API_KEY = "your_gemini_api_key"
GEMINI_MODEL = "your_available_gemini_model"

## ▶️ Running the Application After Setup

Once the initial setup is complete, you generally only need to:

**1. Open the project folder in VS Code.**

**2. Open the terminal.**

**3. Activate the virtual environment:**

```powershell
.\venv\Scripts\Activate.ps1
```

**4. Start the application:**

```powershell
streamlit run app.py
```

**5. Open the local URL shown in the terminal.**

Keep the terminal running while you use the application.

To stop the application, press `Ctrl + C` in the terminal.

---

## 🧪 Running Tests

The project uses pytest to test selected business logic.

Run the tests from the project root:

```powershell
python -m pytest tests/ -v
```

The test suite covers selected functionality, including:

- Outstanding rent calculations.
- Rent collection summaries.
- Overdue payment identification.
- Vacant room retrieval.
- Rent reminder-related functionality.

The test results should be verified by running the tests in your current environment.

### Manual Testing

After starting the application, verify that:

1. The dashboard loads correctly.
2. Property and room information is displayed.
3. Tenant and payment records are accessible.
4. Rent collection metrics are displayed.
5. The AI assistant responds to a relevant question when Gemini is configured.
6. Rent reminder drafts can be generated if that feature is implemented.
7. No unexpected application errors appear.

Verify financial amounts against the database rather than relying exclusively on AI-generated responses.

---

## 🧠 AI Integration Workflow

The AI assistant uses the following workflow:

1. The user submits a natural-language question through the Streamlit interface.
2. The application retrieves relevant property and rental information.
3. Python service functions calculate relevant financial metrics.
4. The application prepares contextual information for the Gemini API.
5. Gemini generates a natural-language response using the supplied context.
6. The response is displayed in the application.

For rent reminders, the application retrieves relevant payment information and asks Gemini to draft a professional reminder.

The generated reminder is returned for review rather than automatically sent to the tenant.

### Reliability Considerations

- Financial calculations are performed by Python application logic.
- The AI assistant is instructed to use the supplied application context.
- AI-generated information should be checked against the underlying records.
- The language model should not be treated as an authoritative source for financial or legal decisions.
- The quality of the output depends on the accuracy of the source data and the model response.

---

## 📄 Assessment Reports

The `reports/` directory contains the project's supporting documentation.

| Report | Description |
|---|---|
| `ai_opportunity_report.md` | Explores AI opportunities, potential business value, risks, and future use cases. |
| `technical_approach.md` | Describes the architecture, technology stack, database design, and AI integration. |
| `evaluation_report.md` | Documents testing, evaluation methods, known limitations, and potential improvements. |

These reports explain the business problem, technical implementation, and evaluation approach behind the proof of concept.

---

## ⚠️ Limitations

This application is a proof of concept and is not intended for production use without further development.

- The application uses demonstration data rather than verified real-world rental records.
- AI-generated responses may contain inaccuracies.
- Financial insights depend on the correctness and consistency of the underlying database.
- The application does not automatically send rent reminders.
- No integration with an official TenantEase or Cynbit Technologies system is claimed.
- A complete production-grade authentication and authorization system is not implemented.
- Real tenant information would require appropriate privacy, security, and access controls.
- The application has not been established as suitable for production-scale workloads.

---

## 🔮 Future Improvements

Potential future enhancements include:

- Predicting late rent payments using historical payment data.
- Adding secure authentication and role-based access control.
- Integrating approved email or messaging services for reminders.
- Improving AI response evaluation and factual consistency.
- Adding audit logs and stronger data protection.
- Supporting larger property portfolios.
- Introducing more comprehensive automated tests.
- Deploying the application to a secure hosting environment.
- Evaluating performance using representative real-world datasets.

---

## 🔐 Security and Privacy

- Store API keys in environment variables.
- Never commit credentials or secrets to version control.
- Use synthetic or anonymized data for demonstrations.
- Restrict access to tenant information in future production deployments.
- Review AI-generated content before using it for tenant communication.
- Apply appropriate access controls before handling real financial or personal information.

---

## 👨‍💻 Project Information

**Project Name:** TenantEase AI Assistant

**Project Category:** Artificial Intelligence / Machine Learning

**Programming Language:** Python

**User Interface:** Streamlit

**Database:** SQLite

**AI Integration:** Google Gemini API

**Purpose:** AI/ML Engineer Intern Technical Assessment

Developed as an independent proof of concept to explore how AI can support rental property management workflows.

---

## 📌 Final Note

TenantEase AI Assistant demonstrates a practical integration of database-backed business logic, interactive data visualization, and generative AI.

The project focuses on making rental information easier to explore, identifying outstanding payments, and assisting with routine property management communication.

The current implementation is a demonstration and would require further validation, security improvements, and testing before use with real tenants or financial records.