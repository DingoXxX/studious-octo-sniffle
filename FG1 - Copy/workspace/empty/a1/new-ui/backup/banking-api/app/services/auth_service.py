def authenticate_user(username: str, password: str):
    # Mock authentication
    if username == "admin" and password == "secret":
        return {"username": "admin"}
    return None
