from app.kyc import verify_identity
from app.ach import initiate_ach_transfer
from app.p2p import peer_to_peer_payment
from app.pan_tokenizer import tokenize_pan, detokenize_pan

def run_tests():
    print(verify_identity("user123", "passport"))
    print(initiate_ach_transfer("acc001", "acc002", 150.75))
    print(peer_to_peer_payment("userA", "userB", 50.00))
    token = tokenize_pan("4111111111111111")
    print("Token:", token)
    print("Original:", detokenize_pan(token))

if __name__ == "__main__":
    run_tests()
