import pyotp
import os

# Normally store and retrieve per-user secrets securely
def generate_otp_secret():
    return pyotp.random_base32()

def get_current_otp(secret: str):
    totp = pyotp.TOTP(secret)
    return totp.now()

def verify_otp(secret: str, otp: str) -> bool:
    totp = pyotp.TOTP(secret)
    return totp.verify(otp)
