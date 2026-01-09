import streamlit as st
from utils.auth import verify_pin
from datetime import datetime
import json, os
from utils.qr import generate_qr

DATA_FILE = "data/sessions.json"
os.makedirs("data", exist_ok=True)


def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    return json.load(open(DATA_FILE))


def save_data(data):
    json.dump(data, open(DATA_FILE, "w"), indent=2)


# 🔐 SESSION STATE
if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False

st.title("🎱 Pool Timer Admin")

# 🔐 PIN SCREEN
if not st.session_state.admin_logged_in:
    pin = st.text_input("Enter Admin PIN", type="password")

    if st.button("Login"):
        if verify_pin(pin):
            st.session_state.admin_logged_in = True
            st.success("Access Granted ✅")
            st.rerun()
        else:
            st.error("Invalid PIN ❌")

    st.stop()

# ✅ ADMIN CONTROLS
st.success("Logged in as Admin")

table = st.selectbox("Table", ["table_1", "table_2"])
name = st.text_input("Customer Name")
rate = st.number_input("Rate (₹ / 30 mins)", value=100)

data = load_data()
session = data.get(table)

# ▶ START GAME
if st.button("▶ Start Game"):
    data[table] = {
        "customer_name": name,
        "rate_per_30": rate,
        "start_time": datetime.now().isoformat(),
        "paused": False,
        "pause_start": None,
        "total_paused_seconds": 0,
        "active": True
    }
    save_data(data)

    app_url = st.secrets.get("APP_URL", "http://localhost:8501")
    qr_url = f"{app_url}/?table={table}"
    qr = generate_qr(qr_url)

    st.image(qr, caption="Customer QR Code")
    st.success("Game Started")

st.divider()
st.subheader("⏸ Pool Controls")

# ⏸ PAUSE / ▶ RESUME
data = load_data()
session = data.get(table)

if session and session.get("active"):
    if not session.get("paused"):
        if st.button("⏸ Pause Game"):
            session["paused"] = True
            session["pause_start"] = datetime.now().isoformat()
            save_data(data)
            st.rerun()
    else:
        if st.button("▶ Resume Game"):
            pause_start = datetime.fromisoformat(session["pause_start"])
            paused_time = (datetime.now() - pause_start).total_seconds()

            session["total_paused_seconds"] += paused_time
            session["pause_start"] = None
            session["paused"] = False
            save_data(data)
            st.rerun()
else:
    st.info("No active game on this table")

st.divider()

# 🔓 LOGOUT
if st.button("Logout"):
    st.session_state.admin_logged_in = False
    st.rerun()
