import hashlib

# PIN = 1234
ADMIN_PIN_HASH = hashlib.sha256("9997".encode()).hexdigest()
