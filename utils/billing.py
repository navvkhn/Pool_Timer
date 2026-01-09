from datetime import datetime
import math

def calculate_bill(start_time, rate_per_30):
    start = datetime.fromisoformat(start_time)
    now = datetime.now()

    elapsed_minutes = (now - start).total_seconds() / 60

    # Round up to nearest 15 mins
    rounded_minutes = math.ceil(elapsed_minutes / 15) * 15

    rate_per_min = rate_per_30 / 30
    bill = rounded_minutes * rate_per_min

    return int(rounded_minutes), int(bill)
