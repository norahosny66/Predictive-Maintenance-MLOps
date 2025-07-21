from evidently import Report
from evidently.metrics import ValueDrift
import json

def run_drift(reference_df, current_df, drift_threshold=10):
    metrics = [ValueDrift(column=col) for col in reference_df.columns]
    report = Report(metrics=metrics)
    snapshot = report.run(reference_data=reference_df, current_data=current_df)
    result = snapshot.dict()

    drift_scores = []
    for metric in result.get("metrics", []):
        metric_id = metric.get("metric_id", "").lower()
        if "valuedrift" in metric_id:  # match the JSON keys
            score = metric.get("value", 0)
            drift_scores.append(score)

    avg_drift_score = sum(drift_scores) / len(drift_scores) if drift_scores else 0
    drift_detected = any(score > drift_threshold for score in drift_scores)

    print(f"[DEBUG] Drift scores per sensor: {drift_scores}")
    print(f"[DEBUG] Average Drift Score: {avg_drift_score:.2f} | Threshold: {drift_threshold}")
    print(f"[DEBUG] Drift Detected? {'YES' if drift_detected else 'NO'}")

    return avg_drift_score, drift_detected, result

