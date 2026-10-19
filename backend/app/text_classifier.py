
import time
from typing import Any

from transformers import pipeline


class TextClassifier:
    """
    Three-class sentiment classifier:
    Negative, Neutral, and Positive.
    """

    def __init__(self) -> None:
        self.model_name = (
            "cardiffnlp/twitter-roberta-base-sentiment-latest"
        )
        self.task = "sentiment-analysis"
        self.classifier = None
        self.loaded = False

    def load(self) -> None:
        """Load the pretrained three-class sentiment model."""

        if self.loaded:
            return

        self.classifier = pipeline(
            task=self.task,
            model=self.model_name,
            device=-1,
        )

        self.loaded = True

    def predict(self, text: str) -> dict[str, Any]:
        """Predict negative, neutral, or positive sentiment."""

        if not self.loaded:
            self.load()

        text = text.strip()

        if not text:
            raise ValueError("Text cannot be empty.")

        if len(text) > 2000:
            raise ValueError(
                "Text is too long. Maximum length is 2000 characters."
            )

        start_time = time.perf_counter()

        result = self.classifier(
            text,
            truncation=True,
        )[0]

        inference_time_ms = round(
            (time.perf_counter() - start_time) * 1000,
            2,
        )

        label = result["label"].capitalize()
        confidence = round(
            float(result["score"]) * 100,
            2,
        )

        return {
            "success": True,
            "model": self.model_name,
            "task": self.task,
            "label": label,
            "confidence": confidence,
            "inference_time_ms": inference_time_ms,
        }

    def get_info(self) -> dict[str, Any]:
        """Return model information."""

        return {
            "name": self.model_name,
            "type": "Text Classification",
            "architecture": "RoBERTa",
            "task": "Sentiment Analysis",
            "classes": ["Negative", "Neutral", "Positive"],
            "pretrained": True,
            "loaded": self.loaded,
            "device": "CPU",
        }


text_classifier = TextClassifier()
