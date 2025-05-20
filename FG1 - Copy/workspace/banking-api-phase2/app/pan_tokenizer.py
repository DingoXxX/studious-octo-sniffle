from cryptography.fernet import Fernet
import os

# Generate key for demonstration; in real apps, load securely
key = Fernet.generate_key()
cipher = Fernet(key)

def tokenize_pan(pan: str):
    return cipher.encrypt(pan.encode()).decode()

def detokenize_pan(token: str):
    return cipher.decrypt(token.encode()).decode()
