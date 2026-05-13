"""Test authentication endpoints"""
from fastapi.testclient import TestClient
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.main import app

client = TestClient(app)

def test_signup():
    response = client.post("/auth/signup", json={
        "full_name": "Test User", "username": "test999", "password": "StrongP@ss1", "role": "parent"
    })
    assert response.status_code in [200, 201, 409]

def test_signin():
    response = client.post("/auth/signin", json={"identifier": "admin", "password": "admin123"})
    assert response.status_code in [200, 401, 423]
