import streamlit as st
import datetime
from firebase_config import get_db_ref  # ✅ Centralized Firebase setup
from utils import show_home_button

def main():
    show_home_button()

    st.markdown('<p class="title">✨ Shift Data Logging ✨</p>', unsafe_allow_html=True)

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
            .red-text {
                color: red;
                font-weight: bold;
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="log-box">', unsafe_allow_html=True)

    log_date = datetime.date.today()
    st.date_input("📅 Log Date", log_date)
    operator_id = st.text_input("🔑 Operator ID")

    machine_options = [
        "P40W41", "P42W43", "P44W45", "P46W47",
        "P48W49", "P50W51", "P62W63", "P64W65",
        "P66W67", "P68W69", "P80W81", "P82W83",
        "P84W85", "P86W87", "P88W89"
    ]
    selected_machine = st.selectbox("🛠️ Select Machine", machine_options)

    shift_options = ["Day A (7AM - 7PM)", "Day B (7AM - 7PM)", "Night A (7PM - 7AM)", "Night B (7PM - 7AM)"]
    selected_shift = st.selectbox("🔹 Select Shift", shift_options)

    cube_count = st.number_input("🟦 Total Cube Count", min_value=1000000, max_value=1300000, step=10000)
    runtime_mins = st.number_input("⏱️ Runtime (minutes)", min_value=0.0, step=1.0)
    downtime_mins = st.number_input("⚠️ Downtime (minutes)", min_value=0.0, step=1.0)

    availability = st.number_input("🟢 Availability (%)", 0.0, 150.0, step=0.1)
    performance = st.number_input("⚡ Performance (%)", 0.0, 150.0, step=0.1)
    quality = st.number_input("✅ Quality (%)", 0.0, 150.0, step=0.1)
    oee_value = st.number_input("📊 OEE (%)", 0.0, 150.0, step=0.1)

    oee_display = f'<p class="red-text">OEE: {oee_value:.1f}%</p>' if oee_value < 73 else f"OEE: {oee_value:.1f}%"
    st.markdown(oee_display, unsafe_allow_html=True)

    if st.button("Submit Shift Log"):
        if all([operator_id, cube_count, runtime_mins, downtime_mins, availability, performance, quality, oee_value]):
            try:
                ref = get_db_ref(f"/shift_logs/{selected_machine}")
                ref.push({
                    "operator_id": operator_id,
                    "log_date": str(log_date),
                    "shift_label": selected_shift,
                    "cube_count": cube_count,
                    "runtime_mins": runtime_mins,
                    "downtime_mins": downtime_mins,
                    "availability": availability,
                    "performance": performance,
                    "quality": quality,
                    "oee_value": oee_value
                })
                st.success(
                    f"📝 Log Submitted! | Operator: {operator_id} | Machine: {selected_machine} | "
                    f"Shift: {selected_shift} | Date: {log_date}"
                )
            except Exception as e:
                st.error(f"🚨 Failed to submit log: {e}")
        else:
            st.warning("⚠ Please fill out all required fields before submitting.")

    st.markdown('</div>', unsafe_allow_html=True)
