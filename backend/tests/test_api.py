import io
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
image_classifier.predict.return_value = {
    "success": True,
    "model": "MobileNetV2",
    "dataset": "ImageNet",
    "predictions": [
        {"label": "golden retriever", "confidence": 94.25},
        {"label": "labrador", "confidence": 4.10},
    ],
    "inference_time_ms": 42.5,
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
text_classifier.predict.return_value = {
    "success": True,
    "model": "cardiffnlp/twitter-roberta-base-sentiment-latest",
    "task": "sentiment-analysis",
    "label": "Positive",
    "confidence": 98.45,
    "inference_time_ms": 25.1,
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


def test_predict_text_success():
    response = client.post(
        "/predict/text",
        json={"text": "This platform deployment is very reliable!"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["label"] == "Positive"
    assert data["confidence"] == 98.45


def test_predict_text_empty():
    response = client.post(
        "/predict/text",
        json={"text": "   "},
    )
    assert response.status_code == 400


def test_predict_image_success():
    fake_image_bytes = b"\xff\xd8\xff\xe0\x00\x10JFIF" + b"\x00" * 50
    response = client.post(
        "/predict/image",
        files={"file": ("test.jpg", io.BytesIO(fake_image_bytes), "image/jpeg")},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["model"] == "MobileNetV2"
    assert len(data["predictions"]) == 2


def test_predict_image_unsupported_type():
    response = client.post(
        "/predict/image",
        files={"file": ("test.txt", io.BytesIO(b"not an image"), "text/plain")},
    )
    assert response.status_code == 400
