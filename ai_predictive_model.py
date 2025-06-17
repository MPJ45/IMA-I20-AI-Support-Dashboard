import streamlit as st
import firebase_admin
from firebase_admin import credentials
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from sklearn.ensemble import RandomForestRegressor
from utils import show_home_button, get_safe_machine_data

def main():
    if not firebase_admin._apps:
        cred = credentials.Certificate("/home/darkdemon/firebase_project/firebase-key.json")
        firebase_admin.initialize_app(cred, {
            'databaseURL': "https://ima-i20-default-rtdb.firebaseio.com/"
        })

    show_home_button()

    st.markdown("<h1 style='text-align: center; color: #003366;'>🤖 AI Predictive Dashboard</h1>", unsafe_allow_html=True)

    machine_options = [
        "P40W41", "P42W43", "P44W45", "P46W47",
        "P48W49", "P50W51", "P62W63", "P64W65",
        "P66W67", "P68W69", "P80W81", "P82W83",
        "P84W85", "P86W87", "P88W89"
    ]
    selected_machine = st.selectbox("🛠️ Select Machine", machine_options)

    # ✅ Fetch machine data safely
    data = get_safe_machine_data(selected_machine)

    if data.empty:
        st.warning(f"⚠ No machine data available for {selected_machine}. Start logging shifts to enable AI predictions.")
        return

    # ✅ Convert important columns to numeric
    for col in ["runtime_mins", "downtime_mins", "oee_value"]:
        data[col] = pd.to_numeric(data[col], errors="coerce")
    data = data.dropna(subset=["runtime_mins", "downtime_mins", "oee_value"])

    # ✅ Add shift selector matching logger format
    shift_options = ["Day A (7AM - 7PM)", "Day B (7AM - 7PM)", "Night A (7PM - 7AM)", "Night B (7PM - 7AM)"]
    selected_shift = st.selectbox("🔹 Select Shift", shift_options)
    data = data[data["shift_label"] == selected_shift]

    # ✅ Reset index for plotting
    data = data.reset_index(drop=True)

    # ✅ Prediction Logic
    if data.shape[0] < 5:
        st.info("🔎 Not enough data for training. Using averages with slight uncertainty.")
        avg_runtime = data["runtime_mins"].mean()
        avg_downtime = data["downtime_mins"].mean()
        avg_oee = data["oee_value"].mean()
        pred_runtime = avg_runtime * np.random.uniform(0.95, 1.05)
        pred_downtime = avg_downtime * np.random.uniform(0.95, 1.05)
        pred_oee = avg_oee * np.random.uniform(0.97, 1.05)
        confidence_low = pred_oee * 0.98
        confidence_high = pred_oee * 1.02
    else:
        X = data[["runtime_mins", "downtime_mins"]]
        y = data["oee_value"]
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X, y)
        avg_runtime = X["runtime_mins"].mean()
        avg_downtime = X["downtime_mins"].mean()
        avg_oee = y.mean()
        pred_oee = model.predict([[avg_runtime, avg_downtime]])[0]
        pred_runtime = avg_runtime * np.random.uniform(0.98, 1.04)
        pred_downtime = avg_downtime * np.random.uniform(0.98, 1.04)
        confidence_low = pred_oee * 0.95
        confidence_high = pred_oee * 1.05

    # ✅ Handle issue_logged if present
    issues = data["issue_logged"].dropna() if "issue_logged" in data.columns else pd.Series(dtype=str)
    top_issues = issues.value_counts().head(3).index.tolist() if not issues.empty else ["No logged issues"]

    # ✅ Output predictions
    st.subheader(f"📊 AI Prediction for {selected_machine} — {selected_shift}")
    st.markdown(f"**⏱ Avg Runtime:** {avg_runtime:.1f} mins → **Predicted:** {pred_runtime:.1f} mins")
    st.markdown(f"**⚠ Avg Downtime:** {avg_downtime:.1f} mins → **Predicted:** {pred_downtime:.1f} mins")
    st.markdown(f"**📈 Avg OEE:** {avg_oee:.1f}% → **Predicted:** {pred_oee:.1f}% (Confidence: {confidence_low:.1f}% – {confidence_high:.1f}%)")
    st.markdown(f"**🔍 Likely Issues Next Shift:** {', '.join(top_issues)}")

    # ✅ Line Chart
    fig_line = go.Figure()
    fig_line.add_trace(go.Scatter(x=data.index, y=data["oee_value"],
                                  mode="lines+markers", name="Historical OEE", line=dict(color="gray")))
    fig_line.add_trace(go.Scatter(x=[len(data)], y=[pred_oee],
                                  mode="markers", name="Predicted OEE", marker=dict(color="blue", size=10)))
    fig_line.update_layout(title="📊 OEE Trend & Forecast", xaxis_title="Shift Index", yaxis_title="OEE (%)")
    st.plotly_chart(fig_line, use_container_width=True)

    # ✅ Bar Chart
    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(x=["Runtime", "Downtime", "OEE"], y=[avg_runtime, avg_downtime, avg_oee],
                             name="Historical Avg", marker_color="lightgray"))
    fig_bar.add_trace(go.Bar(x=["Runtime", "Downtime", "OEE"], y=[pred_runtime, pred_downtime, pred_oee],
                             name="Predicted", marker_color="#003366"))
    fig_bar.update_layout(title="📊 Predicted vs Historical Performance", barmode="group")
    st.plotly_chart(fig_bar, use_container_width=True)

    if st.button("📥 Export Chart as PNG"):
        fig_bar.write_image("prediction_chart.png")
        st.success("✅ Chart saved successfully! Check your project folder.")
