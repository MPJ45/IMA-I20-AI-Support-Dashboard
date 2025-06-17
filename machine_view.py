import streamlit as st
import firebase_admin
from firebase_admin import credentials
import pandas as pd
from utils import show_home_button, get_safe_machine_data

def main():
    if not firebase_admin._apps:
        cred = credentials.Certificate("/home/darkdemon/firebase_project/firebase-key.json")
        firebase_admin.initialize_app(cred, {
            'databaseURL': "https://your-database.firebaseio.com/"
        })

    show_home_button()

    st.markdown("<h1 style='text-align: center; color: #003366;'>📊 Machine Performance Dashboard</h1>", unsafe_allow_html=True)

    machine_options = [
        "P40W41", "P42W43", "P44W45", "P46W47",
        "P48W49", "P50W51", "P62W63", "P64W65",
        "P66W67", "P68W69", "P80W81", "P82W83",
        "P84W85", "P86W87", "P88W89"
    ]
    selected_machine = st.selectbox("🛠️ Select Machine to View Performance", machine_options)

    # ✅ Use safe utility function from utils.py
    machine_data = get_safe_machine_data(selected_machine)

    if machine_data.empty:
        st.warning("⚠ No performance data available for this machine yet.")
        return

    st.subheader(f"📌 Performance Data for {selected_machine}")
    st.dataframe(machine_data, use_container_width=True)

    avg_oee = machine_data["oee_value"].mean() if "oee_value" in machine_data.columns else 0
    avg_downtime = machine_data["downtime_mins"].mean() if "downtime_mins" in machine_data.columns else 0
    common_issues = machine_data["issue_logged"].value_counts().head(5).index.tolist() if "issue_logged" in machine_data.columns else ["No issues logged"]

    st.markdown(f"**📊 Average OEE:** {avg_oee:.2f}%")
    st.markdown(f"**⚠ Average Downtime:** {avg_downtime:.1f} mins")
    st.markdown(f"**🔍 Most Common Issues:** {', '.join(common_issues)}")

    st.success("✅ Machine Performance View Loaded Successfully!")
