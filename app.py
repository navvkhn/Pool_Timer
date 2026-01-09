import streamlit as st
import json
import os
from utils.billing import calculate_bill
from streamlit_autorefresh import st_autorefresh

# ----------------------------
# Page config (IMPORTANT)
# ----------------------------
st.set_page_config(
    page_title="Pool Timer",
    page_icon="🎱",
    layout="wide"   # WIDE so sidebar is visible
)

# ----------------------------
# FORCE SIDEBAR TO SHOW
# ----------------------------
st.sidebar.title("🎱 Pool Timer")
st.sidebar.markdown("Use sidebar to navigate")

# ----------------------------
# Constants
# ----------------------------
DATA_FILE = os.path.join("data", "sessions.json")

# Auto-refresh customer screen
st_autorefresh(interval=5000, key="refresh")

# ----------------------------
# Read QR parameter
# ----------------------------
table = st.query_params.get("table")

# ----------------------------
# UI
# ----------------------------
st.title("🎱 Pool Timer")

# ----------------------------
# CUSTOMER LANDING (NO QR)
# ----------------------------
if not table:
    st.info("Scan the QR code on your table")

    st.markdown(
        """
        ### 🔐 Staff Access
        Open the **sidebar** and click **Admin**
        """
    )
    st.stop()

# ----------------------------
# CUSTOMER SESSION VIEW
# ----------------------------
if not os.path.exists(DATA_FILE):
    st.warning("No active session")
    st.stop()

with open(DATA_FILE, "r") as f:
    data = json.load(f)

session = data.get(table)

if not session:
    st.warning("Game not started yet")
    st.stop()

if session.get("ended"):
    st.success(f"Game Ended\n\nFinal Bill: ₹{session['final_bill']}")
    st.stop()

# Calculate billing
elapsed_minutes, bill = calculate_bill(session)

st.metric("Time Elapsed", f"{elapsed_minutes} mins")
st.metric("Current Bill", f"₹{bill}")

if session.get("paused"):
    st.warning("⏸ Game Paused")
