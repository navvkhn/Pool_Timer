import streamlit as st
import json
from utils.billing import calculate_bill
from streamlit_autorefresh import st_autorefresh

DATA_FILE = "data/sessions.json"

# 🔄 AUTO REFRESH EVERY 5 SECONDS
st_autorefresh(interval=5000, key="timer_refresh")

query = st.query_params
table = query.get("table")

if not table:
    st.error("Invalid QR")
    st.stop()

data = json.load(open(DATA_FILE))
session = data.get(table)

if not session or not session["active"]:
    st.warning("Game not active")
    st.stop()

mins, bill = calculate_bill(session)

st.title("🎱 Pool Timer")

st.metric("Customer", session["customer_name"])
st.metric("Table", table)
st.metric("Time Elapsed", f"{mins} mins")
st.metric("Current Bill", f"₹{bill}")

if session.get("paused"):
    st.warning("⏸ Game Paused")
