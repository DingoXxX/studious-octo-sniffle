from app.transfer import initiate_ach_transfer, initiate_wire_transfer
from app.mfa import generate_otp_secret, get_current_otp, verify_otp
from app.kyc_aml import check_kyc, run_aml_screening

def run_all_tests():
    print(initiate_ach_transfer("user001", "1234567890", 150.00))
    print(initiate_wire_transfer("user002", "DEUTDEFF", "DE89370400440532013000", 500.00))

    otp_secret = generate_otp_secret()
    current_otp = get_current_otp(otp_secret)
    print(f"Generated OTP: {current_otp}")
    print("OTP valid:", verify_otp(otp_secret, current_otp))

    print(check_kyc("user001"))
    print(run_aml_screening("Jane Smith"))

if __name__ == "__main__":
    run_all_tests()
