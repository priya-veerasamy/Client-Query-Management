import streamlit as st
from login_page import login_page
from client_page import client_query_page
from client_page import client_dashboard_page
from client_page import client_profile_page
from support_page import support_query_page
from support_page import support_dashboard_page
from support_page import support_profile_page

# Initialize session
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    login_page()

else:

    if st.session_state.role == "client":
        page = st.sidebar.radio("Go to", ["Dashboard", "Queries", "Profile"])
        if page == "Queries":
            client_query_page()
        if page == "Dashboard":
            client_dashboard_page()
        if page == "Profile":
            client_profile_page()

    elif st.session_state.role == "support":
        page = st.sidebar.radio("Go to", ["Dashboard", "Queries", "Profile"])
        if page == "Queries":
            support_query_page()
        if page == "Dashboard":
            support_dashboard_page()
        if page == "Profile":
            support_profile_page()

    if st.sidebar.button("Logout"):
        st.session_state.clear()
        st.success("Logged out successfully.")
        login_page()
        st.rerun()
