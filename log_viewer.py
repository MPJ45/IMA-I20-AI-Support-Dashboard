import streamlit as st
import pandas as pd
import firebase_admin
from firebase_admin import credentials, db, exceptions
from utils import show_home_button

# ✅ Initialize Firebase if not already done
if not firebase_admin._apps:
    cred = credentials.Certificate("/home/darkdemon/firebase_project/firebase-key.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL': "https://your-database.firebaseio.com/"
    })

def main():
    show_home_button()  # ✅ Add home button at the top

    st.markdown("## 📋 Operator Log Viewer")

    try:
        ref = db.reference("/shift_logs")
        raw_data = ref.get()

        if not raw_data:
            st.info("⚠️ No logs found yet.")
            return

        records = []
        for machine, entries in raw_data.items():
            for log_id, entry in entries.items():
                records.append({
                    "Machine": machine,
                    "Operator": entry.get("operator_id", ""),
                    "Date": entry.get("log_date", ""),
                    "Shift": entry.get("shift_label", ""),
                    "Issue": entry.get("issue_logged", ""),
                    "Fix": entry.get("fix_logged", ""),
                    "Downtime (mins)": entry.get("downtime_mins", ""),
                    "Log ID": log_id
                })

        df = pd.DataFrame(records)

        # === Filters ===
        with st.expander("🔍 Filter Logs", expanded=False):
            col1, col2, col3 = st.columns(3)

            machines = ["All"] + sorted(df["Machine"].unique())
            operators = ["All"] + sorted(df["Operator"].unique())
            shifts = ["All"] + sorted(df["Shift"].unique())

            selected_machine = col1.selectbox("Machine", machines)
            selected_operator = col2.selectbox("Operator", operators)
            selected_shift = col3.selectbox("Shift", shifts)

            if selected_machine != "All":
                df = df[df["Machine"] == selected_machine]
            if selected_operator != "All":
                df = df[df["Operator"] == selected_operator]
            if selected_shift != "All":
                df = df[df["Shift"] == selected_shift]

        df = df.sort_values(by="Date", ascending=False)
        st.dataframe(df.drop(columns=["Log ID"]), use_container_width=True)

    except exceptions.NotFoundError:
        st.warning("❌ Firebase path '/shift_logs' not found.")
    except Exception as e:
        st.error(f"🔥 Unexpected error while loading logs: {e}")
