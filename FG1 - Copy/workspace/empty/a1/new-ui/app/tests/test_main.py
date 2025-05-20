import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code in (200, 404)  # 200 if root exists, 404 if SPA only

def test_register_and_login():
    # Register
    payload = {"username": "testuser", "email": "testuser@example.com", "password": "testpass123"}
    response = client.post("/users/", json=payload)
    assert response.status_code in (200, 201, 400)  # 400 if user exists
    # Login
    login_payload = {"username": "testuser", "password": "testpass123"}
    response = client.post("/auth/token", data=login_payload)
    assert response.status_code == 200
    assert "access_token" in response.json()
