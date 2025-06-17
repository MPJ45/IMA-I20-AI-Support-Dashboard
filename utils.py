import streamlit as st
import datetime
import pandas as pd
from firebase_admin import db, exceptions
from firebase_config import get_db_ref  # 🔧 Use your centralized Firebase reference

# Function to format timestamps
def format_timestamp():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Convert OEE percentage to performance grade
def get_oee_grade(oee_value):
    if oee_value >= 85:
        return "🔵 Excellent"
    elif oee_value >= 70:
        return "🟢 Good"
    elif oee_value >= 50:
        return "🟡 Needs Improvement"
    else:
        return "🔴 Critical"

# Utility to clean user input
def sanitize_input(text):
    return text.strip().lower()

# Optional login form
def login_form():
    st.markdown(
        "<h1 style='text-align: center; color: #003366;'>IMA I20 AI SUPPORT SYSTEM</h1>",
        unsafe_allow_html=True
    )
    st.subheader("🔐 Login with your PNG number or full name")
    username = st.text_input("Enter PNG Number or Full Name")

    if st.button("Login"):
        if username.strip():
            st.session_state["logged_in"] = True
            st.session_state["user"] = username
            st.success(f"✅ Welcome, {username}!")
            st.experimental_rerun()
        else:
            st.error("❌ Please enter your PNG number or full name.")

# Home Button
def show_home_button():
    st.markdown("""
        <style>
            .stButton > button {
                background-color: #003366;
                color: white;
                padding: 10px 22px;
                font-size: 16px;
                font-weight: bold;
                border: none;
                border-radius: 8px;
                transition: 0.3s;
                cursor: pointer;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
            }
            .stButton > button:hover {
                background-color: #0055aa;
                transform: scale(1.05);
                box-shadow: 0 6px 20px rgba(0, 85, 170, 0.4);
            }
        </style>
    """, unsafe_allow_html=True)

    if st.button("🏠 Back to Home"):
        st.session_state.active_page = "home"

# ✅ Firebase-safe data loader with fallback
def get_safe_machine_data(machine_id):
    try:
        ref = get_db_ref(f"/shift_logs/{machine_id}")  # centralized call
        data = ref.get()
        if not data:
            st.warning(f"⚠️ No logs found for machine: {machine_id}")
            return pd.DataFrame()
        return pd.DataFrame.from_dict(data, orient="index")
    except exceptions.NotFoundError:
        st.warning(f"❌ Firebase path not found: /shift_logs/{machine_id}")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"🔥 Unexpected error while loading machine data: {e}")
        return pd.DataFrame()
