import streamlit as st
import importlib

st.set_page_config(
    page_title="IMA I20 AI SUPPORT SYSTEM",
    page_icon="🤖",
    layout="wide"
)

# === Page Routing Dictionary ===
pages = {
    "Operator Log": "operator_log",
    "OEE Logging": "oee_logging",
    "Machine View": "machine_view",
    "AI Predictive Model": "ai_predictive_model",
    "Log Viewer": "log_viewer"  # 👈 Make sure this file exists!
}

# === Session State Defaults ===
if "active_page" not in st.session_state:
    st.session_state.active_page = "home"

if "go_to_page" in st.session_state:
    st.session_state.active_page = st.session_state["go_to_page"]
    del st.session_state["go_to_page"]

# === Page Loader ===
if st.session_state.active_page in pages:
    page = importlib.import_module(pages[st.session_state.active_page])
    if hasattr(page, "main"):
        page.main()
    else:
        st.error(f"❌ '{st.session_state.active_page}' module is missing a `main()` function.")
else:
    # === HOME PAGE ===
    st.markdown(
        "<h1 style='text-align: center; color: #003366;'>Welcome to IMA I20 AI Support System</h1>",
        unsafe_allow_html=True
    )
    st.markdown("""
        <div style='text-align: center; font-size: 18px; padding: 10px 50px 30px 50px;'>
            This intelligent dashboard supports the IMA I20 line by allowing operators to log performance data,monitor machine activity,analyze OEE metrics and access predictive AI tools.Select a section below to get started
        </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("📋 Operator Log"):
            st.session_state["go_to_page"] = "Operator Log"
        if st.button("📈 OEE Logging"):
            st.session_state["go_to_page"] = "OEE Logging"
        if st.button("📒 View Operator Logs"):
            st.session_state["go_to_page"] = "Log Viewer"  # 👈 This is the one you wanted
    with col2:
        if st.button("⚙️ Machine View"):
            st.session_state["go_to_page"] = "Machine View"
        if st.button("🧠 AI Predictive Model"):
            st.session_state["go_to_page"] = "AI Predictive Model"

    st.markdown(
        "<hr style='margin-top: 40px;'><p style='text-align: center; font-size: 14px;'>Crafted and Designed by <strong>MPJ_for onga cube factory</strong></p>",
        unsafe_allow_html=True
    )
