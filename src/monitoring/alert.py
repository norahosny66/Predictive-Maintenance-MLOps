# src/monitoring/alert.py
import requests

def send_slack_alert(message):
    webhook_url = "https://hooks.slack.com/services/your/webhook/url"
    payload = {"text": message}
    requests.post(webhook_url, json=payload)
