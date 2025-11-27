import streamlit as st
from db_connection import get_db
from datetime import datetime
import bcrypt
import pandas as pd
import plotly.express as px
import time

def client_query_page():
    st.title('Create a New Query')
    current_email = st.session_state.user['email']
    current_mobile = st.session_state.user['mobile_number']
    email = st.text_input('Email',current_email)
    mobile = st.text_input('Mobile Number',current_mobile)
    category = st.selectbox("Query Category",['Bug Report','Technical Support','Billing Problem',
                                                     'Payment Failure','Account Suspension','Login Issue',
                                                     'Subscription Cancellation','Feature Request',
                                                     'UI Feedback','Data Export'])
    heading = st.text_input('Query Heading')
    description = st.text_area('Query Description')

    if st.button('Submit Query'):
        if not email:
            st.error("Email field is required!")
        if not mobile:
            st.error("Mobile Number field is required!")
        if not category:
            st.error("Query Category is required!")
        if not heading:
            st.error("Query Heading is required!")
        if not description:
            st.error("Query Description is required!")
        else:
            conn, cursor = get_db()
            user_id = st.session_state.user['id']
            cursor.execute("INSERT INTO queries (user_id, email, mobile, category, heading, description, query_created_time) VALUES (%s, %s, %s, %s, %s, %s, %s)""", (user_id, email, mobile, category, heading, description, datetime.now()))
            conn.commit()
            st.success('Query Submitted Successfully!')
            time.sleep(2)
            st.rerun()


def client_dashboard_page():
    st.title("Dashboard")

    user_id = st.session_state.user['id']

    # Fetch only the logged-in client’s queries
    conn, cursor = get_db()
    cursor.execute("SELECT * FROM queries WHERE user_id = %s", (user_id,))
    data = cursor.fetchall()

    if not data:
        st.info("No queries found yet. Create your first query!")
        return

    df = pd.DataFrame(data)

    # Normalize text fields
    df['status'] = df['status'].str.strip().str.lower()
    df['category'] = df['category'].str.strip()

    st.subheader("Your Queries")

    # Filters section
    col1, col2 = st.columns([1, 1])

    with col1:
        status_filter = st.radio(
            "Filter by Status",
            ["All", "Open", "Closed"],
            horizontal=True
        )

    with col2:
        category_filter = st.multiselect(
            "Filter by Category",
            sorted(df['category'].dropna().unique().tolist())
        )

    # Apply status filter
    table_content = df.copy()
    if status_filter == "Open":
        table_content = table_content[table_content['status'] == 'open']
    elif status_filter == "Closed":
        table_content = table_content[table_content['status'] == 'closed']

    # Apply category filter
    if category_filter:
        table_content = table_content[table_content['category'].isin(category_filter)]

    # Display Query table
    st.dataframe(table_content, use_container_width=True)

    # Status count
    st.subheader("Open vs Closed Queries")

    status_count = df['status'].value_counts().reset_index()
    status_count.columns = ['status', 'count']

    fig_status = px.bar(
        status_count,
        x='status',
        y='count',
        title="Open vs Closed Queries",
        text='count',
        template="plotly_white"
    )
    fig_status.update_traces(textposition='outside')
    st.plotly_chart(fig_status, use_container_width=True)

    # Category Distribution
    st.subheader("Category Distribution")

    fig_pie = px.pie(
        df,
        names='category',
        title="Category Share",
        hole=0.4,
        template="plotly_white"
    )
    st.plotly_chart(fig_pie, use_container_width=True)

    # Statistics based on Query Closed time
    df_closed = df[df['status'] == 'closed'].copy()

    if not df_closed.empty:
        df_closed['query_created_time'] = pd.to_datetime(df_closed['query_created_time'])
        df_closed['query_closed_time'] = pd.to_datetime(df_closed['query_closed_time'])
        df_closed['time_taken'] = df_closed['query_closed_time'] - df_closed['query_created_time']

        # Calculate statistics
        max_time = df_closed['time_taken'].max().total_seconds()
        min_time = df_closed['time_taken'].min().total_seconds()
        avg_time = df_closed['time_taken'].mean().total_seconds()

        stats_df = pd.DataFrame({
            'Metric': ['Highest', 'Lowest', 'Average'],
            'Seconds': [max_time, min_time, avg_time]
        })

        fig_time = px.bar(
            stats_df,
            x='Metric',
            y='Seconds',
            title="Query Resolution Time (Seconds)",
            text='Seconds',
            template="plotly_white"
        )
        fig_time.update_traces(textposition='outside')
        st.plotly_chart(fig_time, use_container_width=True)

        # Display Average Time
        avg_time_text = str(pd.to_timedelta(avg_time, unit='s'))
        st.success(f" **Average Time to Resolve Query: {avg_time_text}**")

    else:
        st.info("No closed queries yet to calculate time taken.")

    conn.close()


def client_profile_page():
    st.title('Your Profile')

    conn, cursor = get_db()

    user_id = st.session_state.user['id']

    if not user_id:
        st.warning("Please login to view profile.")
        return

    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()

    if not user:
        st.error("User not found!")
        return
    
    # pre-filled fields
    name = st.text_input("Name", user['username'])
    email = st.text_input("Email", user['email'])
    phone = st.text_input("Mobile Number", user['mobile_number'])
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    if st.button("Update Profile"):

        if not name or not email or not phone:
            st.error("Name, Email and Mobile Number fields are required!")
            return

        if password or confirm_password:
            if password != confirm_password:
                st.error("Passwords do not match!")
                return
            else:
                hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
                
                cursor.execute("""
                    UPDATE users SET username = %s, email = %s, mobile_number = %s, hashed_password = %s WHERE id = %s
                """, (name, email, phone, hashed_password, user_id))
        else:
            cursor.execute("""
                UPDATE users SET username = %s, email = %s, mobile_number = %s WHERE id = %s
            """, (name, email, phone, user_id))

        conn.commit()
        conn.close()
        st.success("Profile Updated Successfully ✔")
        time.sleep(2)
        st.rerun()
