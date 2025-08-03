# Predictive Maintenance MLOps Pipeline

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Prefect](https://img.shields.io/badge/Orchestration-Prefect-ffb400.svg)
![MLflow](https://img.shields.io/badge/Experiment%20Tracking-MLflow-green.svg)
![CI/CD](https://img.shields.io/badge/CI/CD-Jenkins-orange.svg)
![License](https://img.shields.io/badge/License-MIT-lightgrey.svg)

---

## Overview

This repository implements a **production-grade MLOps pipeline** for **predictive maintenance of rotating machinery (bearings)**, using the [NASA Bearing Dataset](https://ti.arc.nasa.gov/tech/dash/groups/pcoe/prognostic-data-repository/).

The project automates:
- **Model training, tuning, and serving**
- **Data drift detection** (via [Evidently AI](https://evidentlyai.com/))
- **Experiment tracking and model registry** (via MLflow)
- **Workflow orchestration** (via Prefect)
- **Continuous Integration & Delivery** (via Jenkins)
- **Alerting via Microsoft Teams**

Runs entirely on a **local VM (Docker-based)** but is built to be **cloud-ready** (AWS/GCP) without Kubernetes.

---

## Problem Statement

Industrial equipment failures, such as bearing breakdowns, lead to:
- Expensive **unplanned downtime**
- Higher **maintenance expenses**
- Significant **safety risks**

Traditional time-based maintenance schedules waste resources and fail to prevent unexpected failures.

**Goal:**  
Predict failures **before they happen** by:
1. Analyzing vibration and sensor time-series data.
2. Building ML models to predict Remaining Useful Life (RUL) or failure probability.
3. Detecting **data drift** and **performance degradation** automatically.
4. Triggering **retraining and alerts** when model reliability drops.

---

## Solution Architecture

### Workflow

             ┌──────────────────────────┐
             │   Raw Sensor Data (CSV)  │
             └──────────────┬───────────┘
                            │
                            ▼
                 Data Preprocessing & Splits
                            │
                            ▼
     ┌────────────────────────────────────────────┐
     │     Model Training & Hyperparameter Tuning │
     │      (RandomForestRegressor + Hyperopt)    │
     └───────────────────┬────────────────────────┘
                         │
                 Logs Metrics & Artifacts
                         │
                         ▼
               MLflow Tracking & Registry
                         │
                         ▼
    ┌─────────────────────────────┐
    │   FastAPI Model Serving     │
    │ (Production-tagged Model)   │
    └───────────────┬─────────────┘
                    │
┌────────────────────┴─────────────────────┐
│ │
▼ ▼
Drift Detection (Evidently AI) Teams Notifications
│ │
│ Drift > Threshold? │
└───────────────Yes───────────────► Retrain Trigger (Prefect Flow)


---

## Quickstart

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/predictive-maintenance-mlops.git
cd predictive-maintenance-mlops
```
### 2. Build the Custom Prefect Image

```bash
cd predictive-maintenance-mlops
docker build -f prefect/Dockerfile -t prefect_image .
```
This image includes:

Prefect 2.x with all Python dependencies (MLflow, Evidently, Hyperopt, etc.)

Auto-start configuration for the Prefect agent.
### 3. Start Services (Prefect + MLflow + Agent)
Navigate to the prefect directory (where the docker-compose.yml is) and launch:

```bash
cd prefect
docker compose up -d
```
This starts:

Prefect Orion server (workflow orchestration)

Prefect agent (auto-starts to run flows)

# MLflow tracking server

Access UIs:

Prefect → http://localhost:4200

MLflow → http://localhost:5000

### 4. Trigger the Training Pipeline
```bash
docker compose exec prefect prefect deployment run bearing-prediction/main
```
### 5. Simulate Drift Detection & Retrain
```bash
docker exec -it prefect-prefect-agent-1  bash
prefect deployment apply prefect/monitor_pipeline-deployment.yaml
```
This will:

Detect drift (via Evidently AI)

Trigger retraining

Send a Teams alert (webhook must be configured in your Microsoft Teams and edited in alert.py )

