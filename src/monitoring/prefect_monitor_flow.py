# src/monitoring/prefect_monitor_flow.py
import sys, os
from io import StringIO
import boto3
import pandas as pd
from prefect import flow, task

# Ensure both original source path and the temp deployment path are covered
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from monitoring.drift_check import run_drift
from monitoring.alert import send_teams_alert
from monitoring.workflow_trigger import trigger_retrain

# --- Configuration ---
BUCKET_NAME = "mlops-project-artifacts-noura"
REFERENCE_PREFIX = "dataset/raw/Nasa-Bearing/1st_test/"
CURRENT_PREFIX = "dataset/drifted/1st_test/"
MAX_FILES = 10


def read_s3_file(s3_client, bucket, key):
    response = s3_client.get_object(Bucket=bucket, Key=key)
    return pd.read_csv(StringIO(response["Body"].read().decode()), sep="\t", header=None)


def load_data_from_s3(limit=MAX_FILES):
    s3 = boto3.client("s3")

    # List reference files
    ref_objects = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=REFERENCE_PREFIX).get("Contents", [])
    cur_objects = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=CURRENT_PREFIX).get("Contents", [])

    ref_keys = [obj["Key"] for obj in ref_objects if obj["Key"].endswith(".txt")][:limit]
    cur_keys = [obj["Key"] for obj in cur_objects if obj["Key"].endswith(".txt")]

    print(f"[DEBUG] S3 reference files: {len(ref_keys)}, current files: {len(cur_keys)}")

    # Load and concatenate
    reference = pd.concat((read_s3_file(s3, BUCKET_NAME, key) for key in ref_keys), ignore_index=True)
    current = pd.concat((read_s3_file(s3, BUCKET_NAME, key) for key in cur_keys), ignore_index=True)

    reference.columns = current.columns = [f"sensor_{i+1}" for i in range(reference.shape[1])]
    return reference, current


@task
def check_drift(reference, current):
    drift_score, drift_detected, _ = run_drift(reference, current)
    return drift_score, drift_detected


@flow
def monitor_pipeline():
    reference, current = load_data_from_s3()
    drift_score, drift_detected = check_drift(reference, current)

    if drift_detected or drift_score > 0.1:
        print("⚠️ Drift detected.")
        send_teams_alert("⚠️ Drift detected! Retraining pipeline started for bearing failure prediction.")
        trigger_retrain()
    else:
        print("✅ No significant drift detected.")


if __name__ == "__main__":
    monitor_pipeline()
