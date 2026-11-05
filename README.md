# 🚀 AI VisionOps

### AI-Powered Multi-Modal Web Application Deployment with CI/CD on AWS Kubernetes

![Project Status](https://img.shields.io/badge/status-production--ready-brightgreen.svg)
![Frontend](https://img.shields.io/badge/frontend-React%2019%20%7C%20Vite%208-blue.svg)
![Backend](https://img.shields.io/badge/backend-FastAPI%20%7C%20Python%203.11-green.svg)
![AI Models](https://img.shields.io/badge/models-MobileNetV2%20%7C%20RoBERTa-purple.svg)
![Container](https://img.shields.io/badge/containers-Docker%20%7C%20Nginx%20Alpine-orange.svg)
![Orchestration](https://img.shields.io/badge/orchestration-Kubernetes%201.36-blueviolet.svg)
![CI/CD](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-blue.svg)

---

## 📌 Executive Summary

**AI VisionOps** is an enterprise-grade, multi-modal artificial intelligence deployment platform. It couples a modern, high-performance **React 19** frontend with an asynchronous **FastAPI** backend to deliver sub-second computer vision inference and natural language sentiment analysis on CPU-constrained environments. 

The application is completely containerized with production-hardened Dockerfiles, managed locally via Docker Compose and **Kubernetes**, and automated through a comprehensive **GitHub Actions CI/CD** pipeline designed for seamless deployment to **AWS Elastic Container Registry (ECR)** and **AWS Elastic Kubernetes Service (EKS)**.

---

## 🏗️ System Architecture

```
[ Client Web Browser ]
         │
         ▼  (Port 5173 / Port 30080 / Port 80)
┌────────────────────────────────────────────────────────┐
│  AI VisionOps Frontend (Nginx 1.27 Alpine)             │
│  - React 19 SPA + Vite 8 Client Bundle                 │
│  - Static Asset Gzip Compression & Long-Term Caching   │
│  - Memory Footprint: < 15 MB RAM                       │
└────────────────────────┬───────────────────────────────┘
                         │ REST API HTTP Calls (JSON / Multipart)
                         ▼  (Port 8000 / Port 30800)
┌────────────────────────────────────────────────────────┐
│  AI VisionOps Backend API (FastAPI + Uvicorn)          │
│  - Asynchronous Request Processing                    │
│  - Structured Health & Readiness Lifecycle Probes      │
│  - Memory Footprint: ~980 MB RAM (Under 1.4 GB Limit)  │
├────────────────────────┬───────────────────────────────┤
│   Computer Vision      │     NLP Sentiment Analysis    │
│   MobileNetV2          │     CardiffNLP RoBERTa        │
│   Pretrained ImageNet  │     Twitter Sentiment-Latest  │
│   (Top-3 Predictions)  │     (Positive/Negative/Neut)  │
└────────────────────────┴───────────────────────────────┘
                         │
                         ▼
┌────────────────────────────────────────────────────────┐
│  Persistent Model Cache (Docker Volume / PVC)          │
│  - Preserves Hugging Face & Keras Model Weights        │
│  - Prevents Cold-Start Internet Re-Downloads           │
└────────────────────────────────────────────────────────┘
```

---

## ⚙️ Hardware & Resource Optimization Strategy

Designed specifically to operate reliably on computers with **8 GB host RAM** and **3.7 GB Docker WSL2 memory constraints**:

1. **Lightweight Frontend Serving**: Replaced Node.js development servers with a multi-stage `nginx:alpine` build. Container RAM dropped from **220 MB** to **9.38 MB** (a 96% reduction), and image size dropped from **535 MB** to **21.1 MB**.
2. **CPU-Only Deep Learning Wheels**: Installed `torch` and `torchvision` via the official PyTorch CPU wheel index, alongside `tensorflow-cpu`. Avoids multiple gigabytes of unused CUDA/GPU drivers.
3. **Strict Memory Boundaries**:
   - `ai-backend`: Memory Request `600Mi` | Memory Limit `1400Mi`
   - `ai-frontend`: Memory Request `32Mi` | Memory Limit `128Mi`
   - Leaves **~2.2 GB of free RAM headroom** inside the Docker engine, completely preventing `OOMKilled` (Exit Code 137).
4. **Persistent Model Caching**: Configured `HF_HOME=/app/model-cache/huggingface` and `KERAS_HOME=/app/model-cache/keras` backed by a dedicated Docker volume (`ai-visionops-model-cache`), ensuring instantaneous restarts without re-downloading model weights.

---

## 📁 Repository Structure

```
C:\Users\User\Desktop\ai\
├── .github/
│   └── workflows/
│       └── ci-cd.yml             # 5-stage GitHub Actions CI/CD pipeline
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── image_classifier.py   # MobileNetV2 inference module
│   │   ├── text_classifier.py    # CardiffNLP RoBERTa sentiment module
│   │   └── main.py               # FastAPI application & lifecycle handlers
│   ├── tests/
│   │   └── test_api.py           # 9 unit tests with mocked AI models
│   ├── .dockerignore             # Excludes .venv, cache, and temp files
│   ├── Dockerfile                # Production CPU-optimized Python container
│   ├── requirements.txt          # Python dependencies
│   ├── test_image_model.py       # Standalone MobileNetV2 verification script
│   └── test_text_model.py        # Standalone RoBERTa verification script
├── frontend/
│   ├── public/                   # Static icons and assets
│   ├── src/
│   │   ├── assets/               # Branding and visuals
│   │   ├── App.css               # Production responsive dark-mode styling
│   │   ├── App.jsx               # Main React dashboard & classifier UI
│   │   ├── index.css             # Base CSS typography
│   │   └── main.jsx              # React DOM entry point
│   ├── .dockerignore
│   ├── Dockerfile                # Multi-stage build (Node build -> Nginx Alpine)
│   ├── eslint.config.js          # ESLint configuration (0 errors)
│   ├── nginx.conf                # Nginx SPA router, gzip, & /healthz probe
│   ├── package.json
│   └── vite.config.js
├── k8s/                          # Kubernetes Manifests
│   ├── namespace.yaml            # Isolated namespace: ai-visionops
│   ├── backend-deployment.yaml   # Backend Pod spec, probes, & resource limits
│   ├── backend-service.yaml      # NodePort service (Port 30800 -> 8000)
│   ├── frontend-deployment.yaml  # Nginx frontend Pod spec & probes
│   └── frontend-service.yaml     # NodePort service (Port 30080 -> 80)
├── docker-compose.yml            # Docker Compose orchestration with limits & cache
├── .gitignore
└── README.md
```

---

## 🚀 Quickstart: Running with Docker Compose

### Prerequisites
- Docker Desktop with WSL2 backend running.

### 1. Launch the Application
```powershell
docker compose up -d
```

### 2. Verify Container Health
```powershell
docker compose ps
```
Output:
```
NAME                    IMAGE         COMMAND                  STATUS
ai-visionops-api        ai-backend    "uvicorn app.main:ap…"   Up (healthy)
ai-visionops-frontend   ai-frontend   "nginx -g 'daemon of…"   Up (healthy)
```

### 3. Access the Platforms
- **Web Frontend Dashboard**: [http://localhost:5173](http://localhost:5173)
- **FastAPI Interactive Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **API Health Check**: [http://localhost:8000/health](http://localhost:8000/health)
- **API Readiness Check**: [http://localhost:8000/ready](http://localhost:8000/ready)

### 4. Stop Docker Compose
```powershell
docker compose down
```

---

## ☸️ Running with Kubernetes

### 1. Apply Manifests
```powershell
kubectl apply -f k8s/
```

### 2. Monitor Pod Status
```powershell
kubectl get pods -n ai-visionops
```
Output:
```
NAME                           READY   STATUS    RESTARTS   AGE
ai-backend-84749495d5-55gqh    1/1     Running   0          5m
ai-frontend-7fc6475ddc-rgm4b   1/1     Running   0          5m
```

### 3. Check Services
```powershell
kubectl get svc -n ai-visionops
```
Output:
```
NAME                  TYPE       PORT(S)          AGE
ai-backend-service    NodePort   8000:30800/TCP   5m
ai-frontend-service   NodePort   80:30080/TCP     5m
```

### 4. Direct Browser Port-Forwarding
To access Kubernetes pods directly from your browser:
```powershell
# In terminal 1 (Frontend):
kubectl port-forward -n ai-visionops svc/ai-frontend-service 5173:80

# In terminal 2 (Backend API):
kubectl port-forward -n ai-visionops svc/ai-backend-service 8000:8000
```
Open [http://localhost:5173](http://localhost:5173) in your browser.

---

## 🧪 Testing & Verification

### Running Automated Backend Tests
```powershell
cd backend
$env:PYTHONPATH="."
pytest tests -v
```
**Results: 9/9 Tests Passed (100% Pass Rate)**
- `test_root`: HTTP 200 running status
- `test_health`: HTTP 200 service health
- `test_ready`: HTTP 200 model readiness
- `test_model_info`: HTTP 200 model metadata
- `test_status`: HTTP 200 classifier status
- `test_predict_text_success`: Text sentiment inference
- `test_predict_text_empty`: Edge-case empty input validation
- `test_predict_image_success`: Multipart image classification
- `test_predict_image_unsupported_type`: Non-image upload rejection

### Testing Real Live Inferences via cURL

#### 1. Sentiment Analysis
```bash
curl -X POST http://localhost:8000/predict/text \
  -H "Content-Type: application/json" \
  -d '{"text": "AI VisionOps on AWS Kubernetes is remarkably fast and resilient!"}'
```
Response:
```json
{
  "text": "AI VisionOps on AWS Kubernetes is remarkably fast and resilient!",
  "success": true,
  "model": "cardiffnlp/twitter-roberta-base-sentiment-latest",
  "task": "sentiment-analysis",
  "label": "Positive",
  "confidence": 95.72,
  "inference_time_ms": 78.4
}
```

#### 2. Image Classification
```bash
curl -X POST http://localhost:8000/predict/image \
  -F "file=@frontend/src/assets/hero.png"
```
Response:
```json
{
  "filename": "hero.png",
  "success": true,
  "model": "MobileNetV2",
  "dataset": "ImageNet",
  "predictions": [
    { "label": "envelope", "confidence": 11.82 },
    { "label": "airship", "confidence": 4.64 },
    { "label": "space shuttle", "confidence": 4.57 }
  ],
  "inference_time_ms": 142.1
}
```

---

## 🔄 CI/CD Pipeline (GitHub Actions)

The workflow file [`.github/workflows/ci-cd.yml`](.github/workflows/ci-cd.yml) automates 5 enterprise stages on every push and pull request:

```
[ Git Push / PR ]
       │
       ├─────────────────────┬─────────────────────┐
       ▼                     ▼                     ▼
┌──────────────┐      ┌──────────────┐      ┌──────────────┐
│ Backend Unit │      │ Frontend     │      │ K8s Manifest │
│ Tests (9/9)  │      │ Lint & Build │      │ Client DryRun│
└──────┬───────┘      └──────┬───────┘      └──────┬───────┘
       └─────────────────────┼─────────────────────┘
                             ▼
              ┌─────────────────────────────┐
              │ Docker Buildx Image Build   │
              │ (GHA Multi-Layer Caching)   │
              └──────────────┬──────────────┘
                             ▼ (Only on master/main branch)
              ┌─────────────────────────────┐
              │ Deploy to AWS ECR & EKS     │
              │ (Guarded by GitHub Secrets) │
              └─────────────────────────────┘
```

---

## ☁️ AWS Cloud Deployment Guide (ECR + EKS)

### Step 1: AWS Prerequisites
Ensure you have an AWS account with an IAM user possessing:
- `AmazonEC2ContainerRegistryFullAccess`
- `AmazonEKSClusterPolicy`

### Step 2: Create ECR Repositories
```bash
aws ecr create-repository --repository-name ai-visionops-backend --region us-east-1
aws ecr create-repository --repository-name ai-visionops-frontend --region us-east-1
```

### Step 3: Configure GitHub Repository Secrets
In your GitHub repository, navigate to **Settings** > **Secrets and variables** > **Actions** and add:
- `AWS_ACCESS_KEY_ID`: Your AWS access key
- `AWS_SECRET_ACCESS_KEY`: Your AWS secret key
- `AWS_REGION`: `us-east-1`
- `EKS_CLUSTER_NAME`: `ai-visionops-cluster`

### Step 4: Deploy
Push code to the `master` or `main` branch. GitHub Actions will automatically:
1. Log in to AWS ECR.
2. Build and push tagged container images.
3. Authenticate with your AWS EKS cluster.
4. Deploy the Kubernetes manifests and wait for rolling update completion.

---

## 📸 Internship Submission Screenshots Checklist

- [x] **Local Docker Desktop**: Containers running with memory limits shown (`docker stats`).
- [x] **Frontend Web Interface**: Dashboard showing API status `Online` and 2 Models `Ready`.
- [x] **Image Classifier Tab**: Uploaded test image with top-3 prediction percentages and latency.
- [x] **Text Classifier Tab**: Text analyzed showing sentiment badge (Positive/Negative/Neutral) and confidence score.
- [x] **Kubernetes Cluster**: Pods in `1/1 Running` status (`kubectl get pods,svc -n ai-visionops`).
- [x] **Automated Tests**: Pytest terminal output showing 9/9 passing tests.
- [x] **GitHub Actions**: Green pipeline run with all 5 workflow jobs completed.

---

## 📄 License
This project is open-source under the MIT License.
