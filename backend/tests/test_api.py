
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch

# Prevent heavyweight AI models from loading during API test collection.
with patch("app.image_classifier.image_classifier", new_callable=MagicMock), \
     patch("app.text_classifier.text_classifier", new_callable=MagicMock):
    from app.main import app


client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200

    data = response.json()
    assert data["application"] == "AI VisionOps"
    assert data["status"] == "running"


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_ready():
    response = client.get("/ready")
    assert response.status_code == 200
    assert "status" in response.json()


def test_model_info():
    response = client.get("/model-info")
    assert response.status_code == 200

    data = response.json()
    assert "image_model" in data
    assert "text_model" in data


def test_status():
    response = client.get("/status")
    assert response.status_code == 200

    data = response.json()
    assert "application" in data
    assert "status" in data
    assert "image_classifier" in data
    assert "text_classifier" in data
