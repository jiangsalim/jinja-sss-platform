"""Test student API endpoints"""
from fastapi.testclient import TestClient
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.main import app

client = TestClient(app)

def test_announcements():
    response = client.get("/api/student/announcements")
    assert response.status_code == 200
    assert response.json()["success"] == True

def test_dashboard_unauthorized():
    response = client.get("/api/student/dashboard")
    assert response.status_code == 401

def test_grades_unauthorized():
    response = client.get("/api/student/grades")
    assert response.status_code == 401
