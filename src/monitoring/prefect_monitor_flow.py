# src/monitoring/prefect_monitor_flow.py
import sys, os
# Ensure both original source path and the temp deployment path are covered

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from prefect import flow, task
import pandas as pd
from pathlib import Path
from monitoring.drift_check import run_drift
from monitoring.alert import send_teams_alert
from monitoring.workflow_trigger import trigger_retrain

def load_data(limit=10):
    # Get first N reference files
    ref_files = list(Path("/opt/flows/predictive_maintenance_project/data/raw/Nasa-Bearing/1st_test/1st_test").glob("*"))[:limit]
    cur_files = list(Path("/opt/flows/predictive_maintenance_project/data/drifted/1st_test").glob("*"))
    print(f"[DEBUG] Current files loaded: {len(cur_files)}")
    # Concatenate all reference and current files
    reference = pd.concat((pd.read_csv(f, sep="\t", header=None) for f in ref_files), ignore_index=True)
    current = pd.concat((pd.read_csv(f, sep="\t", header=None) for f in cur_files), ignore_index=True)

    # Assign sensor column names
    reference.columns = current.columns = [f"sensor_{i+1}" for i in range(reference.shape[1])]

    return reference, current


@task
def check_drift(reference, current):
    drift_score, drift_detected, _ = run_drift(reference, current)
    return drift_score, drift_detected

@flow
def monitor_pipeline():
    reference, current = load_data()
    drift_score, drift_detected = check_drift(reference, current)

    if drift_detected or drift_score > 0.1 :
        print(" Drift detected.")
        send_teams_alert("⚠️ Drift detected! Retraining pipeline started for bearing failure prediction.")
        trigger_retrain()
    else:
        print("✅ No significant drift detected.")

if __name__ == "__main__":
    monitor_pipeline()
