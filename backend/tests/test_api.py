
import sys
from types import ModuleType
from unittest.mock import MagicMock

from fastapi.testclient import TestClient

# Mock the image classifier before importing the application.
image_module = ModuleType("app.image_classifier")
image_classifier = MagicMock()
image_classifier.loaded = True
image_classifier.get_info.return_value = {
    "name": "Mock MobileNetV2"
}
image_module.image_classifier = image_classifier
sys.modules["app.image_classifier"] = image_module

# Mock the text classifier before importing the application.
text_module = ModuleType("app.text_classifier")
text_classifier = MagicMock()
text_classifier.loaded = True
text_classifier.get_info.return_value = {
    "name": "Mock RoBERTa"
}
text_module.text_classifier = text_classifier
sys.modules["app.text_classifier"] = text_module

# Import the API only after installing the mock modules.
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
    assert response.json()["status"] == "ready"


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
    assert data["application"] == "AI VisionOps"
    assert data["status"] == "running"
    assert data["image_classifier"] == "ready"
    assert data["text_classifier"] == "ready"
