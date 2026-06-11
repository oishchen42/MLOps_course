# 🚀 MLOps Infrastructure Project

A comprehensive, fully Dockerized MLOps environment designed to streamline the machine learning lifecycle. This project integrates best-in-class tools for data versioning, orchestration, experiment tracking, and model serving into a seamless, production-ready stack.

---

## ✨ Features

- **📦 Automated Data Versioning** — Manage datasets with Git-like semantics using **lakeFS**. Data is automatically loaded and versioned upon startup.
- **⚙️ Orchestration** — Define, schedule, and monitor data pipelines with **Dagster**.
- **📊 Experiment Tracking** — Log experiments, compare runs, and manage models with **MLflow**.
- **🔌 Model Serving** — Deploy and serve your models as a REST API using **FastAPI**.
- **🔄 Reproducibility** — Dockerized services ensure a consistent environment from development to production.

---

## 🏗️ Infrastructure Map

| Service | Host Port | Internal Port | Purpose |
|:---:|:---:|:---:|---|
| 🐙 Dagster | `3000` | `3000` | Data orchestration and pipeline execution |
| 🌊 lakeFS | `8000` | `8000` | Data versioning and storage |
| 🧪 MLflow | `5001` | `5000` | Experiment tracking and model registry |
| 🚀 FastAPI | `8080` | `8080` | REST API for real-time model serving |

---

## 🚀 Quick Start

Follow these steps to spin up the fully automated MLOps environment.

### Step 1: Environment Setup

Run the setup script from the project root. This prepares your local directories, downloads necessary data, installs `uv`, and generates the required `.env` configuration file containing your lakeFS keys.

```bash
bash setup.sh
```

### Step 2: Build and Launch the Stack

Bring up the entire infrastructure using Docker Compose. The configuration uses an initialization container (`lakefs-setup`) to automatically create your data repository and upload the raw CSV files.

```bash
docker compose build --no-cache
docker compose up -d
```

Monitor the automated data upload:

```bash
docker compose logs -f lakefs-setup
```

⏳ **Wait until you see `Data upload complete` before proceeding.**

### Step 3: Train the Champion Model

Before the API can serve predictions, execute the data pipeline to train and evaluate the models.

1. **Open the Dagster UI** at http://127.0.0.1:3000

2. **Trigger the pipeline** — Navigate to your assets and click **Materialize All** to trigger the `__ASSET_JOB`

3. **Monitor training** — Dagster will process the lakeFS data, train three models:
   - Base Linear Regression
   - XGBoost
   - HistGradientBoosting
   
   The best performing model will be automatically registered in MLflow under the `champion` alias.

4. **(Optional) View metrics** — Check training metrics and the model registry in the MLflow UI at http://127.0.0.1:5001

### Step 4: Serve Predictions

The FastAPI service automatically monitors MLflow. Once Dagster registers the champion model, the API is ready to accept HTTP POST requests.

**Endpoint:** http://127.0.0.1:8080/predict

If the API container was started before the model was trained, restart it to load the fresh model into memory:

```bash
docker compose restart api
```

---

## 🛠️ Troubleshooting

### 503 Service Unavailable (FastAPI)

**Problem:** POST request to the API returns a 503 error stating "Model is not yet trained and loaded".

**Solution:** Your Dagster pipeline has not yet successfully registered a model to the `champion` alias in MLflow. Run the pipeline in Dagster first (Step 3).

### 401 Unauthorized (lakeFS Authentication)

**Problem:** Dagster throws 401 Unauthorized errors when trying to read `lakefs://bike-rentals/...`

**Cause:** Your container volumes are out of sync with your `.env` keys.

**Solution:** Force a clean reset of the database and credentials:

```bash
docker compose down -v
docker compose build --no-cache
docker compose up -d
```

### Module Not Found (Dagster)

**Problem:** Dagster reports `No module named 'bikes'`

**Solution:** Ensure the Python path is correctly mapped in your `Dockerfile.dagster`:

```dockerfile
ENV PYTHONPATH=/opt/dagster/app/src
```

### Docker Cache Issues

**Problem:** Your Python code changes (e.g., in `api.py` or Dagster definitions) are not reflecting in the running environment.

**Solution:** Rebuild the images explicitly bypassing the cache:

```bash
docker compose build --no-cache
docker compose up -d
```