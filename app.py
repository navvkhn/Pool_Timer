import streamlit as st
import json
import os
from utils.billing import calculate_bill
from streamlit_autorefresh import st_autorefresh

st.set_page_config(
    page_title="Pool Timer",
    page_icon="🎱",
    layout="centered"
)

DATA_FILE = os.path.join("data", "sessions.json")

# Auto-refresh for customer view
st_autorefresh(interval=5000, key="refresh")

# Read QR param
table = st.query_params.get("table")

st.title("🎱 Pool Timer")

# -----------------------------
# CUSTOMER LANDING
# -----------------------------
if not table:
    st.info("Scan the QR code on your table")

    st.divider()
    st.subheader("🔐 Staff Access")

    # IMPORTANT: absolute link
    st.link_button(
        "Admin Login",
        "/admin"
    )
    st.stop()

# -----------------------------
# CUSTOMER SESSION VIEW
# -----------------------------
if not os.path.exists(DATA_FILE):
    st.warning("No active session")
    st.stop()

with open(DATA_FILE) as f:
    data = json.load(f)

session = data.get(table)

if not session:
    st.warning("Game not started yet")
    st.stop()

if session.get("ended"):
    st.success(f"Game Ended\n\nFinal Bill: ₹{session['final_bill']}")
    st.stop()

mins, bill = calculate_bill(session)

st.metric("Time Elapsed", f"{mins} mins")
st.metric("Current Bill", f"₹{bill}")

if session.get("paused"):
    st.warning("⏸ Game Paused")
