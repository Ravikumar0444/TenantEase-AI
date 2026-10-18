# Technical Approach Report: TenantEase AI Assistant

**Prepared for:** Cynbit Technologies — Technical Assessment  
**Project:** TenantEase AI Assistant  
**Document Type:** Technical Implementation Report  
**Status:** Independent Proof of Concept

---

## 1. Introduction

TenantEase AI Assistant is an independent proof of concept designed to demonstrate how generative AI can support property-management workflows.

The application allows users to explore property information, review rent collection metrics, identify outstanding payments, ask questions through a natural-language interface, and generate rent reminder drafts.

The implementation combines a Streamlit frontend, Python business logic, an SQLite database, and Google's Gemini API.

The prototype uses fictional demonstration data and is not an official integration with Cynbit Technologies or TenantEase.

## 2. Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application logic and data processing |
| Streamlit | Interactive web interface |
| SQLite | Relational data storage |
| SQL | Database queries and aggregations |
| Pandas | Tabular data presentation |
| Plotly | Dashboard visualizations |
| Google Gemini API | Natural-language responses and reminder generation |
| python-dotenv | Environment variable management |
| pytest | Automated testing |

### 2.1 Why Python?

Python provides a straightforward way to integrate databases, web interfaces, and generative AI APIs. It also supports future integration with machine-learning models.

### 2.2 Why Streamlit?

Streamlit enables rapid development of interactive dashboards and forms without requiring a separate JavaScript frontend.

### 2.3 Why SQLite?

SQLite provides relational data storage without requiring a separate database server. It is suitable for a local proof of concept.

A production deployment with concurrent users or larger operational requirements may need a managed database such as PostgreSQL.

### 2.4 Why Gemini?

Gemini provides natural-language generation capabilities that can be used to explain structured information and draft tenant communications.

The model does not replace database queries or authoritative financial calculations.

## 3. System Architecture

The application is organized into four logical layers.

### 3.1 Presentation Layer

**File:** `app.py`

Responsibilities:
- Display dashboard metrics and charts.
- Present property and tenant information.
- Show rent collection insights.
- Provide the AI assistant interface.
- Allow users to review generated reminder drafts.

### 3.2 Business Logic Layer

**Directory:** `src/`

Responsibilities include:
- Retrieving property and payment metrics.
- Calculating outstanding rent.
- Identifying overdue payments.
- Retrieving vacant rooms.
- Preparing context for AI responses.
- Generating reminder drafts.

The business logic separates database operations from presentation code.

### 3.3 Data Layer

**Directory:** `database/`

Responsibilities:
- Define the database schema.
- Create database connections.
- Initialize database tables.
- Populate fictional demonstration records.

SQLite stores the application's structured information.

### 3.4 AI Integration Layer

**File:** `src/ai_assistant.py`

Responsibilities:
- Load the Gemini API configuration.
- Construct prompts.
- Supply retrieved database context to the model.
- Generate natural-language responses.
- Generate rent reminder drafts.

The current implementation sends selected database information to Gemini as part of the prompt.

## 4. Database Design

The database contains four main tables.

### 4.1 Properties

Stores property-level information.

| Column | Description |
|---|---|
| property_id | Primary key |
| property_name | Property name |
| address | Property address |
| city | City |
| property_type | Property category |

### 4.2 Rooms

Stores room-level information and rental amounts.

| Column | Description |
|---|---|
| room_id | Primary key |
| property_id | Foreign key referencing properties |
| room_number | Room identifier |
| monthly_rent | Monthly rental amount |
| status | Occupied or vacant |

A uniqueness constraint prevents duplicate room numbers within the same property.

### 4.3 Tenants

Stores tenant information associated with rooms.

| Column | Description |
|---|---|
| tenant_id | Primary key |
| room_id | Foreign key referencing rooms |
| tenant_name | Tenant name |
| email | Tenant email address |
| phone | Tenant phone number |
| lease_start | Lease start date |
| lease_end | Lease end date |

### 4.4 Payments

Stores rent-payment records.

| Column | Description |
|---|---|
| payment_id | Primary key |
| tenant_id | Foreign key referencing tenants |
| rent_month | Reporting month |
| amount_due | Amount due |
| amount_paid | Amount paid |
| due_date | Payment deadline |
| payment_date | Actual payment date, when available |
| status | Payment status |

The schema includes constraints for nonnegative monetary amounts, valid room statuses, valid payment statuses, and unique tenant-payment records for each rent month.

Foreign-key enforcement is enabled through the database connection.

## 5. Application Workflow

### 5.1 Dashboard Workflow

1. The user opens the dashboard.
2. Python service functions query SQLite.
3. The application calculates property and rent metrics.
4. Streamlit displays summary cards, charts, and payment records.

### 5.2 Rent Intelligence Workflow

1. The user opens the rent intelligence page.
2. The application retrieves payment records.
3. Python calculates outstanding balances and collection metrics.
4. Streamlit displays the results.

### 5.3 AI Assistant Workflow

1. The user enters a natural-language question.
2. The application retrieves a predefined set of property and payment information.
3. The retrieved information is serialized into the prompt.
4. Gemini generates a natural-language response.
5. Streamlit displays the response.

**Current limitation:** The assistant supplies a predefined context for each question rather than selecting a specialized database query based on the user's intent. A future version should implement controlled intent detection and query selection.

### 5.4 Reminder Generation Workflow

1. The application retrieves payments with outstanding balances past their due dates.
2. The user selects a tenant.
3. The application retrieves the tenant's outstanding payment details.
4. Gemini drafts a reminder using the supplied information.
5. The user reviews the generated draft.

The current prototype does not send emails or SMS messages automatically.

## 6. Financial Calculations

Financial calculations are performed in Python or SQL.

### Outstanding Balance

For each payment:

Outstanding Balance = Amount Due − Amount Paid

### Collection Rate

Collection Rate = (Total Amount Paid ÷ Total Amount Due) × 100

If total rent due is zero, the application should return a collection rate of zero rather than dividing by zero.

### Overdue Payment Identification

A payment is considered overdue when:

- Its due date is earlier than the reporting date.
- The amount paid is less than the amount due.

This definition excludes payments that have been paid in full, even when their due dates have passed.

The reporting period and date should be clearly specified when presenting financial results.

## 7. Generative AI Integration

The application uses the Google Gen AI Python SDK.

The API key and model name are configured through environment variables.

Example configuration:

```dotenv
GEMINI_API_KEY=your_api_key
GEMINI_MODEL=your_available_gemini_model
```

The `.env` file should not be committed to source control.

The AI prompt instructs the model to:
- Use the supplied database context.
- Avoid inventing tenant or payment information.
- Use Indian rupees for monetary amounts.
- Distinguish paid, partially paid, and unpaid rent.
- State when the required information is unavailable.
- Generate professional reminder drafts without inventing penalties or legal consequences.

These instructions reduce the likelihood of unsupported responses but do not guarantee factual accuracy. Model outputs require evaluation.

## 8. Testing Strategy

The project uses pytest for automated testing.

The current test suite contains seven passing tests covering rent-service and reminder-service behavior.

The tests cover areas such as:
- Outstanding rent calculations.
- Rent collection summaries.
- Overdue payment identification.
- Vacant-room retrieval.
- Reminder records and required fields.
- Retrieval of tenant payment details.

These tests provide basic regression protection for business logic.

They do not constitute comprehensive testing of the Streamlit interface, Gemini responses, security, or production performance.

Further testing should include:
- Empty database scenarios.
- Invalid user input.
- Missing API credentials.
- API quota exhaustion.
- Network failures.
- Unexpected model responses.
- Date-boundary cases.
- Database consistency.
- End-to-end user workflows.

## 9. Security and Privacy

The current prototype is intended for demonstration using fictional data.

Before production use, the system should implement:

- User authentication.
- Role-based access controls.
- Input validation.
- Secure API-key storage.
- Appropriate database access restrictions.
- Audit logging for sensitive actions.
- Data-retention policies.
- Privacy controls for external AI requests.
- Human approval for tenant communications.

Only the minimum necessary information should be sent to an external AI service.

The prototype should not be represented as production-ready without these additional controls and a security review.

## 10. Limitations

The current implementation has several limitations:

1. It uses fictional demonstration data.
2. SQLite is used as a lightweight local database.
3. The reporting period is partly hardcoded to October 2026.
4. The AI assistant receives predefined database context.
5. Gemini-generated answers may still contain errors.
6. Reminder drafts require human review.
7. No email or SMS delivery system is implemented.
8. No predictive rent-delay model has been trained.
9. Authentication and role-based access controls are not yet implemented.
10. The seven passing tests do not establish production reliability.

## 11. Future Improvements

Potential improvements include:

- Configurable reporting periods.
- Controlled natural-language query routing.
- Additional automated tests.
- Authentication and authorization.
- PostgreSQL integration.
- Email and SMS delivery with approval workflows.
- Audit logs and monitoring.
- Retrieval of relevant records based on question intent.
- Evaluation datasets for measuring AI answer accuracy.
- Predictive rent-delay analysis using suitable historical data.

## 12. Conclusion

TenantEase AI Assistant demonstrates a practical architecture for combining relational data, Python business logic, an interactive dashboard, and generative AI.

The design keeps financial calculations within deterministic application code while using Gemini for natural-language explanations and reminder drafting.

The implementation provides a foundation for further experimentation, but additional testing, privacy safeguards, security controls, and operational engineering would be required before production deployment.

**Disclaimer:** This is an independent proof of concept prepared for a technical assessment. It is not an official Cynbit Technologies implementation or integration.