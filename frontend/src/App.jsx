import { useEffect, useState } from "react";
import {
  Activity,
  Brain,
  CheckCircle2,
  Cloud,
  FileImage,
  Gauge,
  Image as ImageIcon,
  MessageSquareText,
  Server,
  ShieldCheck,
  Sparkles,
  Upload,
  Zap,
} from "lucide-react";

import "./App.css";

const API_BASE_URL = "http://127.0.0.1:8000";

function App() {
  const [activePage, setActivePage] = useState("dashboard");

  const [apiStatus, setApiStatus] = useState("checking");
  const [modelsReady, setModelsReady] = useState(false);

  const [imageFile, setImageFile] = useState(null);
  const [imagePreview, setImagePreview] = useState("");
  const [imageResult, setImageResult] = useState(null);
  const [imageLoading, setImageLoading] = useState(false);
  const [imageError, setImageError] = useState("");

  const [text, setText] = useState("");
  const [textResult, setTextResult] = useState(null);
  const [textLoading, setTextLoading] = useState(false);
  const [textError, setTextError] = useState("");

  const [modelInfo, setModelInfo] = useState(null);

  useEffect(() => {
    checkBackend();
  }, []);

  const checkBackend = async () => {
    try {
      const healthResponse = await fetch(`${API_BASE_URL}/health`);
      const readyResponse = await fetch(`${API_BASE_URL}/ready`);
      const modelResponse = await fetch(`${API_BASE_URL}/model-info`);

      if (!healthResponse.ok) {
        throw new Error("Backend unavailable");
      }

      const readyData = await readyResponse.json();
      const modelData = await modelResponse.json();

      setApiStatus("online");
      setModelsReady(readyData.status === "ready");
      setModelInfo(modelData);
    } catch (error) {
      console.error(error);
      setApiStatus("offline");
      setModelsReady(false);
    }
  };

  const handleImageChange = (event) => {
    const file = event.target.files?.[0];

    if (!file) {
      return;
    }

    setImageFile(file);
    setImageResult(null);
    setImageError("");

    const previewUrl = URL.createObjectURL(file);
    setImagePreview(previewUrl);
  };

  const predictImage = async () => {
    if (!imageFile) {
      setImageError("Please select an image first.");
      return;
    }

    setImageLoading(true);
    setImageError("");
    setImageResult(null);

    try {
      const formData = new FormData();
      formData.append("file", imageFile);

      const response = await fetch(
        `${API_BASE_URL}/predict/image`,
        {
          method: "POST",
          body: formData,
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Image prediction failed.");
      }

      setImageResult(data);
    } catch (error) {
      setImageError(error.message);
    } finally {
      setImageLoading(false);
    }
  };

  const predictText = async () => {
    if (!text.trim()) {
      setTextError("Please enter some text.");
      return;
    }

    setTextLoading(true);
    setTextError("");
    setTextResult(null);

    try {
      const response = await fetch(
        `${API_BASE_URL}/predict/text`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            text: text.trim(),
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Text prediction failed.");
      }

      setTextResult(data);
    } catch (error) {
      setTextError(error.message);
    } finally {
      setTextLoading(false);
    }
  };

  const renderConfidence = (confidence) => {
    return (
      <div className="confidence-row">
        <div className="confidence-bar">
          <div
            className="confidence-fill"
            style={{ width: `${confidence}%` }}
          />
        </div>

        <span>{confidence.toFixed(2)}%</span>
      </div>
    );
  };

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-icon">
            <Brain size={24} />
          </div>

          <div>
            <h1>AI VisionOps</h1>
            <span>AI Deployment Platform</span>
          </div>
        </div>

        <nav className="sidebar-nav">
          <button
            className={activePage === "dashboard" ? "nav-item active" : "nav-item"}
            onClick={() => setActivePage("dashboard")}
          >
            <Gauge size={19} />
            Dashboard
          </button>

          <button
            className={activePage === "image" ? "nav-item active" : "nav-item"}
            onClick={() => setActivePage("image")}
          >
            <ImageIcon size={19} />
            Image Classifier
          </button>

          <button
            className={activePage === "text" ? "nav-item active" : "nav-item"}
            onClick={() => setActivePage("text")}
          >
            <MessageSquareText size={19} />
            Text Classifier
          </button>
        </nav>

        <div className="sidebar-bottom">
          <div className="deployment-card">
            <div className="deployment-icon">
              <Cloud size={18} />
            </div>

            <div>
              <strong>Deployment Ready</strong>
              <span>Docker · Kubernetes · AWS</span>
            </div>
          </div>

          <div className="version">
            AI VisionOps v1.0.0
          </div>
        </div>
      </aside>

      <main className="main-content">
        <header className="topbar">
          <div>
            <p className="eyebrow">MULTI-MODAL AI PLATFORM</p>
            <h2>
              {activePage === "dashboard" && "AI Operations Dashboard"}
              {activePage === "image" && "Image Classification"}
              {activePage === "text" && "Text Classification"}
            </h2>
          </div>

          <div className="system-status">
            <span
              className={`status-dot ${
                apiStatus === "online" ? "online" : "offline"
              }`}
            />

            <span>
              {apiStatus === "online"
                ? "API Online"
                : apiStatus === "checking"
                ? "Checking API..."
                : "API Offline"}
            </span>
          </div>
        </header>

        {activePage === "dashboard" && (
          <section className="page-content">
            <div className="hero-card">
              <div className="hero-content">
                <div className="hero-badge">
                  <Sparkles size={15} />
                  AI POWERED
                </div>

                <h3>
                  Intelligent classification.
                  <br />
                  <span>Production-ready deployment.</span>
                </h3>

                <p>
                  Analyze images and text using pretrained deep-learning
                  models through a scalable FastAPI backend.
                </p>

                <div className="hero-actions">
                  <button
                    className="primary-button"
                    onClick={() => setActivePage("image")}
                  >
                    <ImageIcon size={18} />
                    Try Image AI
                  </button>

                  <button
                    className="secondary-button"
                    onClick={() => setActivePage("text")}
                  >
                    <MessageSquareText size={18} />
                    Try Text AI
                  </button>
                </div>
              </div>

              <div className="hero-visual">
                <div className="orb orb-one" />
                <div className="orb orb-two" />

                <div className="neural-card">
                  <Brain size={48} />
                  <strong>AI Core</strong>
                  <span>2 Models Active</span>
                </div>
              </div>
            </div>

            <div className="stats-grid">
              <div className="stat-card">
                <div className="stat-icon purple">
                  <Brain size={21} />
                </div>
                <span>AI Models</span>
                <strong>2</strong>
                <small>MobileNetV2 + DistilBERT</small>
              </div>

              <div className="stat-card">
                <div className="stat-icon green">
                  <Server size={21} />
                </div>
                <span>Backend</span>
                <strong>{apiStatus === "online" ? "Online" : "Offline"}</strong>
                <small>FastAPI REST API</small>
              </div>

              <div className="stat-card">
                <div className="stat-icon blue">
                  <ShieldCheck size={21} />
                </div>
                <span>Model Status</span>
                <strong>{modelsReady ? "Ready" : "Loading"}</strong>
                <small>Inference available</small>
              </div>

              <div className="stat-card">
                <div className="stat-icon orange">
                  <Zap size={21} />
                </div>
                <span>Deployment</span>
                <strong>Cloud Ready</strong>
                <small>AWS + Kubernetes</small>
              </div>
            </div>

            <div className="section-heading">
              <div>
                <p className="eyebrow">MODEL REGISTRY</p>
                <h3>AI Models</h3>
              </div>
            </div>

            <div className="model-grid">
              <div className="model-card">
                <div className="model-card-header">
                  <div className="model-logo image-logo">
                    <FileImage size={22} />
                  </div>

                  <span className="ready-badge">
                    <CheckCircle2 size={14} />
                    Ready
                  </span>
                </div>

                <h4>MobileNetV2</h4>

                <p>
                  Image classification model pretrained on ImageNet.
                </p>

                <div className="model-meta">
                  <span>224 × 224</span>
                  <span>ImageNet</span>
                </div>
              </div>

              <div className="model-card">
                <div className="model-card-header">
                  <div className="model-logo text-logo">
                    <MessageSquareText size={22} />
                  </div>

                  <span className="ready-badge">
                    <CheckCircle2 size={14} />
                    Ready
                  </span>
                </div>

                <h4>DistilBERT</h4>

                <p>
                  Transformer model optimized for sentiment classification.
                </p>

                <div className="model-meta">
                  <span>CPU</span>
                  <span>SST-2</span>
                </div>
              </div>
            </div>
          </section>
        )}

        {activePage === "image" && (
          <section className="page-content">
            <div className="classifier-header">
              <div>
                <p className="eyebrow">COMPUTER VISION</p>
                <h3>Image Classification</h3>
                <p>
                  Upload an image and let MobileNetV2 identify the most
                  likely ImageNet classes.
                </p>
              </div>

              <div className="model-pill">
                <Brain size={17} />
                MobileNetV2
              </div>
            </div>

            <div className="classifier-grid">
              <div className="upload-card">
                <label className="upload-zone">
                  <input
                    type="file"
                    accept="image/jpeg,image/png,image/webp"
                    onChange={handleImageChange}
                  />

                  {imagePreview ? (
                    <img
                      src={imagePreview}
                      alt="Selected preview"
                      className="image-preview"
                    />
                  ) : (
                    <>
                      <div className="upload-icon">
                        <Upload size={27} />
                      </div>

                      <strong>Upload an image</strong>

                      <span>
                        PNG, JPG or WebP · Maximum 8 MB
                      </span>
                    </>
                  )}
                </label>

                {imageFile && (
                  <div className="selected-file">
                    <FileImage size={18} />
                    <span>{imageFile.name}</span>
                  </div>
                )}

                <button
                  className="primary-button full-width"
                  onClick={predictImage}
                  disabled={imageLoading || !imageFile}
                >
                  {imageLoading ? (
                    <>
                      <span className="spinner" />
                      Analyzing...
                    </>
                  ) : (
                    <>
                      <Sparkles size={18} />
                      Analyze Image
                    </>
                  )}
                </button>

                {imageError && (
                  <div className="error-message">
                    {imageError}
                  </div>
                )}
              </div>

              <div className="result-card">
                <div className="result-header">
                  <div>
                    <p className="eyebrow">INFERENCE RESULT</p>
                    <h3>Top Predictions</h3>
                  </div>

                  <Activity size={20} />
                </div>

                {!imageResult && (
                  <div className="empty-result">
                    <ImageIcon size={42} />
                    <strong>No prediction yet</strong>
                    <span>
                      Upload an image and click Analyze Image.
                    </span>
                  </div>
                )}

                {imageResult && (
                  <div className="prediction-list">
                    {imageResult.predictions.map((prediction, index) => (
                      <div className="prediction-item" key={prediction.label}>
                        <div className="prediction-title">
                          <span className="rank">
                            #{index + 1}
                          </span>

                          <strong>{prediction.label}</strong>
                        </div>

                        {renderConfidence(prediction.confidence)}
                      </div>
                    ))}

                    <div className="inference-time">
                      <span>Inference time</span>
                      <strong>
                        {imageResult.inference_time_ms} ms
                      </strong>
                    </div>
                  </div>
                )}
              </div>
            </div>
          </section>
        )}

        {activePage === "text" && (
          <section className="page-content">
            <div className="classifier-header">
              <div>
                <p className="eyebrow">NATURAL LANGUAGE PROCESSING</p>
                <h3>Text Classification</h3>
                <p>
                  Analyze the sentiment of text using a pretrained
                  DistilBERT model.
                </p>
              </div>

              <div className="model-pill">
                <Brain size={17} />
                DistilBERT
              </div>
            </div>

            <div className="text-classifier-grid">
              <div className="text-input-card">
                <label htmlFor="text-input">
                  Enter text to analyze
                </label>

                <textarea
                  id="text-input"
                  value={text}
                  onChange={(event) => setText(event.target.value)}
                  placeholder="Example: I really enjoyed using this application..."
                  maxLength={2000}
                />

                <div className="character-count">
                  {text.length} / 2000
                </div>

                <button
                  className="primary-button full-width"
                  onClick={predictText}
                  disabled={textLoading || !text.trim()}
                >
                  {textLoading ? (
                    <>
                      <span className="spinner" />
                      Analyzing...
                    </>
                  ) : (
                    <>
                      <Sparkles size={18} />
                      Analyze Sentiment
                    </>
                  )}
                </button>

                {textError && (
                  <div className="error-message">
                    {textError}
                  </div>
                )}
              </div>

              <div className="result-card sentiment-card">
                <div className="result-header">
                  <div>
                    <p className="eyebrow">INFERENCE RESULT</p>
                    <h3>Sentiment</h3>
                  </div>

                  <MessageSquareText size={20} />
                </div>

                {!textResult && (
                  <div className="empty-result">
                    <MessageSquareText size={42} />
                    <strong>No prediction yet</strong>
                    <span>
                      Enter text and click Analyze Sentiment.
                    </span>
                  </div>
                )}

                {textResult && (
                  <div className="sentiment-result">
                    <div
                      className={`sentiment-badge ${
                        textResult.label.toLowerCase()
                      }`}
                    >
                      <CheckCircle2 size={21} />
                      {textResult.label}
                    </div>

                    <div className="large-confidence">
                      <span>Confidence</span>
                      <strong>
                        {textResult.confidence.toFixed(2)}%
                      </strong>
                    </div>

                    <div className="confidence-bar large">
                      <div
                        className="confidence-fill"
                        style={{
                          width: `${textResult.confidence}%`,
                        }}
                      />
                    </div>

                    <div className="inference-time">
                      <span>Inference time</span>
                      <strong>
                        {textResult.inference_time_ms} ms
                      </strong>
                    </div>
                  </div>
                )}
              </div>
            </div>
          </section>
        )}
      </main>
    </div>
  );
}

export default App;