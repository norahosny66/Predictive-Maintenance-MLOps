# Predictive Maintenance MLOps Pipeline

![Terraform](https://img.shields.io/badge/Provisioning-Terraform-623CE4?logo=terraform)
![Ansible](https://img.shields.io/badge/Configuration-Ansible-EE0000?logo=ansible)
![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Prefect](https://img.shields.io/badge/Orchestration-Prefect-ffb400.svg)
![MLflow](https://img.shields.io/badge/Experiment%20Tracking-MLflow-green.svg)
![CI/CD](https://img.shields.io/badge/CI/CD-Jenkins-orange.svg)
![License](https://img.shields.io/badge/License-MIT-lightgrey.svg)

---

## Overview

This repository implements a **production-grade MLOps pipeline** for **predictive maintenance of rotating machinery (bearings)**, using the [NASA Bearing Dataset](https://ti.arc.nasa.gov/tech/dash/groups/pcoe/prognostic-data-repository/).

The project automates:
- **EC2 &s3 provisioning on AWS** (via Terraform)
- **EC2 Infra Configuration** (via Ansible)
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
### 2. ☁️ Provision Infrastructure (Terraform)
```bash
cd terraform/
terraform init
terraform plan 
terraform apply
```
This will create:

EC2 instance with IAM Role

S3 bucket for model/data storage

Security groups with necessary ports open
### 3. Update Inventory for Ansible

```bash
cd ../ansible/
echo -e "[mlops]\n<your-ec2-public-ip>" > inventory.yml
```
### 4. ⚙️ Configure EC2 (Ansible)
```bash
ansible-playbook -i inventory.yml mlflow.yml
ansible-playbook -i inventory.yml prefect.yml
ansible-playbook -i inventory.yml jenkins.yml
```
### 5. 📤 Upload Data to S3

### 6. Register & Run Prefect Flow
Build and apply Prefect deployment:
```bash
prefect deployment build pipeline.py:train_and_monitor -n "prod-flow"
prefect deployment apply train_and_monitor-deployment.yaml
prefect agent start
```
And do the same for monitoring pipeline
# MLflow tracking server

Access UIs:

Prefect → http://<ec2-ip>:4200

MLflow → http://<ec2-ip>:5000

Jenkins → http://<ec2-ip>:8080


### Simulate Drift Detection & Retrain
```bash
docker exec -it prefect-prefect-agent-1  bash
prefect deployment apply prefect/monitor_pipeline-deployment.yaml
```
This will:

Detect drift (via Evidently AI)

Trigger retraining

Send a Teams alert (webhook must be configured in your Microsoft Teams and edited in alert.py )


## 🙋‍♀️ Maintainer

**Noura Hosny**  
SRE | Cloud & Automation Enthusiast  
📧 Feel free to reach out for collaboration.

