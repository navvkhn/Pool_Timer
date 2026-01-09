import hashlib
from config import ADMIN_PIN_HASH

def verify_pin(pin: str) -> bool:
    hashed = hashlib.sha256(pin.encode()).hexdigest()
    return hashed == ADMIN_PIN_HASH
