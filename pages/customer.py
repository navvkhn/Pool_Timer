import streamlit as st
import json, os
from utils.billing import calculate_bill
from streamlit_autorefresh import st_autorefresh

st.set_page_config(
    page_title="Pool Timer",
    page_icon="🎱",
    layout="centered"
)

DATA_FILE = "data/sessions.json"

# 🔄 Auto refresh every 5 seconds
st_autorefresh(interval=5000, key="refresh")

# --- Read table from QR ---
query = st.query_params
table = query.get("table", [None])[0]

if not table:
    st.error("Invalid QR")
    st.stop()

if not os.path.exists(DATA_FILE):
    st.warning("No active session")
    st.stop()

data = json.load(open(DATA_FILE))
session = data.get(table)

if not session or not session.get("active"):
    st.warning("Game not active")
    st.stop()

elapsed_mins, bill = calculate_bill(session)

st.title("🎱 Pool Timer")

st.metric("Table", table)
st.metric("Customer", session["customer_name"])
st.metric("Time Elapsed", f"{elapsed_mins} mins")
st.metric("Current Bill", f"₹{bill}")

if session.get("paused"):
    st.warning("⏸ Game Paused")
