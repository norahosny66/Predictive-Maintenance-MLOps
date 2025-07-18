
from evidently import Report
from evidently.metrics import ValueDrift

def run_drift(reference_df, current_df):
    metrics = [ValueDrift(column_name=col) for col in reference_df.columns]

    report = Report(metrics=metrics)
    report.run(reference_data=reference_df, current_data=current_df)
    result = report.as_dict()

    drift_scores = []
    drift_flags = []

    for metric in result['metrics']:
        if metric['metric'] == 'ValueDrift':
            drift_scores.append(metric['result']['drift_score'])
            drift_flags.append(metric['result']['drift_detected'])

    drift_score = sum(drift_scores) / len(drift_scores) if drift_scores else 0
    drift_detected = any(drift_flags)

    return drift_score, drift_detected, result
