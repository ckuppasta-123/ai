FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    HF_HOME=/app/model-cache/huggingface \
    KERAS_HOME=/app/model-cache/keras \
    TF_CPP_MIN_LOG_LEVEL=2

WORKDIR /app

# Install only the OS utilities required by Python packages.
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Install CPU-based PyTorch and CPU-based TensorFlow to minimize memory & image size
RUN python -m pip install --upgrade pip && \
    python -m pip install --no-cache-dir \
      torch torchvision \
      --index-url https://download.pytorch.org/whl/cpu && \
    python -m pip install --no-cache-dir \
      fastapi \
      "uvicorn[standard]" \
      python-multipart \
      pillow \
      numpy \
      tensorflow-cpu \
      transformers

COPY app ./app

# Create a non-root user for safer runtime execution and ensure cache directory permissions
RUN useradd --create-home --uid 10001 appuser && \
    mkdir -p /app/model-cache/huggingface /app/model-cache/keras && \
    chown -R appuser:appuser /app

USER appuser

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
