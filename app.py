import streamlit as st
import pandas as pd
import plotly.express as px
from src.ai_assistant import ask_tenantease_ai
from src.property_service import (
    add_tenant,
    get_vacant_rooms,
    get_all_tenants,
    delete_tenant,
    deactivate_tenant,
)
from src.property_service import (
    get_all_properties,
    add_property,
    update_property,
    delete_property,
    get_property_room_summary,
    add_room,
)

from src.rent_service import settle_all_tenant_payments
from src.rent_service import get_tenants_with_outstanding_payments

from src.reminder_service import (
    get_tenants_needing_reminders,
    generate_reminder_details,
)

from src.ai_assistant import generate_rent_reminder

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
            "Rent Reminders",
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

    st.title("🏢 Property Management")
    st.caption("Add, view, edit, and manage your properties.")

    # Fetch the latest property records.
    properties = get_all_properties()

    # Property summary.
    st.metric("Total Properties", len(properties))

    st.divider()

    st.subheader("🚪 Add Room to Property")

    properties_for_rooms = get_all_properties()

    if not properties_for_rooms:
        st.info("Add a property before creating rooms.")
    else:
        property_options = {
            f"{p['property_name']} — {p['city']} (ID: {p['property_id']})":
            p["property_id"]
            for p in properties_for_rooms
        }

        with st.form("add_room_form", clear_on_submit=True):
            selected_property = st.selectbox(
                "Select Property",
                options=list(property_options.keys()),
            )

            room_number = st.text_input(
                "Room Number",
                placeholder="e.g., 101",
            )

            monthly_rent = st.number_input(
                "Monthly Rent (₹)",
                min_value=1.0,
                value=8000.0,
                step=500.0,
            )

            room_submitted = st.form_submit_button(
                "➕ Add Room",
                use_container_width=True,
            )

            if room_submitted:
                property_id = property_options[selected_property]

                success, message = add_room(
                    property_id,
                    room_number,
                    monthly_rent,
                )

                if success:
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)

    # ---------- ADD PROPERTY ----------
    st.subheader("➕ Add New Property")

    with st.form("add_property_form", clear_on_submit=True):

        property_name = st.text_input("Property Name")
        address = st.text_input("Address")
        city = st.text_input("City")

        property_type = st.selectbox(
            "Property Type",
            ["Residential", "Commercial", "Mixed Use", "Other"],
        )

        add_submitted = st.form_submit_button(
            "Add Property",
            use_container_width=True,
        )

        if add_submitted:

            success, message = add_property(
                property_name,
                address,
                city,
                property_type,
            )

            if success:
                st.success(message)
                st.rerun()
            else:
                st.error(message)

    st.divider()

    # ---------- VIEW PROPERTIES ----------
    st.subheader("📋 Existing Properties")

    properties = get_all_properties()

    if not properties:

        st.info("No properties found. Add your first property above.")

    else:

        for property_data in properties:

            property_id = property_data["property_id"]

            with st.expander(
                f"🏠 {property_data['property_name']} "
                f"— {property_data['city']}"
            ):

                st.write(f"**Property ID:** {property_id}")
                st.write(f"**Address:** {property_data['address']}")
                st.write(f"**Type:** {property_data['property_type']}")
                room_summary = get_property_room_summary(property_id)

                st.markdown("#### 🏠 Room Overview")

                col1, col2, col3, col4 = st.columns(4)

                col1.metric("Total Rooms", room_summary["total_rooms"])
                col2.metric("Occupied", room_summary["occupied_rooms"])
                col3.metric("Vacant", room_summary["vacant_rooms"])
                col4.metric("Occupancy", f"{room_summary['occupancy_rate']}%")

                # ---------- EDIT PROPERTY ----------
                st.markdown("#### Edit Property")

                with st.form(f"edit_property_{property_id}"):

                    edited_name = st.text_input(
                        "Property Name",
                        value=property_data["property_name"],
                        key=f"edit_name_{property_id}",
                    )

                    edited_address = st.text_input(
                        "Address",
                        value=property_data["address"],
                        key=f"edit_address_{property_id}",
                    )

                    edited_city = st.text_input(
                        "City",
                        value=property_data["city"],
                        key=f"edit_city_{property_id}",
                    )

                    available_types = [
                        "Residential",
                        "Commercial",
                        "Mixed Use",
                        "Other",
                    ]

                    current_type = property_data["property_type"]

                    if current_type not in available_types:
                        available_types.append(current_type)

                    edited_type = st.selectbox(
                        "Property Type",
                        available_types,
                        index=available_types.index(current_type),
                        key=f"edit_type_{property_id}",
                    )

                    edit_submitted = st.form_submit_button(
                        "Save Changes",
                        use_container_width=True,
                    )

                    if edit_submitted:

                        success, message = update_property(
                            property_id,
                            edited_name,
                            edited_address,
                            edited_city,
                            edited_type,
                        )

                        if success:
                            st.success(message)
                            st.rerun()
                        else:
                            st.error(message)

                # ---------- DELETE PROPERTY ----------
                st.markdown("#### Delete Property")

                has_rooms = False

                from database.db import get_connection

                with get_connection() as connection:

                    room_count = connection.execute(
                        """
                        SELECT COUNT(*)
                        FROM rooms
                        WHERE property_id = ?
                        """,
                        (property_id,),
                    ).fetchone()[0]

                    has_rooms = room_count > 0

                if has_rooms:

                    st.warning(
                        f"This property has {room_count} associated room(s). "
                        "Permanent deletion is blocked to protect tenant "
                        "and payment records."
                    )

                else:

                    confirm_delete = st.checkbox(
                        "I confirm that I want to delete this property.",
                        key=f"confirm_delete_{property_id}",
                    )

                    if st.button(
                        "🗑️ Delete Property",
                        key=f"delete_property_{property_id}",
                        use_container_width=True,
                    ):

                        if not confirm_delete:

                            st.warning(
                                "Please confirm deletion first."
                            )

                        else:

                            success, message = delete_property(
                                property_id
                            )

                            if success:
                                st.success(message)
                                st.rerun()
                            else:
                                st.error(message)

# --------------------------------------------------
# TENANTS PAGE
# --------------------------------------------------

elif page == "Tenants":

    st.title("Tenant Directory")
    st.caption("Search tenant payment records.")

    # Add New Tenant form
    with st.expander("➕ Add New Tenant", expanded=False):

        vacant_rooms = get_vacant_rooms()

        if not vacant_rooms:
            st.info(
                "No vacant rooms are currently available. "
                "Add a vacant room before registering a tenant."
            )

        else:
            room_options = {
                (
                    f"{room['property_name']} | "
                    f"Room {room['room_number']} | "
                    f"₹{room['monthly_rent']:,.0f}/month"
                ): room["room_id"]
                for room in vacant_rooms
            }

            with st.form("add_tenant_form"):

                tenant_name = st.text_input(
                    "Tenant Name *",
                    placeholder="Enter tenant's full name",
                )

                email = st.text_input(
                    "Email Address",
                    placeholder="tenant@example.com",
                )

                phone = st.text_input(
                    "Phone Number",
                    placeholder="Enter phone number",
                )

                selected_room = st.selectbox(
                    "Select Vacant Room *",
                    options=list(room_options.keys()),
                )

                col1, col2 = st.columns(2)

                with col1:
                    lease_start = st.date_input(
                        "Lease Start Date",
                        value=None,
                    )

                with col2:
                    lease_end = st.date_input(
                        "Lease End Date",
                        value=None,
                    )

                submitted = st.form_submit_button(
                    "Add Tenant",
                    use_container_width=True,
                )

                if submitted:

                    if not tenant_name.strip():
                        st.error("Please enter the tenant's name.")

                    else:
                        room_id = room_options[selected_room]

                        success, message = add_tenant(
                            tenant_name=tenant_name,
                            email=email,
                            phone=phone,
                            room_id=room_id,
                            lease_start=(
                                lease_start.isoformat()
                                if lease_start else None
                            ),
                            lease_end=(
                                lease_end.isoformat()
                                if lease_end else None
                            ),
                        )

                        if success:
                            st.success(message)
                            st.rerun()

                        else:
                            st.error(message)

                            

    st.subheader("Registered Tenants")

    tenant_df = pd.DataFrame(get_all_tenants())

    if tenant_df.empty:
        st.info("No tenants registered yet. Use the form above to add one.")

    else:
        search = st.text_input(
            "Search by tenant or property name",
            key="tenant_directory_search",
        )

        filtered_df = tenant_df.copy()

        if search:
            mask = (
                filtered_df["tenant_name"].str.contains(
                    search, case=False, na=False
                )
                |
                filtered_df["property_name"].str.contains(
                    search, case=False, na=False
                )
            )
            filtered_df = filtered_df[mask]

        display_columns = [
            "tenant_name",
            "email",
            "phone",
            "room_number",
            "property_name",
            "monthly_rent",
            "lease_start",
            "lease_end",
        ]

        st.dataframe(
            filtered_df[display_columns],
            use_container_width=True,
            hide_index=True,
            column_config={
                "tenant_name": st.column_config.TextColumn("Tenant"),
                "email": st.column_config.TextColumn("Email"),
                "phone": st.column_config.TextColumn("Phone"),
                "property_name": st.column_config.TextColumn("Property"),
                "room_number": st.column_config.TextColumn("Room"),
                "monthly_rent": st.column_config.NumberColumn(
                    "Monthly Rent (₹)", format="₹%.2f"
                ),
                "lease_start": st.column_config.DateColumn("Lease Start"),
                "lease_end": st.column_config.DateColumn("Lease End"),
            },
        )
        st.divider()

        st.subheader("Deactivate Tenant")

        tenants = get_all_tenants()

        if tenants:
            tenant_options = {
                f"{tenant['tenant_name']} — "
                f"{tenant['property_name']}, Room {tenant['room_number']} "
                f"(ID: {tenant['tenant_id']})": tenant["tenant_id"]
                for tenant in tenants
            }

            selected_tenant = st.selectbox(
                "Select a tenant to deactivate",
                options=list(tenant_options.keys()),
                key="deactivate_tenant_select",
            )

            # Get the ID belonging to the selected tenant.
            tenant_id = tenant_options[selected_tenant]

            confirm_deactivate = st.checkbox(
                "I confirm that I want to deactivate this tenant.",
                key="confirm_deactivate_tenant",
            )

            if st.button(
                "Deactivate Tenant",
                key="deactivate_tenant_button",
                type="primary",
                disabled=not confirm_deactivate,
            ):
                success, message = deactivate_tenant(tenant_id)

                if success:
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)

        else:
            st.info("There are no active tenants available to deactivate.")
        st.caption(f"Total registered tenants: {len(filtered_df)}")


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

    # ---------- PAGE HEADER ----------
    st.title("✦ TenantEase AI")
    st.markdown(
        """
        <style>
        /* Modern chat input container */
        div[data-testid="stChatInput"] {
            border-radius: 24px;
            border: 1px solid #D1D5DB;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.06);
            background-color: var(--secondary-background-color);
            padding: 4px;
        }

        /* Input area */
        div[data-testid="stChatInput"] textarea {
            font-size: 16px;
            line-height: 1.5;
        }

        /* Focus effect */
        div[data-testid="stChatInput"]:focus-within {
            border-color: #6366F1;
            box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.15);
        }

        /* Send button */
        div[data-testid="stChatInput"] button {
            border-radius: 50%;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    
    st.caption(
        "Your intelligent property management assistant"
    )

    st.divider()

    # ---------- SESSION STATE ----------
    if "ai_messages" not in st.session_state:
        st.session_state.ai_messages = []

    # ---------- WELCOME SCREEN ----------
    if not st.session_state.ai_messages:

        st.markdown(
            """
            <div style="text-align: center; padding: 35px 10px 20px 10px;">
                <h2>How can I help you today?</h2>
                <p style="font-size: 16px; color: gray;">
                    Ask me about tenants, rent collection,
                    overdue payments, or vacant rooms.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("#### ✨ Try asking")

        col1, col2 = st.columns(2)

        with col1:
            if st.button(
                "💰  Check rent collection",
                use_container_width=True,
            ):
                st.session_state.ai_selected_question = (
                    "How much rent was collected in October 2026?"
                )

            if st.button(
                "🏠  Find vacant rooms",
                use_container_width=True,
            ):
                st.session_state.ai_selected_question = (
                    "Show me all vacant rooms"
                )

        with col2:
            if st.button(
                "⚠️  Overdue payments",
                use_container_width=True,
            ):
                st.session_state.ai_selected_question = (
                    "Who has overdue payments?"
                )

            if st.button(
                "👥  List all tenants",
                use_container_width=True,
            ):
                st.session_state.ai_selected_question = (
                    "List all tenants"
                )

    # ---------- CHAT HISTORY ----------
    for message in st.session_state.ai_messages:

        with st.chat_message(message["role"]):

            st.markdown(message["content"])

# ----------CHAT INPUT ----------
    typed_question = st.chat_input(
        "Message TenantEase AI...",
        key="tenant_ai_chat_input",
        max_chars=2000,
    )

    # Handle either a typed question or a suggested question.
    question = typed_question

    if not question:
        question = st.session_state.pop(
            "ai_selected_question",
            None,
        )
    else:
        st.session_state.pop(
            "ai_selected_question",
            None,
        )

    # ---------- PROCESS QUESTION ----------
    if question:

        st.session_state.ai_messages.append(
            {
                "role": "user",
                "content": question,
            }
        )

        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):

            with st.spinner(
                "Analyzing your property records..."
            ):
                answer = ask_tenantease_ai(question)

            st.markdown(answer)

        st.session_state.ai_messages.append(
            {
                "role": "assistant",
                "content": answer,
            }
        )

        # Rerun so the conversation displays consistently.
        st.rerun()

    # ---------- FOOTER ----------
    st.divider()

    st.caption(
        "TenantEase AI may use AI-generated responses. "
        "Always verify important financial information "
        "against your database."
    )

    if st.session_state.ai_messages:

        if st.button(
            "🗑️ Clear conversation",
            use_container_width=False,
        ):
            st.session_state.ai_messages = []
            st.session_state.pop(
                "ai_selected_question",
                None,
            )
            st.rerun()
            
elif page == "Rent Reminders":

    st.title("Rent Reminder Center")

    st.write(
        "Review outstanding payments and generate "
        "personalized reminder drafts."
    )

    st.warning(
        "Demo mode: reminders are generated for review only. "
        "No emails or SMS messages will be sent."
    )

    overdue_tenants = get_tenants_needing_reminders()

    if not overdue_tenants:
        st.success("No overdue payments were found.")
    else:
        import pandas as pd

        df = pd.DataFrame(overdue_tenants)

        st.subheader("Outstanding Payments")

        # Display outstanding payment records.
        st.dataframe(
            df[
                [
                    "tenant_name",
                    "property_name",
                    "room_number",
                    "rent_month",
                    "outstanding_amount",
                    "due_date",
                ]
            ],
            use_container_width=True,
            hide_index=True,
        )

        # Get active tenants who have outstanding balances.
        tenants_with_outstanding = (
            get_tenants_with_outstanding_payments()
        )

        tenant_options = {
            f"{tenant['tenant_name']} — Tenant ID {tenant['tenant_id']}":
                tenant["tenant_id"]
            for tenant in tenants_with_outstanding
        }

        if tenant_options:

            # -----------------------------------------
            # RENT REMINDER
            # -----------------------------------------
            st.subheader("Rent Reminder")

            reminder_tenant_label = st.selectbox(
                "Select a tenant for the rent reminder",
                list(tenant_options.keys()),
                key="reminder_tenant_select",
            )

            reminder_tenant_id = tenant_options[
                reminder_tenant_label
            ]

            if st.button(
                "Generate Reminder Draft",
                key="generate_reminder_button",
            ):
                payment_details = generate_reminder_details(
                    reminder_tenant_id
                )

                with st.spinner("Drafting reminder with Gemini..."):
                    reminder = generate_rent_reminder(
                        payment_details
                    )

                st.subheader("Reminder Draft")

                st.text_area(
                    "Review and edit before sending",
                    value=reminder,
                    height=300,
                    key="reminder_draft_text",
                )

                st.caption(
                    "This draft has not been sent to the tenant."
                )

            # -----------------------------------------
            # SETTLE ALL PAYMENTS
            # -----------------------------------------
            st.divider()
            st.subheader("Settle All Payments")

            settlement_tenant_label = st.selectbox(
                "Select a tenant whose payments you want to settle",
                list(tenant_options.keys()),
                key="settlement_tenant_select",
            )

            settlement_tenant_id = tenant_options[
                settlement_tenant_label
            ]

            st.warning(
                "Only settle payments after the tenant has actually paid."
            )

            confirm_settlement = st.checkbox(
                "I confirm that the selected tenant has paid all outstanding rent.",
                key="confirm_settlement",
            )

            if st.button(
                "Settle All Payments",
                key="settle_all_payments_button",
                disabled=not confirm_settlement,
                type="primary",
            ):
                success, message, total_settled = (
                    settle_all_tenant_payments(
                        settlement_tenant_id
                    )
                )

                if success:
                    st.success(message)

                    st.metric(
                        "Amount Settled",
                        f"₹{total_settled:,.2f}",
                    )

                    st.rerun()

                else:
                    st.error(message)

        else:
            st.info(
                "No active tenants with outstanding payments were found."
            )

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "TenantEase AI is an independent proof of concept "
    "using fictional sample data. It is not an official Cynbit integration."
)