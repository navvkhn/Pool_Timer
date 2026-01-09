from datetime import datetime
import math

def calculate_bill(session):
    start = datetime.fromisoformat(session["start_time"])
    now = datetime.now()

    paused_seconds = session.get("total_paused_seconds", 0)

    if session.get("paused") and session.get("pause_start"):
        pause_start = datetime.fromisoformat(session["pause_start"])
        paused_seconds += (now - pause_start).total_seconds()

    elapsed_seconds = (now - start).total_seconds() - paused_seconds
    elapsed_minutes = max(0, elapsed_seconds / 60)

    rounded_minutes = math.ceil(elapsed_minutes / 15) * 15
    rate_per_min = session["rate_per_30"] / 30
    bill = rounded_minutes * rate_per_min

    return int(rounded_minutes), int(bill)
