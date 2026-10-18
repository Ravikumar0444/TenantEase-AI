import streamlit as st
import pandas as pd
import plotly.express as px

from src.property_service import (
    get_dashboard_metrics,
    get_tenant_payment_records,
)


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="TenantEase AI",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded",
)


# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown(
    """
    <style>
        .block-container {
            padding-top: 1.8rem;
            padding-bottom: 2rem;
            max-width: 1450px;
        }

        [data-testid="stSidebar"] {
            background-color: #111827;
        }

        [data-testid="stSidebar"] * {
            color: #F9FAFB;
        }

        .brand {
            font-size: 25px;
            font-weight: 800;
            margin-bottom: 0;
        }

        .brand-subtitle {
            color: #9CA3AF;
            font-size: 12px;
            margin-top: 4px;
            margin-bottom: 25px;
        }

        .page-subtitle {
            color: #64748B;
            font-size: 14px;
            margin-top: -12px;
        }

        .metric-card {
            background: #FFFFFF;
            border: 1px solid #E5EAF2;
            border-radius: 14px;
            padding: 19px;
            min-height: 130px;
            box-shadow: 0 2px 8px rgba(15, 23, 42, 0.03);
        }

        .metric-label {
            color: #64748B;
            font-size: 13px;
            font-weight: 600;
        }

        .metric-value {
            color: #172033;
            font-size: 27px;
            font-weight: 800;
            margin-top: 12px;
        }

        .metric-caption {
            color: #64748B;
            font-size: 12px;
            margin-top: 5px;
        }

        .section-heading {
            font-size: 19px;
            font-weight: 750;
            color: #172033;
            margin-bottom: 3px;
        }

        .section-caption {
            color: #64748B;
            font-size: 13px;
            margin-bottom: 15px;
        }

        .info-card {
            background: #FFFFFF;
            border: 1px solid #E5EAF2;
            border-radius: 14px;
            padding: 20px;
        }

        .assistant-card {
            background: linear-gradient(135deg, #EFF6FF, #F5F3FF);
            border: 1px solid #DBEAFE;
            border-radius: 16px;
            padding: 23px;
        }

        .assistant-title {
            color: #1E3A8A;
            font-size: 19px;
            font-weight: 750;
        }

        .assistant-text {
            color: #475569;
            font-size: 14px;
        }

        footer {
            visibility: hidden;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

try:
    metrics = get_dashboard_metrics()
    payment_records = get_tenant_payment_records()

except Exception as error:
    st.error(f"Could not load dashboard data: {error}")
    st.info(
        "Check that your SQLite database has been initialized "
        "and sample data has been inserted."
    )
    st.stop()


payment_df = pd.DataFrame(payment_records)


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:
    st.markdown(
        '<p class="brand">🏠 TenantEase AI</p>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<p class="brand-subtitle">'
        'PROPERTY INTELLIGENCE PLATFORM'
        '</p>',
        unsafe_allow_html=True,
    )

    st.markdown("### WORKSPACE")

    page = st.radio(
        "Navigation",
        [
            "Dashboard",
            "Properties",
            "Tenants",
            "Rent Intelligence",
            "AI Assistant",
        ],
        label_visibility="collapsed",
    )

    st.divider()

    st.markdown("**Demo environment**")
    st.caption("Fictional sample data")
    st.caption("Reporting period: October 2026")


# --------------------------------------------------
# DASHBOARD PAGE
# --------------------------------------------------

if page == "Dashboard":

    col_title, col_period = st.columns([3, 1])

    with col_title:
        st.title("Property Dashboard")
        st.markdown(
            '<p class="page-subtitle">'
            'Monitor properties, rental income, and occupancy.'
            '</p>',
            unsafe_allow_html=True,
        )

    with col_period:
        st.write("")
        st.info("📅 October 2026")

    st.divider()

    # KPI CARDS

    st.markdown(
        '<p class="section-heading">Portfolio Overview</p>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<p class="section-caption">'
        'A snapshot of your rental portfolio.'
        '</p>',
        unsafe_allow_html=True,
    )

    kpis = [
        (
            "TOTAL PROPERTIES",
            str(metrics["total_properties"]),
            "Properties managed",
        ),
        (
            "TOTAL ROOMS",
            str(metrics["total_rooms"]),
            "Across all properties",
        ),
        (
            "OCCUPIED ROOMS",
            str(metrics["occupied_rooms"]),
            f'{metrics["vacant_rooms"]} rooms vacant',
        ),
        (
            "OCCUPANCY RATE",
            (
                f'{metrics["occupied_rooms"] / metrics["total_rooms"] * 100:.1f}%'
                if metrics["total_rooms"] > 0
                else "0%"
            ),
            "Portfolio occupancy",
        ),
    ]

    cols = st.columns(4)

    for col, (label, value, caption) in zip(cols, kpis):
        with col:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">{label}</div>
                    <div class="metric-value">{value}</div>
                    <div class="metric-caption">{caption}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.write("")

    rent_cols = st.columns(3)

    rent_kpis = [
        (
            "EXPECTED MONTHLY RENT",
            f'₹{metrics["expected_rent"]:,.0f}',
        ),
        (
            "RENT COLLECTED",
            f'₹{metrics["rent_collected"]:,.0f}',
        ),
        (
            "OUTSTANDING RENT",
            f'₹{metrics["outstanding_rent"]:,.0f}',
        ),
    ]

    for col, (label, value) in zip(rent_cols, rent_kpis):
        with col:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">{label}</div>
                    <div class="metric-value">{value}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.write("")

    # CHARTS

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.markdown(
            '<p class="section-heading">Room Occupancy</p>',
            unsafe_allow_html=True,
        )

        occupancy_df = pd.DataFrame(
            {
                "Status": ["Occupied", "Vacant"],
                "Rooms": [
                    metrics["occupied_rooms"],
                    metrics["vacant_rooms"],
                ],
            }
        )

        fig = px.pie(
            occupancy_df,
            names="Status",
            values="Rooms",
            hole=0.68,
            color="Status",
            color_discrete_map={
                "Occupied": "#2563EB",
                "Vacant": "#E2E8F0",
            },
        )

        fig.update_traces(
            textinfo="percent+label",
            textposition="outside",
        )

        fig.update_layout(
            showlegend=False,
            margin=dict(t=20, b=20, l=20, r=20),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
        )

        st.plotly_chart(fig, use_container_width=True)

    with chart_col2:
        st.markdown(
            '<p class="section-heading">Rent Collection</p>',
            unsafe_allow_html=True,
        )

        collected = metrics["rent_collected"]
        outstanding = metrics["outstanding_rent"]

        rent_df = pd.DataFrame(
            {
                "Category": ["Collected", "Outstanding"],
                "Amount": [collected, outstanding],
            }
        )

        fig = px.bar(
            rent_df,
            x="Category",
            y="Amount",
            color="Category",
            color_discrete_map={
                "Collected": "#16A34A",
                "Outstanding": "#F59E0B",
            },
            text="Amount",
        )

        fig.update_traces(
            texttemplate="₹%{y:,.0f}",
            textposition="outside",
        )

        fig.update_layout(
            showlegend=False,
            margin=dict(t=25, b=20, l=10, r=10),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis_title=None,
            yaxis_title=None,
        )

        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # RECENT PAYMENTS

    st.markdown(
        '<p class="section-heading">Tenant Payment Activity</p>',
        unsafe_allow_html=True,
    )

    if not payment_df.empty:

        display_df = payment_df[
            [
                "tenant_name",
                "property_name",
                "room_number",
                "amount_due",
                "amount_paid",
                "outstanding_amount",
                "status",
            ]
        ].copy()

        display_df.columns = [
            "Tenant",
            "Property",
            "Room",
            "Rent Due (₹)",
            "Paid (₹)",
            "Outstanding (₹)",
            "Status",
        ]

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True,
        )

    else:
        st.info("No payment records available.")


# --------------------------------------------------
# PROPERTIES PAGE
# --------------------------------------------------

elif page == "Properties":

    st.title("Properties")
    st.caption("Explore the properties in your portfolio.")

    from database.db import get_connection

    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT
                p.property_name,
                p.city,
                COUNT(r.room_id) AS total_rooms,
                SUM(
                    CASE WHEN r.status = 'occupied'
                    THEN 1 ELSE 0 END
                ) AS occupied_rooms,
                SUM(
                    CASE WHEN r.status = 'vacant'
                    THEN 1 ELSE 0 END
                ) AS vacant_rooms
            FROM properties p
            LEFT JOIN rooms r
                ON p.property_id = r.property_id
            GROUP BY p.property_id
            ORDER BY p.property_name
            """
        ).fetchall()

    st.dataframe(
        pd.DataFrame([dict(row) for row in rows]),
        use_container_width=True,
        hide_index=True,
    )


# --------------------------------------------------
# TENANTS PAGE
# --------------------------------------------------

elif page == "Tenants":

    st.title("Tenant Directory")
    st.caption("Search tenant payment records.")

    if payment_df.empty:
        st.info("No tenant payment records available.")

    else:
        search = st.text_input(
            "Search by tenant or property name"
        )

        filtered_df = payment_df.copy()

        if search:
            mask = (
                filtered_df["tenant_name"].str.contains(
                    search,
                    case=False,
                    na=False,
                )
                |
                filtered_df["property_name"].str.contains(
                    search,
                    case=False,
                    na=False,
                )
            )

            filtered_df = filtered_df[mask]

        st.dataframe(
            filtered_df,
            use_container_width=True,
            hide_index=True,
        )


# --------------------------------------------------
# RENT INTELLIGENCE PAGE
# --------------------------------------------------

elif page == "Rent Intelligence":

    st.title("Rent Intelligence")
    st.caption(
        "Review rent collection and outstanding balances."
    )

    total_due = (
        payment_df["amount_due"].sum()
        if not payment_df.empty else 0
    )

    total_paid = (
        payment_df["amount_paid"].sum()
        if not payment_df.empty else 0
    )

    collection_rate = (
        total_paid / total_due * 100
        if total_due > 0 else 0
    )

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Due", f"₹{total_due:,.0f}")
    col2.metric("Total Paid", f"₹{total_paid:,.0f}")
    col3.metric("Collection Rate", f"{collection_rate:.1f}%")

    if not payment_df.empty:
        unpaid_df = payment_df[
            payment_df["outstanding_amount"] > 0
        ].copy()

        st.subheader("Accounts with Outstanding Balances")

        st.dataframe(
            unpaid_df[
                [
                    "tenant_name",
                    "property_name",
                    "amount_due",
                    "amount_paid",
                    "outstanding_amount",
                    "due_date",
                    "status",
                ]
            ],
            use_container_width=True,
            hide_index=True,
        )


# --------------------------------------------------
# AI ASSISTANT PREVIEW
# --------------------------------------------------

elif page == "AI Assistant":

    st.title("TenantEase AI Assistant")

    st.markdown(
        """
        <div class="assistant-card">
            <div class="assistant-title">
                Your property management copilot
            </div>
            <p class="assistant-text">
                Ask questions about rental income, tenants,
                occupancy, and outstanding payments.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")

    st.info(
        "The AI integration will be implemented in a later phase. "
        "For now, you can explore the dashboard and rent records."
    )

    st.markdown("### Example questions")

    examples = [
        "How much rent is outstanding?",
        "Which tenants have unpaid rent?",
        "What is my current occupancy rate?",
        "Which properties have vacant rooms?",
    ]

    for question in examples:
        st.markdown(f"- {question}")


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "TenantEase AI is an independent proof of concept "
    "using fictional sample data. It is not an official Cynbit integration."
)