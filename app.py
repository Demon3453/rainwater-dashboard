import streamlit as st
import pandas as pd
import sqlite3
import time

# --- CONFIGURATION ---
DB_FILE = "water_data.db"

# --- PAGE CONFIG ---
# Set page title, icon, and layout
st.set_page_config(
    page_title="Live Water Quality Dashboard",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- STYLING (NEW) ---
# Custom CSS for colorful metric boxes and titles
st.markdown("""
<style>
    /* Main title style */
    .main-title {
        font-size: 3rem;
        font-weight: bold;
        padding: 10px;
        border-radius: 10px;
        color: white;
        text-align: center;
        background-image: linear-gradient(to right, #007bff, #00bfff);
    }
    /* Sub-header style */
    .sub-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #007bff;
        text-align: center;
    }
    /* Custom metric box */
    .metric-box {
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .metric-box h3 {
        font-size: 1.25rem;
        margin-bottom: 10px;
    }
    .metric-box p {
        font-size: 2.5rem;
        font-weight: bold;
    }
    .ph-box { background-color: #28a745; }
    .solids-box { background-color: #17a2b8; }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
st.sidebar.header("About")
st.sidebar.info(
    "This is a real-time dashboard that analyzes rainwater quality using an AI model. "
    "Data is sent from an STM32 sensor unit and updated live."
)
st.sidebar.success("Project by **Team Legions**")


# --- DASHBOARD UI ---
# Use markdown with custom CSS classes for colorful titles
st.markdown('<p class="sub-header">Team Legions Presents</p>', unsafe_allow_html=True)
st.markdown('<p class="main-title">💧 Live Rainwater Quality Dashboard</p>', unsafe_allow_html=True)

st.header("Latest Reading")

# Create placeholders for our metrics and status
col1, col2, col3 = st.columns(3)
placeholder_ph = col1.empty()
placeholder_solids = col2.empty()
placeholder_status = col3.empty()

st.header("Historical Data")
placeholder_table = st.empty()


# --- FUNCTION TO GET DATA ---
def get_latest_reading():
    """Fetch readings from the database."""
    try:
        conn = sqlite3.connect(DB_FILE)
        latest_df = pd.read_sql_query("SELECT * FROM readings ORDER BY timestamp DESC LIMIT 1", conn)
        history_df = pd.read_sql_query("SELECT * FROM readings ORDER BY timestamp DESC LIMIT 20", conn)
        conn.close()
        return latest_df, history_df
    except Exception:
        return pd.DataFrame(), pd.DataFrame()

# --- LIVE UPDATE LOOP ---
while True:
    latest_data, history_data = get_latest_reading()

    if not latest_data.empty:
        latest_ph = latest_data['ph'].iloc[0]
        latest_solids = latest_data['Solids'].iloc[0]
        latest_prediction = latest_data['prediction'].iloc[0]

        # NEW: Update the colorful metric boxes
        with placeholder_ph:
            st.markdown(f'<div class="metric-box ph-box"><h3>pH Level</h3><p>{latest_ph:.2f}</p></div>', unsafe_allow_html=True)
        
        with placeholder_solids:
            st.markdown(f'<div class="metric-box solids-box"><h3>TDS (ppm)</h3><p>{latest_solids:.0f}</p></div>', unsafe_allow_html=True)

        with placeholder_status:
            if latest_prediction == "Potable":
                st.success(f"## Status: {latest_prediction} ✅")
            else:
                st.error(f"## Status: {latest_prediction} ❌")

        placeholder_table.dataframe(history_data, use_container_width=True)
    else:
        st.info("Waiting for the first data reading from your device...")

    time.sleep(5)

# --- FUNCTION TO GET DATA ---
def get_latest_reading():
    """Fetch the most recent reading from the database."""
    try:
        conn = sqlite3.connect(DB_FILE)
        # Get the most recent row
        latest_df = pd.read_sql_query("SELECT * FROM readings ORDER BY timestamp DESC LIMIT 1", conn)
        # Get all rows for the history table
        history_df = pd.read_sql_query("SELECT * FROM readings ORDER BY timestamp DESC LIMIT 20", conn)
        conn.close()
        return latest_df, history_df
    except Exception as e:
        # Return empty dataframes if table doesn't exist yet or there's an error
        return pd.DataFrame(), pd.DataFrame()

# --- LIVE UPDATE LOOP ---
while True:
    latest_data, history_data = get_latest_reading()

    if not latest_data.empty:
        # Update the metrics
        latest_ph = latest_data['ph'].iloc[0]
        latest_solids = latest_data['Solids'].iloc[0]
        latest_prediction = latest_data['prediction'].iloc[0]

        placeholder_ph.metric("pH Level", f"{latest_ph:.2f}")
        placeholder_solids.metric("Total Dissolved Solids (ppm)", f"{latest_solids:.0f}")

        if latest_prediction == "Potable":
            placeholder_status.success(f"Status: {latest_prediction} ✅")
        else:
            placeholder_status.error(f"Status: {latest_prediction} ❌")

        # Update the history table
        placeholder_table.dataframe(history_data, use_container_width=True)

    else:
        st.info("Waiting for the first data reading from your device...")

    # Wait for 5 seconds before checking the database again
    time.sleep(5)