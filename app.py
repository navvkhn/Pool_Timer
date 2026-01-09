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

# 🔄 Auto refresh for customer view
st_autorefresh(interval=5000, key="refresh")

query = st.query_params
table = query.get("table", [None])[0]

st.title("🎱 Pool Timer")

# ─────────────────────────────
# 🧑 CUSTOMER LANDING (NO QR SCANNED)
# ─────────────────────────────
if not table:
    st.info("Scan the QR code on your table")

    st.divider()

    # 🔐 ADMIN BUTTON (ONLY ENTRY POINT)
    st.markdown(
        """
        <div style="text-align:center;">
            <a href="/admin" target="_self">
                <button style="
                    padding:10px 20px;
                    font-size:16px;
                    border-radius:8px;
                    border:none;
                    background-color:#1f77b4;
                    color:white;
                    cursor:pointer;
                ">
                    🔐 Admin Login
                </button>
            </a>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.stop()

# ─────────────────────────────
# 📱 CUSTOMER SESSION VIEW
# ─────────────────────────────
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
