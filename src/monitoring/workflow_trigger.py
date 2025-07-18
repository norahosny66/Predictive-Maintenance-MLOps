# src/monitoring/workflow_trigger.py
import subprocess

def trigger_retrain():
    # Trigger retrain pipeline using Prefect
    subprocess.run(["prefect", "deploy", "retrain_pipeline"])

def switch_model():
    # Optional: use MLflow to switch model version
    pass
