from datetime import datetime
from zoneinfo import ZoneInfo
import math

IST = ZoneInfo("Asia/Kolkata")

def calculate_bill(session):
    # --- Parse start time safely ---
    start = datetime.strptime(
        session["start_time"], "%Y-%m-%d %H:%M:%S"
    ).replace(tzinfo=IST)

    now = datetime.now(IST)

    # --- SAFETY: paused seconds must always be a number ---
    paused_seconds = session.get("total_paused_seconds") or 0

    # --- If currently paused, add running pause duration ---
    if session.get("paused") and session.get("pause_start"):
        pause_start = datetime.strptime(
            session["pause_start"], "%Y-%m-%d %H:%M:%S"
        ).replace(tzinfo=IST)

        paused_seconds += (now - pause_start).total_seconds()

    # --- Final elapsed time ---
    elapsed_seconds = max(0, (now - start).total_seconds() - paused_seconds)
    elapsed_minutes = int(elapsed_seconds // 60)   # REAL minutes

    # --- Billing slabs (15 min) ---
    billable_minutes = math.ceil(elapsed_minutes / 15) * 15
    rate_per_15 = session["rate_per_30"] / 2
    bill = int((billable_minutes / 15) * rate_per_15)

    return elapsed_minutes, bill
