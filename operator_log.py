import streamlit as st
import datetime
import firebase_admin
from firebase_admin import credentials, db
from utils import show_home_button

# ✅ Initialize Firebase once
if not firebase_admin._apps:
    cred = credentials.Certificate("/home/darkdemon/firebase_project/firebase-key.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL': "https://your-database.firebaseio.com/"
    })

def main():
    show_home_button()

    st.markdown('<p class="title">✨ Operator Log System ✨</p>', unsafe_allow_html=True)

    st.markdown("""
        <style>
            .title {
                font-size: 28px;
                font-weight: bold;
                text-align: center;
                color: #003366;
            }
            .log-box {
                background-color: #ffffff;
                padding: 25px;
                border-radius: 12px;
                box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.2);
                text-align: center;
                width: 80%;
                margin: auto;
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="log-box">', unsafe_allow_html=True)

    log_date = datetime.date.today()
    st.date_input("📅 Log Date", log_date)

    operator_id = st.text_input("🔑 Enter Operator ID (e.g., PNG1080)")

    machine_options = [
        "P40W41", "P42W43", "P44W45", "P46W47",
        "P48W49", "P50W51", "P62W63", "P64W65",
        "P66W67", "P68W69", "P80W81", "P82W83",
        "P84W85", "P86W87", "P88W89"
    ]
    selected_machine = st.selectbox("🛠️ Select Machine", machine_options)

    shift_options = [
        "Day A (7AM - 7PM)",
        "Day B (7AM - 7PM)",
        "Night A (7PM - 7AM)",
        "Night B (7PM - 7AM)"
    ]
    selected_shift = st.selectbox("🔹 Select Shift", shift_options)

    issue_logged = st.text_area("⚠️ Describe the Issue")
    fix_logged = st.text_area("✅ Fix Applied")
    issue_duration = st.number_input("⏱️ Issue Duration (mins)", min_value=1, step=1)

    if st.button("Submit Log"):
        if operator_id and issue_logged and fix_logged and issue_duration:
            # ✅ Push to Firebase Realtime Database
            try:
                ref = db.reference(f"/shift_logs/{selected_machine}")
                ref.push({
                    "operator_id": operator_id,
                    "log_date": str(log_date),
                    "shift_label": selected_shift,
                    "issue_logged": issue_logged,
                    "fix_logged": fix_logged,
                    "downtime_mins": issue_duration
                })
                st.success(
                    f"📝 Log Submitted! | Operator: {operator_id} | Machine: {selected_machine} | "
                    f"Date: {log_date} | Shift: {selected_shift} | Issue Duration: {issue_duration} min"
                )
            except Exception as e:
                st.error(f"🚨 Failed to submit log: {e}")
        else:
            st.warning("⚠ Please fill out all fields before submitting.")

    st.markdown('</div>', unsafe_allow_html=True)
