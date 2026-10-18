# Evaluation Report: TenantEase AI Assistant

**Prepared for:** Cynbit Technologies — Technical Assessment  
**Project:** TenantEase AI Assistant  
**Document Type:** Prototype Evaluation Report  
**Status:** Independent Proof of Concept

---

## 1. Executive Summary

TenantEase AI Assistant is an independent proof of concept that combines a Streamlit dashboard, SQLite database, Python business logic, and Google's Gemini API.

The prototype demonstrates property-management information retrieval, rent collection calculations, overdue-payment identification, and AI-assisted rent reminder drafting.

The automated test suite currently contains seven passing tests covering selected rent-service and reminder-service behaviors.

These results provide basic evidence that the tested business logic behaves as expected for the available test scenarios. They do not establish overall AI accuracy, production readiness, or business impact.

## 2. Evaluation Objectives

The evaluation focuses on five objectives:

1. Verify rent calculations and outstanding-balance retrieval.
2. Verify identification of overdue payments.
3. Verify retrieval of vacant-room information.
4. Verify that reminder-service functions return appropriate payment information.
5. Assess the integration of Gemini with the application.

## 3. Testing Environment

| Component | Configuration |
|---|---|
| Programming language | Python |
| User interface | Streamlit |
| Database | SQLite |
| Generative AI | Google Gemini API |
| Testing framework | pytest |
| Data | Fictional demonstration records |
| Application type | Local proof of concept |

The application was developed and tested in a local Python virtual environment.

## 4. Automated Test Results

The latest reported automated test run completed with seven passing tests.

**Observed result: 7 passed in 0.15 seconds.**

The tests cover selected functions in the rent and reminder services.

| Test Area | Expected Behavior | Observed Result |
|---|---|---|
| October outstanding rent | Calculate outstanding rent for the selected month | Passed |
| October collection summary | Calculate rent due, rent collected, outstanding rent, and collection rate | Passed |
| Overdue-payment identification | Identify payments overdue as of a specified date | Passed |
| Vacant-room retrieval | Return the available vacant rooms | Passed |
| Reminder balances | Return outstanding payments for reminder workflows | Passed |
| Reminder record fields | Return the required tenant and payment information | Passed |
| Tenant payment details | Retrieve outstanding payment details for reminder generation | Passed |

The exact test names may differ slightly depending on the current contents of the test files.

These are unit-level checks of selected service functions. They do not verify every application workflow or every possible input.

## 5. Financial Calculation Validation

The demonstration database has been used to validate the following October 2026 figures:

| Metric | Expected Value |
|---|---:|
| Total rent due | ₹82,000 |
| Total rent collected | ₹34,000 |
| Outstanding rent | ₹48,000 |
| Collection rate | 41.46% |

### Calculation

Outstanding rent:

₹82,000 − ₹34,000 = ₹48,000

Collection rate:

(₹34,000 ÷ ₹82,000) × 100 ≈ 41.46%

These values represent the intended October demonstration dataset. They should be confirmed against the current database before being presented as actual application output, because the sample database has previously differed from the initially intended records.

## 6. Functional Evaluation

### 6.1 Dashboard

**Purpose:** Display property metrics, rent collection information, and payment records.

**Evaluation criteria:**
- Dashboard loads successfully.
- Metrics are retrieved from the database.
- Charts display available data.
- Financial figures match the underlying records.

The dashboard should be manually checked before submission.

### 6.2 Rent Intelligence

**Purpose:** Summarize outstanding payments and collection performance.

**Evaluation criteria:**
- Outstanding balances are calculated correctly.
- Fully paid records are not counted as outstanding.
- Reporting periods are clearly identified.
- Collection rates handle zero-value totals safely.

Automated service tests cover selected calculations. Additional boundary testing remains necessary.

### 6.3 Gemini AI Assistant

**Purpose:** Answer property-management questions using supplied database context.

**Evaluation criteria:**
- The application accepts a natural-language question.
- Gemini returns a response when the API is available.
- The response is consistent with supplied records.
- Missing configuration and API failures are handled appropriately.
- Unsupported financial claims are identified during evaluation.

The Gemini integration has been confirmed to work during development. However, no comprehensive AI accuracy benchmark has been conducted.

### 6.4 Rent Reminder Generation

**Purpose:** Generate polite rent reminder drafts using tenant payment information.

**Evaluation criteria:**
- Outstanding payments can be retrieved.
- The reminder includes the relevant tenant and payment details.
- The message avoids unsupported penalties or legal claims.
- A human can review the draft before sending.
- No message is sent automatically by the current prototype.

Automated tests cover selected reminder-service behaviors. The quality and factual accuracy of generated messages should also be evaluated manually.

## 7. AI Evaluation Plan

A more comprehensive evaluation should use a predefined set of questions and verified expected answers.

Example evaluation cases:

| Question | Expected Evidence |
|---|---|
| How much rent is outstanding for October? | Outstanding balance calculated from October payment records |
| What is the collection rate for October? | Rate calculated from total paid and total due |
| Which rooms are vacant? | Room identifiers and property details retrieved from SQLite |
| Who has overdue rent? | Tenants with overdue payments and outstanding balances |
| Draft a rent reminder | Accurate payment information and professional wording |
| What information is unavailable? | The assistant clearly acknowledges missing data |

For each question, reviewers should compare the response against the database and record whether the answer is factually correct, complete, and appropriately qualified.

The application should not be described as having achieved a particular AI accuracy percentage until such an evaluation has been performed.

## 8. Known Limitations

The current prototype has the following limitations:

1. It uses fictional demonstration data.
2. The assistant supplies predefined database context rather than dynamically selecting specialized queries for every question.
3. The reporting period is partly hardcoded.
4. Generative AI responses may contain errors.
5. The seven passing tests cover only selected business-logic functions.
6. The user interface has not been comprehensively tested across all possible workflows.
7. Reminder messages are generated as drafts; automated delivery is not implemented.
8. Authentication and role-based access control are not yet implemented.
9. No predictive rent-delay model has been trained.
10. Production-scale performance and security have not been evaluated.

## 9. Recommended Improvements

### Short-Term Improvements
- Expand automated test coverage.
- Validate financial outputs against database queries.
- Test missing API keys and API failures.
- Improve error messages.
- Make reporting periods configurable.
- Evaluate AI answers against verified examples.

### Medium-Term Improvements
- Add authentication and authorization.
- Add audit logging.
- Introduce more comprehensive integration tests.
- Improve database handling for concurrent users.
- Add controlled email or SMS integration with human approval.

### Long-Term Improvements
- Evaluate predictive rent-delay analysis using historical data.
- Introduce operational monitoring.
- Conduct user acceptance testing.
- Measure time saved and other business outcomes.

## 10. Conclusion

The prototype demonstrates the feasibility of combining structured property-management data with generative AI to support information retrieval, rent analysis, and reminder drafting.

The latest reported automated test run completed successfully with seven passing tests.

The project provides a useful foundation for further experimentation. However, additional testing, security controls, privacy safeguards, and evaluation of AI-generated answers are required before production deployment.

**Disclaimer:** This is an independent proof of concept developed for a technical assessment. It does not represent an official Cynbit Technologies implementation or integration.