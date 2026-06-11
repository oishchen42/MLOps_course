# 🚀 MLOps Infrastructure Project

This project provides a comprehensive, fully Dockerized MLOps environment designed to streamline the machine learning lifecycle. It integrates best-in-class tools for data versioning, orchestration, experiment tracking, and model serving.

## ✨ Features

-   **Data Versioning:** Manage your datasets with Git-like semantics using **lakeFS**.
-   **Orchestration:** Define, schedule, and monitor data pipelines with **Dagster**.
-   **Experiment Tracking:** Log experiments, compare runs, and manage models with **MLflow**.
-   **Model Serving:** Deploy and serve your models as a REST API using **FastAPI**.
-   **Reproducibility:** Dockerized services ensure a consistent environment from development to production.

## 🏗️ Infrastructure Map

Here are the services included in this MLOps stack:

| Service | Host Port | Internal Port | Purpose |
| :--- | :--- | :--- | :--- |
| 🐙 **Dagster** | `3000` | `3000` | Data orchestration |
| 🌊 **lakeFS** | `8000` | `8000` | Data versioning |
| 🧪 **MLflow** | `5001` | `5000` | Experiment tracking |
|  FastAPI | `8080` | `8080` | Model serving |

## 🚀 Quickstart Guide

Follow these steps to get the MLOps environment up and running.

### 1. Environment Setup

First, run the setup script from the project root. This will download the necessary data, install `uv` (a fast Python package installer), and generate the `.env` configuration file.

```bash
bash setup.sh
```

### 2. Configure lakeFS Credentials

1.  Navigate to the lakeFS UI at [http://127.0.0.1:8000](http://127.0.0.1:8000).
2.  Create an admin user.
3.  Go to the **Administration** > **Create Access Key** section and generate new credentials.
4.  Copy the **Access Key ID** and **Secret Access Key**.
5.  Open the `.env` file in the project root and paste your credentials:

```dotenv
LAKECTL_CREDENTIALS_ACCESS_KEY_ID="<YOUR_ACCESS_KEY_ID>"
LAKECTL_CREDENTIALS_SECRET_ACCESS_KEY="<YOUR_SECRET_ACCESS_KEY>"
```

### 3. Launch the Services

Bring up the entire stack using Docker Compose. The `-d` flag runs the containers in detached mode.

```bash
docker compose up -d
```

Once the services are running, you can access them at their respective ports.

---

## 🛠️ Troubleshooting

Here are solutions to some common issues you might encounter.

### Permission Errors with lakeFS

If the `lakefs` container exits with a `path provided is not writable` error, ensure the `user: "root"` configuration is present in your `docker-compose.yaml` under the `lakefs` service definition.

### Dagster "Module Not Found" Error

If Dagster reports `No module named 'bikes'`, you need to ensure the Python path is correctly set in `Dockerfile.dagster`. Add the following line to your Dockerfile:

```Dockerfile
ENV PYTHONPATH=/opt/dagster/app/src
```

This tells Python to look for modules in your `src` directory.

### Docker Cache Issues

If your code changes (e.g., in `api.py` or other source files) are not being reflected in the running containers, you may need to rebuild the images without using the cache.

```bash
docker compose build --no-cache
docker compose up -d
```

### API Connection Errors to MLflow

If the `api` container fails to connect to MLflow, it's likely because the MLflow tracking URI is hardcoded to a `localhost` address. Inside a Docker network, containers must use the service name as the hostname.

Ensure your `api.py` reads the tracking URI from an environment variable:

```python
import os

# Default to the Docker service name `mlflow` if the env var is not set
tracking_uri = os.getenv("MLFLOW_TRACKING_URI", "http://mlflow:5000")
mlflow.set_tracking_uri(tracking_uri)
```
