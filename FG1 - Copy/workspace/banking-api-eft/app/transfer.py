from app.encryption import encrypt_data, decrypt_data

def initiate_ach_transfer(user_id: str, to_account: str, amount: float):
    secure_acc = encrypt_data(to_account)
    return {
        "user_id": user_id,
        "encrypted_account": secure_acc,
        "amount": amount,
        "type": "ACH",
        "status": "initiated"
    }

def initiate_wire_transfer(user_id: str, swift: str, iban: str, amount: float):
    secure_iban = encrypt_data(iban)
    return {
        "user_id": user_id,
        "SWIFT": swift,
        "encrypted_IBAN": secure_iban,
        "amount": amount,
        "type": "WIRE",
        "status": "initiated"
    }
