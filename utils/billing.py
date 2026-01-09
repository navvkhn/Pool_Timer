from datetime import datetime
from zoneinfo import ZoneInfo
import math

IST = ZoneInfo("Asia/Kolkata")

def calculate_bill(session):
    start = datetime.fromisoformat(session["start_time"])
    now = datetime.now(IST)

    paused_seconds = session.get("total_paused_seconds", 0)

    if session.get("paused") and session.get("pause_start"):
        pause_start = datetime.fromisoformat(session["pause_start"])
        paused_seconds += (now - pause_start).total_seconds()

    elapsed_seconds = (now - start).total_seconds() - paused_seconds
    elapsed_minutes = max(0, int(elapsed_seconds // 60))

    # 🔹 Billing rounded to 15 min slabs
    billable_minutes = math.ceil(elapsed_minutes / 15) * 15

    rate_per_15 = session["rate_per_30"] / 2
    bill = int((billable_minutes / 15) * rate_per_15)

    return elapsed_minutes, bill
