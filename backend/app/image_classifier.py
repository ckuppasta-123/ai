import io
import time
from typing import Any

import numpy as np
from PIL import Image
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import (
    decode_predictions,
    preprocess_input,
)


class ImageClassifier:
    """
    MobileNetV2 image classifier using ImageNet pretrained weights.
    """

    def __init__(self) -> None:
        self.model = None
        self.model_name = "MobileNetV2"
        self.dataset = "ImageNet"
        self.input_size = (224, 224)
        self.loaded = False

    def load(self) -> None:
        """Load the pretrained MobileNetV2 model."""
        if self.loaded:
            return

        self.model = MobileNetV2(
            weights="imagenet",
            include_top=True,
        )

        self.loaded = True

    def predict(
        self,
        image_bytes: bytes,
        top_k: int = 3,
    ) -> dict[str, Any]:
        """
        Run image classification.

        Args:
            image_bytes: Uploaded image as bytes.
            top_k: Number of predictions to return.

        Returns:
            Prediction results with confidence scores and inference time.
        """

        if not self.loaded:
            self.load()

        start_time = time.perf_counter()

        try:
            image = Image.open(io.BytesIO(image_bytes))

            # Convert to RGB so grayscale/RGBA images are handled safely.
            image = image.convert("RGB")

            # MobileNetV2 expects 224x224 input.
            image = image.resize(self.input_size)

            # Convert image to NumPy array.
            image_array = np.asarray(image, dtype=np.float32)

            # Add batch dimension: (224, 224, 3) -> (1, 224, 224, 3)
            image_array = np.expand_dims(image_array, axis=0)

            # MobileNetV2 preprocessing.
            image_array = preprocess_input(image_array)

            # Model inference.
            predictions = self.model.predict(
                image_array,
                verbose=0,
            )

            # Decode ImageNet predictions.
            decoded = decode_predictions(
                predictions,
                top=top_k,
            )[0]

            inference_time_ms = round(
                (time.perf_counter() - start_time) * 1000,
                2,
            )

            results = []

            for _, label, confidence in decoded:
                results.append(
                    {
                        "label": label.replace("_", " "),
                        "confidence": round(float(confidence) * 100, 2),
                    }
                )

            return {
                "success": True,
                "model": self.model_name,
                "dataset": self.dataset,
                "predictions": results,
                "inference_time_ms": inference_time_ms,
            }

        except Exception as exc:
            raise ValueError(
                f"Unable to process the image: {exc}"
            ) from exc

    def get_info(self) -> dict[str, Any]:
        """Return model information."""
        return {
            "name": self.model_name,
            "type": "Image Classification",
            "architecture": "MobileNetV2",
            "dataset": self.dataset,
            "input_size": "224x224",
            "pretrained": True,
            "loaded": self.loaded,
        }


# Create a reusable classifier instance.
image_classifier = ImageClassifier()