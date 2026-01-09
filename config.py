import hashlib

ADMIN_PIN_HASH = hashlib.sha256("1234".encode()).hexdigest()
