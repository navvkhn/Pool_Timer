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
st_autorefresh(interval=5000, key="refresh")

query = st.query_params
table = query.get("table", [None])[0]

st.title("🎱 Pool Timer")

# ───────── CUSTOMER LANDING ─────────
if not table:
    st.info("Scan the QR code on your table")

    st.divider()
    st.subheader("🔐 Staff Access")

    # ✅ Streamlit-native navigation
    st.page_link(
        "pages/admin.py",
        label="Admin Login",
        icon="🔐"
    )
    st.stop()

# ───────── CUSTOMER SESSION VIEW ─────────
if not os.path.exists(DATA_FILE):
    st.warning("No active session")
    st.stop()

data = json.load(open(DATA_FILE))
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
