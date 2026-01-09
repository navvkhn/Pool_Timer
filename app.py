import streamlit as st
from utils.auth import verify_pin
from datetime import datetime
import json, os
from utils.billing import calculate_bill
from zoneinfo import ZoneInfo
from utils.qr import generate_qr

IST = ZoneInfo("Asia/Kolkata")

st.set_page_config(
    page_title="Pool Timer – Admin",
    page_icon="🎱",
    layout="centered"
)

DATA_FILE = "data/sessions.json"
os.makedirs("data", exist_ok=True)


def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    return json.load(open(DATA_FILE))


def save_data(data):
    json.dump(data, open(DATA_FILE, "w"), indent=2)


# 🔐 ADMIN SESSION
if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False

st.title("🎱 Pool Timer – Admin")

# ───────── LOGIN ─────────
if not st.session_state.admin_logged_in:
    pin = st.text_input("Enter Admin PIN", type="password")
    if st.button("Login"):
        if verify_pin(pin):
            st.session_state.admin_logged_in = True
            st.rerun()
        else:
            st.error("Invalid PIN")
    st.stop()

st.success("Logged in")

# ───────── INPUTS ─────────
table = st.selectbox("Table", ["table_1", "table_2"])
name = st.text_input("Customer Name")
rate = st.number_input("Rate (₹ / 30 mins)", value=100)

# ───────── FIXED CUSTOMER QR ─────────
st.divider()
st.subheader("📱 Customer QR & Link")

app_url = st.secrets.get("APP_URL", "http://localhost:8501")
customer_url = f"{app_url}/customer?table={table}"

st.image(generate_qr(customer_url), caption=f"Scan for {table}")
st.markdown(
    f'<a href="{customer_url}" target="_blank">{customer_url}</a>',
    unsafe_allow_html=True
)

# ───────── START GAME ─────────
data = load_data()
session = data.get(table)

if st.button("▶ Start Game"):
    data[table] = {
        "customer_name": name,
        "rate_per_30": rate,
        "start_time": datetime.now(IST).strftime("%Y-%m-%d %H:%M:%S"),
        "paused": False,
        "pause_start": None,
        "total_paused_seconds": 0,
        "active": True,
        "ended": False
    }
    save_data(data)
    st.success("Game Started")
    st.rerun()

# ───────── LIVE DETAILS ─────────
st.divider()
st.subheader("📊 Live Session")

data = load_data()
session = data.get(table)

if session and session.get("active"):
    mins, bill = calculate_bill(session)

    st.metric("Customer", session["customer_name"])
    st.metric("Elapsed", f"{mins} mins")
    st.metric("Bill", f"₹{bill}")

    if session["paused"]:
        st.warning("⏸ Paused")

else:
    st.info("No active game")

# ───────── PAUSE / RESUME ─────────
st.divider()
st.subheader("⏸ Controls")

if session and session.get("active"):
    if not session["paused"]:
        if st.button("⏸ Pause"):
            session["paused"] = True
            session["pause_start"] = datetime.now(IST).strftime("%Y-%m-%d %H:%M:%S")
            save_data(data)
            st.rerun()
    else:
        if st.button("▶ Resume"):
            pause_start = datetime.strptime(
                session["pause_start"], "%Y-%m-%d %H:%M:%S"
            ).replace(tzinfo=IST)

            session["total_paused_seconds"] += (
                datetime.now(IST) - pause_start
            ).total_seconds()

            session["pause_start"] = None
            session["paused"] = False
            save_data(data)
            st.rerun()

# ───────── END GAME (NEW) ─────────
st.divider()
st.subheader("⛔ End Game")

if session and session.get("active"):
    if st.button("⛔ End Game"):
        mins, bill = calculate_bill(session)
        session["active"] = False
        session["ended"] = True
        session["end_time"] = datetime.now(IST).strftime("%Y-%m-%d %H:%M:%S")
        session["final_minutes"] = mins
        session["final_bill"] = bill
        save_data(data)
        st.success(f"Game Ended — Final Bill ₹{bill}")
        st.rerun()

# ───────── LOGOUT ─────────
st.divider()
if st.button("Logout"):
    st.session_state.admin_logged_in = False
    st.rerun()
