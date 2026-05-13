"""Test senior management endpoints"""
from fastapi.testclient import TestClient
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.main import app

client = TestClient(app)

def test_headteacher_dashboard():
    response = client.get("/api/headteacher/dashboard")
    assert response.status_code == 200

def test_deputy_academics():
    response = client.get("/api/deputy-academics/dashboard")
    assert response.status_code == 200

def test_deputy_welfare():
    response = client.get("/api/deputy-welfare/dashboard")
    assert response.status_code == 200

def test_registrar():
    response = client.get("/api/registrar/dashboard")
    assert response.status_code == 200

def test_director_studies():
    response = client.get("/api/director-studies/dashboard")
    assert response.status_code == 200

def test_finance():
    response = client.get("/api/finance/dashboard")
    assert response.status_code == 200

def test_hr():
    response = client.get("/api/hr/dashboard")
    assert response.status_code == 200
