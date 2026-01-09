import streamlit as st
import json, os
from utils.billing import calculate_bill
from streamlit_autorefresh import st_autorefresh

# 🔑 Detect current page
from streamlit.runtime.scriptrunner import get_script_run_ctx

ctx = get_script_run_ctx()
if ctx and ctx.page_script_hash != ctx.main_script_hash:
    # We are NOT on the main app (e.g. /admin)
    # Do NOT render customer UI
    st.stop()

# ─────────────────────────────
# CUSTOMER ROOT APP
# ─────────────────────────────

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

# ───────── LANDING ─────────
if not table:
    st.info("Scan the QR code on your table")
    st.stop()

# ───────── CUSTOMER SESSION ─────────
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
