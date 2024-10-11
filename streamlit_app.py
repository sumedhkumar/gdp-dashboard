import streamlit as st
import pandas as pd

# Sample users (replace with your authentication logic)
users = {
    "admin": {"password": "admin123", "role": "Admin"},
    "user": {"password": "user123", "role": "User"}
}

# Initialize session state variables
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
    st.session_state["role"] = None
    st.session_state["current_page"] = "login"  # Track the current page
    st.session_state["admin_data"] = None  # Store admin data globally

# Login Page
def login_page():
    st.title("Login Page")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in users and users[username]["password"] == password:
            st.session_state["logged_in"] = True
            st.session_state["role"] = users[username]["role"]
            st.success(f"Logged in as {st.session_state['role']}")
        else:
            st.error("Invalid username or password.")

    # "Next" button to navigate to the dashboard
    if st.session_state["logged_in"]:
        if st.button("Next"):
            st.session_state["current_page"] = "dashboard"  # Move to the dashboard

# Dashboard Page
def dashboard():
    st.title("Monk Traders BlackBox Strategy")
    st.subheader("Buy & sell as per below instructions.")

    if st.session_state["role"] == "Admin":
        st.success("Admin Login: You can edit the table below.")
        # Admin input form
        data = {
            'B/S': st.text_input('B/S', 'Buy'),
            'Expiry': st.date_input('Expiry'),
            'Strike': st.number_input('Strike', min_value=0),
            'Type': st.selectbox('Type', ['Call', 'Put']),
            'Lots': st.number_input('Lots', min_value=1, value=1)
        }
        st.session_state["admin_data"] = pd.DataFrame([data])  # Store admin data globally
        st.write("Admin Input Table", st.session_state["admin_data"])

        # Save button
        if st.button('Save'):
            st.success("Data saved and updated in real-time.")

    else:
        st.info("User Login: View-only access.")
        # Display updated table for User in real time
        if st.session_state["admin_data"] is not None:
            st.write("User View Table")
            st.write(st.session_state["admin_data"])
        else:
            st.write("Waiting for Admin to input data...")

# Main Application Logic
if st.session_state["current_page"] == "login":
    login_page()  # Show login page if on the login page
elif st.session_state["current_page"] == "dashboard":
    if st.session_state["logged_in"]:
        dashboard()  # Show dashboard if logged in

# Logout button
if st.session_state["logged_in"]:
    if st.button("Logout"):
        st.session_state["logged_in"] = False
        st.session_state["role"] = None
        st.session_state["current_page"] = "login"  # Reset to login page
