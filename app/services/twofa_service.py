import pyotp
import qrcode
import io
import base64 # To convert the image to a string so u can send it to the frontend

def generate_2fa_secret():
    return pyotp.random_base32() # This is the secret key that the user will use to generate the 2FA codes

def generate_qr_code(email, secret): 
    uri = pyotp.totp.TOTP(secret).provisioning_uri(name=email, issuer_name="SecureApp")

    qr = qrcode.make(uri) 
    buffered = io.BytesIO() # save in memory 
    qr.save(buffered, format="PNG") # Convert it to Base64

    return base64.b64encode(buffered.getvalue()).decode()

def verify_2fa(secret, code): # Code verification
    totp = pyotp.TOTP(secret)
    return totp.verify(code) # Compare and return true or false 