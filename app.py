import streamlit as st
import pandas as pd
import sqlite3
import time

# --- CONFIGURATION ---
DB_FILE = "water_data.db"

# --- APP LAYOUT ---
st.set_page_config(layout="wide")
st.title("💧 Live Rainwater Quality Dashboard")

# Create placeholders for our metrics and status
st.header("Latest Reading")
col1, col2, col3 = st.columns(3)
placeholder_ph = col1.empty()
placeholder_solids = col2.empty()
placeholder_status = col3.empty()

st.header("Historical Data")
placeholder_table = st.empty()

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