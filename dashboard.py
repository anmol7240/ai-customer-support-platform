
import streamlit as st
import requests
import pandas as pd

st.set_page_config(
    page_title="Customer Support Dashboard",
    page_icon="🎫",
    layout="wide"
)

st.title("🎫 AI Customer Support Dashboard")

API_URL = "http://127.0.0.1:8000"

# Analytics API
try:
    response = requests.get(
        f"{API_URL}/analytics/tickets"
    )

    if response.status_code == 200:
        analytics = response.json()

        col1, col2, col3, col4 = st.columns(4)

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

    else:
        st.error("Analytics API failed")

except requests.exceptions.ConnectionError:
    st.error(
        "FastAPI server is not running. "
        "Start the backend first."
    )

# All tickets
st.subheader("📋 All Support Tickets")

try:
    response = requests.get(
        f"{API_URL}/tickets"
    )

    if response.status_code == 200:
        tickets = response.json()

        if tickets:
            df = pd.DataFrame(tickets)

            # Status Filter
            status_options = ["ALL"] + sorted(
                df["status"].dropna().unique().tolist()
            )

            selected_status = st.selectbox(
                "Filter by Status",
                status_options
            )

            if selected_status != "ALL":
                filtered_df = df[
                    df["status"] == selected_status
                ]
            else:
                filtered_df = df

            # Priority Filter
            priority_options = ["ALL"] + sorted(
                df["priority"].dropna().unique().tolist()
            )

            selected_priority = st.selectbox(
                "Filter by Priority",
                priority_options
            )

            if selected_priority != "ALL":
                filtered_df = filtered_df[
                    filtered_df["priority"] == selected_priority
                ]

            # Average Customer Rating
            if "customer_rating" in filtered_df.columns:
                # Charts
                st.subheader("📊 Ticket Analytics")

                chart_col1, chart_col2 = st.columns(2)

                with chart_col1:
                    st.write("Priority Distribution")

                    priority_counts = (
                        filtered_df["priority"]
                        .value_counts()
                    )

                    st.bar_chart(priority_counts)

                with chart_col2:
                    st.write("Status Distribution")

                    status_counts = (
                        filtered_df["status"]
                        .value_counts()
                    )

                    st.bar_chart(status_counts)
                ratings = filtered_df["customer_rating"].dropna()

                if not ratings.empty:
                    st.metric(
                        "Average Customer Rating",
                        round(ratings.mean(), 2)
                    )

            st.dataframe(
                filtered_df,
                use_container_width=True
            )

        else:
            st.info("No tickets available")

    else:
        st.error("Tickets API failed")

except requests.exceptions.ConnectionError:
    st.error("Cannot connect to FastAPI")
    st.subheader("🎫 Create New Support Ticket")

customer_id = st.number_input(
    "Customer ID",
    min_value=1,
    step=1
)

message = st.text_area(
    "Customer Message",
    placeholder="Example: My payment failed and money was deducted."
)

if st.button("Create Ticket"):

    if not message.strip():
        st.warning("Please enter a ticket message.")

    else:
        ticket_data = {
            "message": message,
            "customer_id": customer_id
        }

        try:
            response = requests.post(
                f"{API_URL}/tickets",
                json=ticket_data
            )

            if response.status_code == 200:
                ticket = response.json()

                st.success("Ticket created successfully!")

                st.write("### 🤖 AI Analysis")

                col1, col2, col3 = st.columns(3)

                col1.metric(
                    "Category",
                    ticket["category"]
                )

                col2.metric(
                    "Priority",
                    ticket["priority"]
                )

                col3.metric(
                    "Status",
                    ticket["status"]
                )

            else:
                st.error(
                    f"Error: {response.json()}"
                )

        except requests.exceptions.ConnectionError:
            st.error(
                "FastAPI server is not running."
            )

st.subheader("🔄 Update Ticket Status")

with st.form("status_form"):
    ticket_id = st.number_input(
        "Ticket ID",
        min_value=1,
        step=1
    )

    new_status = st.selectbox(
        "Select New Status",
        [
            "OPEN",
            "IN_PROGRESS",
            "RESOLVED",
            "CLOSED"
        ]
    )

    resolution_notes = st.text_area(
        "Resolution Notes",
        placeholder="Explain how the issue was resolved..."
    )

    customer_rating = st.slider(
        "Customer Rating",
        min_value=1,
        max_value=5,
        value=5
    )

    customer_feedback = st.text_area(
        "Customer Feedback",
        placeholder="Write customer feedback..."
    )

    update_submitted = st.form_submit_button(
        "Update Status"
    )

    if update_submitted:
        update_data = {
            "status": new_status,
            "resolution_notes": resolution_notes,
            "customer_rating": customer_rating,
            "customer_feedback": customer_feedback
        }

        response = requests.put(
            f"{API_URL}/tickets/{int(ticket_id)}",
            json=update_data
        )

        if response.status_code == 200:
            updated_ticket = response.json()

            st.success(
                "Ticket status updated successfully!"
            )

            st.write(
                "Ticket ID:",
                updated_ticket["id"]
            )

            st.write(
                "New Status:",
                updated_ticket["status"]
            )

        else:
            st.error(
                f"Error: {response.text}"
            )