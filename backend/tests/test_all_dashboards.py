"""Test dashboard endpoints"""
from fastapi.testclient import TestClient
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.main import app

client = TestClient(app)

def test_public_endpoints():
    for ep in ["/health", "/", "/api/student/announcements", "/api/parent/events"]:
        r = client.get(ep)
        assert r.status_code == 200, f"{ep} = {r.status_code}"

def test_protected_dashboards():
    protected = ["/api/hod/dashboard", "/api/student/dashboard", "/api/student/grades"]
    for ep in protected:
        r = client.get(ep)
        assert r.status_code == 401, f"{ep} should be 401, got {r.status_code}"
