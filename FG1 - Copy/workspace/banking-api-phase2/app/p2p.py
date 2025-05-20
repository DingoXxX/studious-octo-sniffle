def peer_to_peer_payment(sender: str, receiver: str, amount: float):
    return {
        "sender": sender,
        "receiver": receiver,
        "amount": amount,
        "status": "sent"
    }
