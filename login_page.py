import streamlit as st
import bcrypt
from db_connection import get_db

def login_page():
    st.title("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        conn, cursor = get_db()
        cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
        user = cursor.fetchone()

        if user and bcrypt.checkpw(password.encode(), user['hashed_password'].encode()):
            st.session_state.logged_in = True
            st.session_state.user = user
            st.session_state.role = user['role']

            if user['role'].lower() == "client":
                st.session_state.page = "client"
                st.rerun()
            elif user['role'].lower() == "support":
                st.session_state.page = "support"
                st.rerun()
        else:
            st.error("Invalid username or password.")

    if "logged_in" in st.session_state:
        if st.session_state.logged_in:
            if st.button("Logout"):
                st.session_state.clear()
                st.success("Logged out successfully.")
