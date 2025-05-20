def check_kyc(user_id: str):
    # Simulated check
    return {"user_id": user_id, "kyc_status": "verified"}

def run_aml_screening(name: str):
    # Simulated AML screening
    flagged_names = ["John Doe", "Jane Smith"]
    if name in flagged_names:
        return {"name": name, "aml_flag": True}
    return {"name": name, "aml_flag": False}
