import logging
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.image_classifier import image_classifier
from app.text_classifier import text_classifier


# ---------------------------------------------------------
# Logging
# ---------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger("ai-visionops")


# ---------------------------------------------------------
# Application startup / shutdown
# ---------------------------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting AI VisionOps backend...")

    # Load both models during application startup.
    logger.info("Loading MobileNetV2...")
    image_classifier.load()

    logger.info("Loading DistilBERT...")
    text_classifier.load()

    logger.info("All AI models loaded successfully.")

    yield

    logger.info("Shutting down AI VisionOps backend...")


# ---------------------------------------------------------
# FastAPI application
# ---------------------------------------------------------

app = FastAPI(
    title="AI VisionOps API",
    description=(
        "Multi-modal AI classification API using "
        "MobileNetV2 for images and DistilBERT for text."
    ),
    version="1.0.0",
    lifespan=lifespan,
)


# ---------------------------------------------------------
# CORS
# ---------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------
# Request models
# ---------------------------------------------------------

class TextPredictionRequest(BaseModel):
    text: str


# ---------------------------------------------------------
# Root
# ---------------------------------------------------------

@app.get("/")
async def root():
    return {
        "application": "AI VisionOps",
        "description": "Multi-modal AI classification platform",
        "version": "1.0.0",
        "status": "running",
    }


# ---------------------------------------------------------
# Health
# ---------------------------------------------------------

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "service": "ai-visionops-backend",
    }


# ---------------------------------------------------------
# Readiness
# ---------------------------------------------------------

@app.get("/ready")
async def readiness():
    if not image_classifier.loaded or not text_classifier.loaded:
        raise HTTPException(
            status_code=503,
            detail="AI models are not ready.",
        )

    return {
        "status": "ready",
        "image_model_loaded": image_classifier.loaded,
        "text_model_loaded": text_classifier.loaded,
    }


# ---------------------------------------------------------
# Model information
# ---------------------------------------------------------

@app.get("/model-info")
async def model_info():
    return {
        "image_model": image_classifier.get_info(),
        "text_model": text_classifier.get_info(),
    }


# ---------------------------------------------------------
# Image prediction
# ---------------------------------------------------------

@app.post("/predict/image")
async def predict_image(
    file: UploadFile = File(...),
):
    allowed_types = {
        "image/jpeg",
        "image/png",
        "image/webp",
    }

    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail=(
                "Unsupported image type. "
                "Use JPEG, PNG, or WebP."
            ),
        )

    # 8 MB maximum upload size.
    max_size = 8 * 1024 * 1024

    image_bytes = await file.read()

    if len(image_bytes) > max_size:
        raise HTTPException(
            status_code=413,
            detail="Image size must be less than 8 MB.",
        )

    if not image_bytes:
        raise HTTPException(
            status_code=400,
            detail="Uploaded image is empty.",
        )

    try:
        result = image_classifier.predict(
            image_bytes=image_bytes,
            top_k=3,
        )

        return {
            "filename": file.filename,
            **result,
        }

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        logger.exception("Image prediction failed.")

        raise HTTPException(
            status_code=500,
            detail="Image prediction failed.",
        ) from exc


# ---------------------------------------------------------
# Text prediction
# ---------------------------------------------------------

@app.post("/predict/text")
async def predict_text(
    request: TextPredictionRequest,
):
    text = request.text.strip()

    if not text:
        raise HTTPException(
            status_code=400,
            detail="Text cannot be empty.",
        )

    try:
        result = text_classifier.predict(text)

        return {
            "text": text,
            **result,
        }

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        logger.exception("Text prediction failed.")

        raise HTTPException(
            status_code=500,
            detail="Text prediction failed.",
        ) from exc


# ---------------------------------------------------------
# Application status
# ---------------------------------------------------------

@app.get("/status")
async def status():
    return {
        "application": "AI VisionOps",
        "status": "running",
        "image_classifier": (
            "ready" if image_classifier.loaded else "not_ready"
        ),
        "text_classifier": (
            "ready" if text_classifier.loaded else "not_ready"
        ),
    }