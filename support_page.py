import streamlit as st
import pandas as pd
from db_connection import get_db
from datetime import datetime
import bcrypt
import pandas as pd
import plotly.express as px
import time

def support_query_page():
    st.title("Submitted Queries")

    # --- Fetch data ---
    conn, cursor = get_db()
    cursor.execute("SELECT * FROM queries")
    data = cursor.fetchall()

    if not data:
        st.warning("⚠ No queries found in the database!")
        return

    df = pd.DataFrame(data)

    # Convert datetime fields
    for col in ['query_created_time', 'query_closed_time']:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col])

    # --- Filters ---
    col1, col2 = st.columns([1, 1])
    with col1:
        status_filter = st.radio("Select Status", ["All", "Open", "Closed"], horizontal=True)
    with col2:
        category_options = df['category'].dropna().unique().tolist()
        selected_category = st.multiselect("Filter by Category", category_options)

    # Apply filters
    filtered_df = df.copy()
    if status_filter != "All":
        filtered_df = filtered_df[filtered_df['status'].str.lower() == status_filter.lower()]
    if selected_category:
        filtered_df = filtered_df[filtered_df['category'].isin(selected_category)]

    st.subheader("Query List")
    st.dataframe(filtered_df, use_container_width=True)

    # --- Select a query to view details ---
    st.subheader("View / Update Query")
    if filtered_df.empty:
        st.info("No queries available to select.")
        return

    # Add placeholder option
    options = ["-- Select a Query --"] + filtered_df['id'].tolist()
    selected_id = st.selectbox("Select a Query by ID", options)

    if selected_id != "-- Select a Query --":
        query_row = filtered_df[filtered_df['id'] == selected_id].iloc[0]

        # Display query details
        st.markdown("**Query Details:**")
        st.markdown(f"**ID:** {query_row['id']}")
        st.markdown(f"**Status:** {query_row['status']}")
        st.markdown(f"**Category:** {query_row.get('category', 'N/A')}")
        st.markdown(f"**Heading:** {query_row.get('heading', 'N/A')}")
        st.markdown(f"**Description:** {query_row.get('description', 'N/A')}")
        st.markdown(f"**Created Time:** {query_row.get('query_created_time', 'N/A')}")
        st.markdown(f"**Closed Time:** {query_row.get('query_closed_time', 'N/A')}")


        # --- Close / Reopen button based on current status ---
        if query_row['status'].lower() == 'open':
            if st.button("Close Query"):
                cursor.execute(
                    "UPDATE queries SET status=%s, query_closed_time=%s WHERE id=%s",
                    ("Closed", datetime.now(), selected_id)
                )
                conn.commit()
                st.success(f"Query {selected_id} Closed ✔")
                time.sleep(2)
                st.rerun()
        else:
            if st.button("Reopen Query"):
                cursor.execute(
                    "UPDATE queries SET status=%s, query_created_time=%s, query_closed_time=%s WHERE id=%s",
                    ("Open", datetime.now(), None, selected_id)
                )
                conn.commit()
                st.success(f"Query {selected_id} Reopened ✔")
                time.sleep(2)
                st.rerun()



def support_dashboard_page():
    st.title("Support Dashboard")

    # Fetch all queries
    conn, cursor = get_db()
    cursor.execute("SELECT * FROM queries")
    data = cursor.fetchall()

    if not data:
        st.info("No queries found yet.")
        return

    df = pd.DataFrame(data)

    # Normalize columns
    df['status'] = df['status'].str.strip().str.lower()
    df['category'] = df['category'].str.strip()

    st.subheader("Submitted Queries")

    # Filters
    table_content = df.copy()
    col1, col2 = st.columns([1, 1])

    with col1:
        opened = st.checkbox("Show Opened Queries")
    with col2:
        closed = st.checkbox("Show Closed Queries")

    category = st.multiselect("Filter by Category", sorted(df['category'].unique()))

    # Status filter
    if opened and not closed:
        table_content = table_content[table_content['status'] == 'open']
    elif closed and not opened:
        table_content = table_content[table_content['status'] == 'closed']

    # Category filter
    if category:
        table_content = table_content[table_content['category'].isin(category)]

    st.dataframe(table_content, use_container_width=True)

    # Statistics
    st.subheader("Open vs Closed Queries")
    status_count = df['status'].value_counts().reset_index()
    status_count.columns = ['status', 'count']

    fig_status = px.bar(
        status_count,
        x='status',
        y='count',
        text='count',
        title="Open vs Closed Queries",
        template="plotly_white"
    )
    fig_status.update_traces(textposition='outside')
    st.plotly_chart(fig_status, use_container_width=True)

    # statistics based one time 
    df_closed = df[df['status'] == 'closed'].copy()

    if not df_closed.empty:
        df_closed['query_created_time'] = pd.to_datetime(df_closed['query_created_time'])
        df_closed['query_closed_time'] = pd.to_datetime(df_closed['query_closed_time'])
        df_closed['time_taken'] = df_closed['query_closed_time'] - df_closed['query_created_time']
        df_closed['seconds'] = df_closed['time_taken'].dt.total_seconds()

        # Max / Min / Avg Time Chart
        max_time = df_closed['seconds'].max()
        min_time = df_closed['seconds'].min()
        avg_time = df_closed['seconds'].mean()

        stats_df = pd.DataFrame({
            'Metric': ['Highest', 'Lowest', 'Average'],
            'Seconds': [max_time, min_time, avg_time]
        })

        fig_time = px.bar(
            stats_df,
            x='Metric',
            y='Seconds',
            text='Seconds',
            title="Query Resolution Time (Seconds)",
            template="plotly_white"
        )
        fig_time.update_traces(textposition='outside')
        st.plotly_chart(fig_time, use_container_width=True)

        # Average time text
        avg_time_text = str(pd.to_timedelta(avg_time, unit='s'))
        st.success(f" **Average Time to Resolve Query: {avg_time_text}**")

        # Time taken for each Query closed
        st.subheader("Time Taken Per Closed Query")
        df_closed_sorted = df_closed.sort_values("query_closed_time")

        fig_line = px.line(
            df_closed_sorted,
            x="query_closed_time",
            y="seconds",
            markers=True,
            title="Time Taken Per Closed Query",
            template="plotly_white"
        )
        st.plotly_chart(fig_line, use_container_width=True)

        # Average time for category
        st.subheader("Average Time by Category")
        cat_time_df = df_closed.groupby('category')['seconds'].mean().reset_index()
        cat_time_df['seconds'] = cat_time_df['seconds'].round(2)

        fig_cat = px.bar(
            cat_time_df,
            x='category',
            y='seconds',
            text='seconds',
            title="Average Resolution Time by Category",
            template="plotly_white"
        )
        fig_cat.update_traces(textposition='outside')
        st.plotly_chart(fig_cat, use_container_width=True)

    # Pending queries for last 24 hours
    st.subheader("Pending Queries Over 24 Hours")
    df['query_created_time'] = pd.to_datetime(df['query_created_time'])
    df['pending_time'] = datetime.now() - df['query_created_time']

    pending_queries = df[(df['status'] == 'open') & (df['pending_time'] > pd.Timedelta(hours=24))]

    if not pending_queries.empty:
        st.dataframe(pending_queries[['id', 'heading', 'category', 'pending_time']], use_container_width=True)
    else:
        st.success("No long pending queries – Great job! ")

    conn.close()


def support_profile_page():
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
