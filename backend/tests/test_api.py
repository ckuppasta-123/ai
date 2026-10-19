from fastapi.testclient import TestClient

from app.main import app


def test_root():
    with TestClient(app) as client:
        response = client.get("/")

        assert response.status_code == 200

        data = response.json()

        assert data["application"] == "AI VisionOps"
        assert data["status"] == "running"


def test_health():
    with TestClient  (app) as client:
        response = client.get("/health")

        assert response.status_code == 200

        data = response.json()

        assert data["status"] == "healthy"
def test_ready():
    with TestClient(app) as client:
        response = client.get("/ready")

        assert response.status_code == 200

        data = response.json()

        assert "status" in data

def test_model_info():
    with TestClient(app) as client:
        response = client.get("/model-info")

        assert response.status_code == 200

        data = response.json()

        assert "image_model" in data
        assert "text_model" in data


def test_status():
    with TestClient(app) as client:
        response = client.get("/status")

        assert response.status_code == 200

        data = response.json()

        assert "application" in data
        assert "status" in data
        assert "image_classifier" in data
        assert "text_classifier" in data