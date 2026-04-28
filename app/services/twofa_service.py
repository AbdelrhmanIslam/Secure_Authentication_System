import pyotp
import qrcode
import io
import base64

def generate_2fa_secret():
    return pyotp.random_base32()

def generate_qr_code(email, secret):
    uri = pyotp.totp.TOTP(secret).provisioning_uri(name=email, issuer_name="SecureApp")

    qr = qrcode.make(uri)
    buffered = io.BytesIO()
    qr.save(buffered, format="PNG")

    return base64.b64encode(buffered.getvalue()).decode()

def verify_2fa(secret, code):
    totp = pyotp.TOTP(secret)
    return totp.verify(code)