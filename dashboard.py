import streamlit as st
import requests
import pandas as pd

# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="AI Customer Support",
    page_icon="🎫",
    layout="wide"
)

API_URL = "https://ai-customer-support-platform-tr6k.onrender.com"


# ==================================================
# SESSION STATE
# ==================================================

if "token" not in st.session_state:
    st.session_state.token = None

if "role" not in st.session_state:
    st.session_state.role = None

if "user_id" not in st.session_state:
    st.session_state.user_id = None

if "customer_id" not in st.session_state:
    st.session_state.customer_id = None

if "agent_id" not in st.session_state:
    st.session_state.agent_id = None

if "login_email" not in st.session_state:
    st.session_state.login_email = None


# ==================================================
# HELPER FUNCTIONS
# ==================================================

def auth_headers():
    return {
        "Authorization": f"Bearer {st.session_state.token}"
    }


def api_error(response):
    try:
        data = response.json()
        return data.get("detail", data)
    except Exception:
        return response.text


def logout():
    st.session_state.token = None
    st.session_state.role = None
    st.session_state.user_id = None
    st.session_state.customer_id = None
    st.session_state.agent_id = None
    st.session_state.login_email = None
    st.rerun()


# ==================================================
# LOGIN / SIGN UP PAGE
# ==================================================

if not st.session_state.token:

    st.title("🎫 AI Customer Support Intelligence Platform")

    login_tab, signup_tab = st.tabs(
        ["🔐 Login", "📝 Sign Up"]
    )

    # ==================================================
    # LOGIN
    # ==================================================

    with login_tab:

        st.subheader("Login")

        with st.form("login_form"):

            email = st.text_input(
                "Email",
                placeholder="Enter your email",
                key="login_email_input"
            )

            password = st.text_input(
                "Password",
                type="password",
                placeholder="Enter your password",
                key="login_password_input"
            )

            login_button = st.form_submit_button(
                "Login",
                type="primary",
                use_container_width=True
            )

        if login_button:

            if not email or not password:

                st.warning(
                    "Please enter email and password."
                )

            else:

                try:

                    response = requests.post(
                        f"{API_URL}/auth/login",
                        json={
                            "email": email,
                            "password": password
                        },
                        timeout=10
                    )

                    if response.status_code == 200:

                        data = response.json()

                        st.session_state.token = data["access_token"]
                        st.session_state.role = data["role"]
                        st.session_state.user_id = data["user_id"]
                        st.session_state.customer_id = data.get(
                            "customer_id"
                        )
                        st.session_state.agent_id = data.get(
                            "agent_id"
                        )
                        st.session_state.login_email = email

                        st.success(
                            "Login successful!"
                        )

                        st.rerun()

                    else:

                        st.error(
                            f"Login failed: {api_error(response)}"
                        )

                except requests.exceptions.ConnectionError:

                    st.error(
                        "FastAPI server is not running. "
                        "Start the backend first."
                    )

                except requests.exceptions.RequestException as e:

                    st.error(
                        f"Request error: {e}"
                    )

    # ==================================================
    # CUSTOMER SIGN UP
    # ==================================================

    with signup_tab:

        st.subheader("Create Customer Account")

        st.info(
            "New users can create a Customer account here."
        )

        with st.form("signup_form"):

            signup_name = st.text_input(
                "Full Name",
                placeholder="Enter your name"
            )

            signup_email = st.text_input(
                "Email",
                placeholder="Enter your email",
                key="signup_email"
            )

            signup_password = st.text_input(
                "Password",
                type="password",
                placeholder="Create a password",
                key="signup_password"
            )

            signup_confirm_password = st.text_input(
                "Confirm Password",
                type="password",
                placeholder="Re-enter your password"
            )

            signup_button = st.form_submit_button(
                "Create Customer Account",
                type="primary",
                use_container_width=True
            )

        if signup_button:

            if not signup_name.strip():
                st.warning("Please enter your name.")

            elif not signup_email.strip():
                st.warning("Please enter your email.")

            elif not signup_password:
                st.warning("Please enter a password.")

            elif signup_password != signup_confirm_password:
                st.error(
                    "Password and Confirm Password do not match."
                )

            elif len(signup_password) < 6:
                st.warning(
                    "Password must be at least 6 characters."
                )

            else:

                try:

                    response = requests.post(
                        f"{API_URL}/auth/register",
                        params={
                            "name": signup_name.strip(),
                            "email": signup_email.strip(),
                            "password": signup_password
                        },
                        timeout=10
                    )

                    if response.status_code == 200:

                        data = response.json()

                        st.success(
                            "Customer account created successfully!"
                        )

                        st.info(
                            "Please open the Login tab and "
                            "login with your new account."
                        )

                        st.write(
                            f"**Customer ID:** "
                            f"{data.get('customer_id')}"
                        )

                    else:

                        st.error(
                            f"Registration failed: "
                            f"{api_error(response)}"
                        )

                except requests.exceptions.ConnectionError:

                    st.error(
                        "FastAPI server is not running. "
                        "Start the backend first."
                    )

                except requests.exceptions.RequestException as e:

                    st.error(
                        f"Request error: {e}"
                    )

    st.stop()


# ==================================================
# SIDEBAR
# ==================================================

st.sidebar.title("🎫 Customer Support")

st.sidebar.write(
    f"**Logged in as:** {st.session_state.login_email}"
)

st.sidebar.write(
    f"**Role:** {st.session_state.role.upper()}"
)

if st.sidebar.button(
    "🚪 Logout",
    use_container_width=True
):
    logout()


# ==================================================
# CUSTOMER DASHBOARD
# ==================================================

if st.session_state.role == "customer":

    st.title("👤 Customer Dashboard")

    # ==================================================
    # CREATE NEW TICKET
    # ==================================================

    st.subheader("🎫 Create New Support Ticket")

    # --------------------------------------------------
    # LOAD CATEGORIES
    # --------------------------------------------------

    try:

        category_df = pd.read_csv(
            "data/tickets.csv"
        )

        ticket_categories = sorted(
            category_df["category"]
            .dropna()
            .unique()
            .tolist()
        )

    except Exception:

        ticket_categories = [
            "Account",
            "Payment",
            "Technical",
            "Delivery",
            "Refund",
            "Security",
            "Subscription",
            "Other"
        ]

    selected_category = st.selectbox(
        "Select Ticket Type",
        ticket_categories
    )

    # --------------------------------------------------
    # CUSTOMER MESSAGE TEMPLATES
    # --------------------------------------------------

    message_templates = {

        "payment": [
            "My payment failed but money was deducted.",
            "My payment was deducted but my order is still pending.",
            "I was charged twice for the same transaction.",
            "My refund has not been received yet.",
            "The payment is showing as failed."
        ],

        "account": [
            "I cannot login to my account.",
            "I forgot my account password.",
            "My account is locked.",
            "I want to update my account information.",
            "I cannot access my account."
        ],

        "technical": [
            "The application is not working properly.",
            "The website is showing an error.",
            "I am unable to use the application.",
            "The system is very slow.",
            "The application keeps crashing."
        ],

        "delivery": [
            "My order has not been delivered yet.",
            "My delivery is delayed.",
            "I received the wrong product.",
            "My order was marked delivered but I did not receive it.",
            "I want to know the status of my delivery."
        ],

        "refund": [
            "I have not received my refund.",
            "Please check the status of my refund.",
            "My refund amount is incorrect.",
            "I want to request a refund.",
            "When will I receive my refund?"
        ],

        "security": [
            "I think someone accessed my account.",
            "My account may have been hacked.",
            "I noticed a suspicious transaction.",
            "I want to report unauthorized activity.",
            "There is suspicious activity on my account."
        ],

        "subscription": [
            "I want to cancel my subscription.",
            "I was charged for my subscription.",
            "My subscription is not working.",
            "I want to change my subscription plan.",
            "I want information about my subscription."
        ],

        "other": [
            "I need help with my account.",
            "I have a general question.",
            "I need assistance with my issue.",
            "I want to contact customer support.",
            "I need help regarding my problem."
        ]
    }

    category_key = str(
        selected_category
    ).strip().lower()

    available_messages = message_templates.get(
        category_key,
        message_templates["other"]
    )

    selected_message = st.selectbox(
        "Select Customer Message",
        available_messages
    )

    st.info(
        f"Selected message: {selected_message}"
    )

    if st.button(
        "🚀 Create Ticket",
        type="primary"
    ):

        ticket_data = {
            "message": selected_message,
            "customer_id": st.session_state.customer_id
        }

        try:

            response = requests.post(
                f"{API_URL}/tickets",
                json=ticket_data,
                headers=auth_headers(),
                timeout=10
            )

            if response.status_code == 200:

                ticket = response.json()

                st.success(
                    "Ticket created successfully!"
                )

                st.write("### 🤖 AI Analysis")

                col1, col2, col3 = st.columns(3)

                col1.metric(
                    "AI Category",
                    ticket.get("category", "N/A")
                )

                col2.metric(
                    "Priority",
                    ticket.get("priority", "N/A")
                )

                col3.metric(
                    "Status",
                    ticket.get("status", "OPEN")
                )

                st.write("### 📝 Customer Message")

                st.info(ticket["message"])

                st.write(
                    f"**Ticket ID:** {ticket['id']}"
                )

            else:

                st.error(
                    f"Error: {api_error(response)}"
                )

        except requests.exceptions.ConnectionError:

            st.error(
                "FastAPI server is not running."
            )

        except requests.exceptions.RequestException as e:

            st.error(f"Request error: {e}")


    # ==================================================
    # MY TICKETS
    # ==================================================

    st.divider()

    st.subheader("📋 My Tickets")

    try:

        response = requests.get(
            f"{API_URL}/tickets",
            headers=auth_headers(),
            timeout=10
        )

        if response.status_code == 200:

            tickets = response.json()

            if tickets:

                df = pd.DataFrame(tickets)

                st.dataframe(
                    df,
                    use_container_width=True
                )

                # ------------------------------------------
                # TICKET DETAILS
                # ------------------------------------------

                ticket_ids = [
                    ticket["id"]
                    for ticket in tickets
                ]

                selected_ticket_id = st.selectbox(
                    "Select Ticket",
                    ticket_ids,
                    key="customer_ticket_select"
                )

                selected_ticket = next(
                    (
                        ticket
                        for ticket in tickets
                        if ticket["id"] == selected_ticket_id
                    ),
                    None
                )

                if selected_ticket:

                    col1, col2, col3 = st.columns(3)

                    col1.metric(
                        "Status",
                        selected_ticket["status"]
                    )

                    col2.metric(
                        "Priority",
                        selected_ticket.get(
                            "priority",
                            "N/A"
                        )
                    )

                    col3.metric(
                        "Agent ID",
                        selected_ticket.get(
                            "agent_id",
                            "Not assigned"
                        )
                    )

                    st.write("**Message:**")
                    st.info(
                        selected_ticket["message"]
                    )

                    if selected_ticket.get(
                        "resolution_notes"
                    ):
                        st.write(
                            "**Resolution:**"
                        )
                        st.success(
                            selected_ticket[
                                "resolution_notes"
                            ]
                        )

                    # ------------------------------------------
                    # CUSTOMER FEEDBACK
                    # ------------------------------------------

                    if selected_ticket["status"] == "RESOLVED":

                        st.write(
                            "### ⭐ Rate Your Support Experience"
                        )

                        with st.form(
                            f"feedback_form_{selected_ticket_id}"
                        ):

                            rating = st.slider(
                                "Customer Rating",
                                min_value=1,
                                max_value=5,
                                value=5
                            )

                            feedback = st.text_area(
                                "Customer Feedback",
                                placeholder=(
                                    "Tell us about your support experience..."
                                )
                            )

                            submit_feedback = (
                                st.form_submit_button(
                                    "Submit Feedback",
                                    type="primary"
                                )
                            )

                        if submit_feedback:

                            if not feedback.strip():

                                st.warning(
                                    "Please enter feedback."
                                )

                            else:

                                feedback_data = {
                                    "customer_rating": rating,
                                    "customer_feedback": feedback
                                }

                                try:

                                    feedback_response = (
                                        requests.put(
                                            f"{API_URL}/tickets/"
                                            f"{selected_ticket_id}/feedback",
                                            json=feedback_data,
                                            headers=auth_headers(),
                                            timeout=10
                                        )
                                    )

                                    if (
                                        feedback_response.status_code
                                        == 200
                                    ):

                                        st.success(
                                            "Feedback submitted successfully!"
                                        )

                                        st.rerun()

                                    else:

                                        st.error(
                                            f"Error: "
                                            f"{api_error(feedback_response)}"
                                        )

                                except requests.exceptions.RequestException as e:

                                    st.error(
                                        f"Request error: {e}"
                                    )

            else:

                st.info(
                    "You do not have any tickets yet."
                )

        else:

            st.error(
                f"Tickets API failed: {api_error(response)}"
            )

    except requests.exceptions.ConnectionError:

        st.error(
            "Cannot connect to FastAPI."
        )

    except requests.exceptions.RequestException as e:

        st.error(
            f"Request error: {e}"
        )


# ==================================================
# AGENT DASHBOARD
# ==================================================

elif st.session_state.role == "agent":

    st.title("👨‍💼 Agent Dashboard")

    # ==================================================
    # ANALYTICS
    # ==================================================

    st.subheader("📊 Support Analytics")

    try:

        response = requests.get(
            f"{API_URL}/analytics/tickets",
            headers=auth_headers(),
            timeout=10
        )

        if response.status_code == 200:

            analytics = response.json()

            col1, col2, col3, col4, col5 = st.columns(5)

            col1.metric(
                "Total Tickets",
                analytics["total_tickets"]
            )

            col2.metric(
                "High Priority",
                analytics["high_priority_tickets"]
            )

            col3.metric(
                "Critical Priority",
                analytics["critical_priority_tickets"]
            )

            col4.metric(
                "Open Tickets",
                analytics["open_tickets"]
            )

            col5.metric(
                "Resolved Tickets",
                analytics["resolved_tickets"]
            )

        else:

            st.error(
                f"Analytics API failed: "
                f"{api_error(response)}"
            )

    except requests.exceptions.ConnectionError:

        st.error(
            "FastAPI server is not running."
        )

    except requests.exceptions.RequestException as e:

        st.error(
            f"Request error: {e}"
        )


    # ==================================================
    # ALL SUPPORT TICKETS
    # ==================================================

    st.divider()

    st.subheader("📋 All Support Tickets")

    try:

        response = requests.get(
            f"{API_URL}/tickets",
            headers=auth_headers(),
            timeout=10
        )

        if response.status_code == 200:

            tickets = response.json()

            if tickets:

                df = pd.DataFrame(tickets)

                # ------------------------------------------
                # FILTERS
                # ------------------------------------------

                filter_col1, filter_col2 = st.columns(2)

                with filter_col1:

                    status_options = [
                        "ALL"
                    ] + sorted(
                        df["status"]
                        .dropna()
                        .unique()
                        .tolist()
                    )

                    selected_status = st.selectbox(
                        "Filter by Status",
                        status_options,
                        key="agent_status_filter"
                    )

                with filter_col2:

                    priority_options = [
                        "ALL"
                    ] + sorted(
                        df["priority"]
                        .dropna()
                        .unique()
                        .tolist()
                    )

                    selected_priority = st.selectbox(
                        "Filter by Priority",
                        priority_options,
                        key="agent_priority_filter"
                    )

                filtered_df = df.copy()

                if selected_status != "ALL":

                    filtered_df = filtered_df[
                        filtered_df["status"]
                        == selected_status
                    ]

                if selected_priority != "ALL":

                    filtered_df = filtered_df[
                        filtered_df["priority"]
                        == selected_priority
                    ]

                # ------------------------------------------
                # AVERAGE RATING
                # ------------------------------------------

                if "customer_rating" in filtered_df.columns:

                    ratings = (
                        filtered_df["customer_rating"]
                        .dropna()
                    )

                    if not ratings.empty:

                        st.metric(
                            "Average Customer Rating",
                            round(ratings.mean(), 2)
                        )

                # ------------------------------------------
                # CHARTS
                # ------------------------------------------

                chart_col1, chart_col2 = st.columns(2)

                with chart_col1:

                    st.write(
                        "### Priority Distribution"
                    )

                    priority_counts = (
                        filtered_df["priority"]
                        .value_counts()
                    )

                    st.bar_chart(
                        priority_counts
                    )

                with chart_col2:

                    st.write(
                        "### Status Distribution"
                    )

                    status_counts = (
                        filtered_df["status"]
                        .value_counts()
                    )

                    st.bar_chart(
                        status_counts
                    )

                # ------------------------------------------
                # TABLE
                # ------------------------------------------

                st.dataframe(
                    filtered_df,
                    use_container_width=True
                )

                # ==================================================
                # SELECT TICKET
                # ==================================================

                st.divider()

                st.subheader(
                    "🎯 Manage Ticket"
                )

                ticket_ids = (
                    filtered_df["id"]
                    .tolist()
                )

                if ticket_ids:

                    selected_ticket_id = st.selectbox(
                        "Select Ticket ID",
                        ticket_ids,
                        key="agent_ticket_select"
                    )

                    selected_ticket = next(
                        (
                            ticket
                            for ticket in tickets
                            if ticket["id"]
                            == selected_ticket_id
                        ),
                        None
                    )

                    if selected_ticket:

                        # ------------------------------------------
                        # TICKET INFORMATION
                        # ------------------------------------------

                        info_col1, info_col2, info_col3, info_col4 = (
                            st.columns(4)
                        )

                        info_col1.metric(
                            "Ticket ID",
                            selected_ticket["id"]
                        )

                        info_col2.metric(
                            "Priority",
                            selected_ticket.get(
                                "priority",
                                "N/A"
                            )
                        )

                        info_col3.metric(
                            "Status",
                            selected_ticket["status"]
                        )

                        info_col4.metric(
                            "Agent ID",
                            selected_ticket.get(
                                "agent_id",
                                "Not assigned"
                            )
                        )

                        st.write(
                            "**Customer Message:**"
                        )

                        st.info(
                            selected_ticket["message"]
                        )

                        # ==================================================
                        # ASSIGN TICKET
                        # ==================================================

                        st.write(
                            "### 👨‍💼 Assign Ticket"
                        )

                        try:

                            agents_response = requests.get(
                                f"{API_URL}/agents",
                                headers=auth_headers(),
                                timeout=10
                            )

                            if agents_response.status_code == 200:

                                agents = agents_response.json()

                                if agents:

                                    agent_options = {
                                        f"{agent['name']} "
                                        f"({agent['email']})":
                                        agent["id"]
                                        for agent in agents
                                    }

                                    selected_agent_name = (
                                        st.selectbox(
                                            "Select Agent",
                                            list(
                                                agent_options.keys()
                                            ),
                                            key="assign_agent"
                                        )
                                    )

                                    if st.button(
                                        "👨‍💼 Assign Ticket",
                                        key="assign_ticket_button"
                                    ):

                                        agent_id = agent_options[
                                            selected_agent_name
                                        ]

                                        assign_response = requests.put(
                                            f"{API_URL}/tickets/"
                                            f"{selected_ticket_id}/assign",
                                            json={
                                                "agent_id": agent_id
                                            },
                                            headers=auth_headers(),
                                            timeout=10
                                        )

                                        if (
                                            assign_response.status_code
                                            == 200
                                        ):

                                            st.success(
                                                "Ticket assigned successfully!"
                                            )

                                            st.rerun()

                                        else:

                                            st.error(
                                                f"Error: "
                                                f"{api_error(assign_response)}"
                                            )

                                else:

                                    st.warning(
                                        "No agents available."
                                    )

                            else:

                                st.error(
                                    f"Unable to load agents: "
                                    f"{api_error(agents_response)}"
                                )

                        except requests.exceptions.RequestException as e:

                            st.error(
                                f"Request error: {e}"
                            )

                        # ==================================================
                        # UPDATE / RESOLVE TICKET
                        # ==================================================

                        st.write(
                            "### 🔄 Update Ticket"
                        )

                        with st.form(
                            f"update_ticket_form_{selected_ticket_id}"
                        ):

                            new_status = st.selectbox(
                                "Status",
                                [
                                    "OPEN",
                                    "IN_PROGRESS",
                                    "RESOLVED"
                                ],
                                index=[
                                    "OPEN",
                                    "IN_PROGRESS",
                                    "RESOLVED"
                                ].index(
                                    selected_ticket["status"]
                                    if selected_ticket["status"]
                                    in [
                                        "OPEN",
                                        "IN_PROGRESS",
                                        "RESOLVED"
                                    ]
                                    else "OPEN"
                                )
                            )

                            new_priority = st.selectbox(
                                "Priority",
                                [
                                    "LOW",
                                    "MEDIUM",
                                    "HIGH",
                                    "CRITICAL"
                                ],
                                index=[
                                    "LOW",
                                    "MEDIUM",
                                    "HIGH",
                                    "CRITICAL"
                                ].index(
                                    selected_ticket.get(
                                        "priority",
                                        "MEDIUM"
                                    )
                                    if selected_ticket.get(
                                        "priority",
                                        "MEDIUM"
                                    ) in [
                                        "LOW",
                                        "MEDIUM",
                                        "HIGH",
                                        "CRITICAL"
                                    ]
                                    else "MEDIUM"
                                )
                            )

                            resolution_notes = st.text_area(
                                "Resolution Notes",
                                value=(
                                    selected_ticket.get(
                                        "resolution_notes"
                                    )
                                    or ""
                                ),
                                placeholder=(
                                    "Explain how the issue was resolved..."
                                )
                            )

                            update_ticket_button = (
                                st.form_submit_button(
                                    "💾 Update Ticket",
                                    type="primary"
                                )
                            )

                        if update_ticket_button:

                            update_data = {
                                "status": new_status,
                                "priority": new_priority,
                                "resolution_notes": resolution_notes
                            }

                            try:

                                update_response = requests.put(
                                    f"{API_URL}/tickets/"
                                    f"{selected_ticket_id}",
                                    json=update_data,
                                    headers=auth_headers(),
                                    timeout=10
                                )

                                if (
                                    update_response.status_code
                                    == 200
                                ):

                                    st.success(
                                        "Ticket updated successfully!"
                                    )

                                    st.rerun()

                                else:

                                    st.error(
                                        f"Error: "
                                        f"{api_error(update_response)}"
                                    )

                            except requests.exceptions.RequestException as e:

                                st.error(
                                    f"Request error: {e}"
                                )

            else:

                st.info(
                    "No tickets available."
                )

        else:

            st.error(
                f"Tickets API failed: "
                f"{api_error(response)}"
            )

    except requests.exceptions.ConnectionError:

        st.error(
            "Cannot connect to FastAPI."
        )

    except requests.exceptions.RequestException as e:

        st.error(
            f"Request error: {e}"
        )


# ==================================================
# INVALID ROLE
# ==================================================

else:

    st.error(
        "Invalid user role."
    )
