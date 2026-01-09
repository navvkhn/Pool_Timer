import hashlib
from config import ADMIN_PIN_HASH

def verify_pin(pin: str) -> bool:
    return hashlib.sha256(pin.encode()).hexdigest() == ADMIN_PIN_HASH
