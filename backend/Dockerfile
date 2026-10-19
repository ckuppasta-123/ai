
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    HF_HOME=/app/model-cache \
    TF_CPP_MIN_LOG_LEVEL=2

WORKDIR /app

# Install only the OS utilities required by Python packages.
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Install CPU-based PyTorch first to avoid pulling CUDA packages.
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
      tensorflow \
      transformers

COPY app ./app

# Create a non-root user for safer runtime execution.
RUN useradd --create-home --uid 10001 appuser && \
    mkdir -p /app/model-cache && \
    chown -R appuser:appuser /app

USER appuser

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
