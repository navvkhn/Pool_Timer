import qrcode
from io import BytesIO

def generate_qr(url: str):
    qr = qrcode.make(url)
    buf = BytesIO()
    qr.save(buf, format="PNG")
    return buf.getvalue()
