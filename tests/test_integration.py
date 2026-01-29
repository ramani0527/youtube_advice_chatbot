import sys
import os

project_root = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, project_root)

from fastapi.testclient import TestClient
from src.main import app  

client = TestClient(app)

def test_ask_endpoint_returns_answer():
    response = client.post("/ask", json={"question": "How to improve introductions?"})
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert "chunks" in data
    if data["chunks"]:
        assert "[source:" in data["answer"]

def test_ask_endpoint_with_video_filter():
    response = client.post("/ask", json={"question": "How to improve intros?", "video_id": "aprilynne"})
    assert response.status_code == 200
    data = response.json()
    for c in data["chunks"]:
        assert c["video_id"] == "aprilynne"
