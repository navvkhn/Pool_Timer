# 🎱 Pool Timer – QR Based Streamlit App

Pool Timer is a **Streamlit-based web application** designed for pool/snooker tables where:
- Admin starts a pool session
- A **QR code** is generated
- Customer scans the QR and sees **live game timing & bill** on their mobile

No login required for customers. Simple, fast, and POS-friendly.

---

## 🚀 Features

### Admin Panel
- Start pool game for a table
- Enter customer name
- Configure rate (₹ per 30 minutes)
- Auto-generate QR code for customer
- Multiple tables supported

### Customer View (via QR)
- Customer name
- Table number
- Start time
- **Live elapsed time**
- **Auto-calculated bill**
- Billing rounded to **15-minute slabs**
- Works on any mobile browser

---

## 🧮 Billing Logic

- Rate defined as **₹ per 30 minutes**
- Billing calculated per minute
- Time is **rounded up to nearest 15 minutes**

Example:
- Elapsed time: **17 mins**
- Rounded to: **30 mins**
- Bill = ₹100 (if rate is ₹100 / 30 mins)

---

## 🗂 Project Structure

Pool_Timer/
│
├── app.py # Main entry point
├── admin.py # Admin (Reception) screen
├── customer.py # Customer live timer screen
│
├── utils/
│ ├── billing.py # Billing & rounding logic
│ └── qr.py # QR code generation
│
├── data/
│ └── sessions.json # Session storage (temporary)
│
├── requirements.txt
└── README.md

yaml
Copy code

---

## 🧑‍💼 Admin Flow

1. Open Admin panel
2. Select table
3. Enter customer name
4. Set rate
5. Click **Start Game**
6. QR code appears
7. Customer scans QR

---

## 📱 Customer Flow

1. Scan QR code
2. Opens web app automatically
3. View:
   - Name
   - Table
   - Start time
   - Time elapsed
   - Current bill
4. Refresh to update live bill

---

## 🛠 Installation (Local)

```bash
git clone https://github.com/navvkhn/Pool_Timer.git
cd Pool_Timer
pip install -r requirements.txt
streamlit run app.py
🌐 Deployment
Recommended:

Streamlit Cloud

QR URL format:

ruby
Copy code
https://your-app-name.streamlit.app/?table=table_1
This URL is embedded inside the QR code.

🔮 Future Enhancements
⏸ Pause / Resume game

🧾 Combine Food + Pool billing

🔐 Admin authentication

🗄 Supabase / Database storage

📄 PDF bill generation

🔄 Auto-refresh without manual reload
