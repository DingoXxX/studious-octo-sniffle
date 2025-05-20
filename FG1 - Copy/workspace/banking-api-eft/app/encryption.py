from cryptography.fernet import Fernet
import os

key = Fernet.generate_key()  # Replace with env var in prod
cipher = Fernet(key)

def encrypt_data(data: str) -> str:
    return cipher.encrypt(data.encode()).decode()

def decrypt_data(token: str) -> str:
    return cipher.decrypt(token.encode()).decode()
