import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_generate_bullets_api():
    payload = {
        "experience": "Built a recommendation engine using Python and collaborative filtering.",
        "job_description": "Looking for a Python developer with recommendation system expertise.",
        "style": "default"
    }

    response = client.post("/generate-bullets", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert "bullets" in data
    assert isinstance(data["bullets"], list)
    assert len(data["bullets"]) == 2
    assert all(isinstance(b, str) and b.strip() for b in data["bullets"])
