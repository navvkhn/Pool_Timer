import streamlit as st
import json, os
from datetime import datetime
from utils.qr import generate_qr

DATA_FILE = "data/sessions.json"
os.makedirs("data", exist_ok=True)

def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    return json.load(open(DATA_FILE))

def save_data(data):
    json.dump(data, open(DATA_FILE, "w"), indent=2)

st.title("🎱 Pool Table Admin")

table = st.selectbox("Table", ["table_1", "table_2"])
name = st.text_input("Customer Name")
rate = st.number_input("Rate (₹ / 30 mins)", value=100)

if st.button("▶ Start Game"):
    data = load_data()
    data[table] = {
        "customer_name": name,
        "rate_per_30": rate,
        "start_time": datetime.now().isoformat(),
        "active": True
    }
    save_data(data)

    url = f"https://YOUR_STREAMLIT_URL/?table={table}"
    qr = generate_qr(url)

    st.success("Game Started")
    st.image(qr, caption="Customer QR Code")
