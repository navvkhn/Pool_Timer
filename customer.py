import streamlit as st
import json, os
from utils.billing import calculate_bill
from streamlit_autorefresh import st_autorefresh

DATA_FILE = "data/sessions.json"

st_autorefresh(interval=5000, key="refresh")

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

mins, bill = calculate_bill(session)

st.title("🎱 Pool Timer")

st.metric("Customer", session["customer_name"])
st.metric("Table", table)
st.metric("Elapsed Time", f"{mins} mins")
st.metric("Current Bill", f"₹{bill}")

if session.get("paused"):
    st.warning("⏸ Game Paused")
