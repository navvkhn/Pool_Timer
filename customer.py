import streamlit as st
import json
from utils.billing import calculate_bill

DATA_FILE = "data/sessions.json"

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

mins, bill = calculate_bill(
    session["start_time"],
    session["rate_per_30"]
)

st.title("🎱 Pool Timer")

st.metric("Customer", session["customer_name"])
st.metric("Table", table)
st.metric("Start Time", session["start_time"])
st.metric("Time Elapsed", f"{mins} mins")
st.metric("Current Bill", f"₹{bill}")

st.caption("⏱ Updates every refresh")
st.button("🔄 Refresh")
