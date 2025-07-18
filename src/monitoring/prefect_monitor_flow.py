# src/monitoring/prefect_monitor_flow.py
from prefect import flow, task
import pandas as pd
from monitoring.drift_check import run_drift
from monitoring.alert import send_slack_alert
from monitoring.workflow_trigger import trigger_retrain

@task
def load_data():
    reference = pd.read_csv("data/reference.csv")
    current = pd.read_csv("data/current.csv")
    return reference, current

@task
def check_drift(reference, current):
    drift_score, drift_detected, _ = run_drift(reference, current)
    return drift_score, drift_detected

@flow
def monitor_pipeline():
    reference, current = load_data()
    drift_score, drift_detected = check_drift(reference, current)

    if drift_detected:
        send_slack_alert(f"[ALERT] Drift detected! Drift score: {drift_score:.2f}")
        trigger_retrain()
    else:
        print("✅ No significant drift detected.")

if __name__ == "__main__":
    monitor_pipeline()
