import time
import json
import requests  # <-- Make sure this is imported
from functools import wraps
from google.cloud import bigquery

# 1. PASTE YOUR SLACK WEBHOOK URL HERE
SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/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"

def send_slack_notification(payload: dict):
    """Sends a cleanly formatted alert to Slack."""
    if "YOUR/WEBHOOK/URL" in SLACK_WEBHOOK_URL:
        print("⚠️ Slack URL not set. Skipping notification.")
        return

    # Color code: Green for success, Red for failure
    color = "#36a64f" if payload["status"] == "SUCCESS" else "#ff0000"
    emoji = "✅" if payload["status"] == "SUCCESS" else "🚨"

    slack_data = {
        "attachments": [
            {
                "color": color,
                "title": f"{emoji} Pipeline Stage: {payload['stage']}",
                "fields": [
                    {"title": "Status", "value": payload["status"], "short": True},
                    {"title": "Duration", "value": f"{payload['duration_seconds']}s", "short": True},
                    {"title": "Error Message", "value": str(payload["error_message"]), "short": False}
                ],
                "footer": "Data Pipeline Monitor Framework",
                "ts": int(time.time())
            }
        ]
    }

    try:
        response = requests.post(SLACK_WEBHOOK_URL, json=slack_data, headers={'Content-Type': 'application/json'})
        if response.status_code != 200:
            print(f"❌ Slack API returned an error: {response.status_code}, {response.text}")
    except Exception as e:
        print(f"❌ Failed to connect to Slack webhook: {e}")


def pipeline_orchestrator(stage_name: str, max_retries: int = 1, delay_seconds: int = 5):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 0
            while attempt <= max_retries:
                start_time = time.time()
                job_status = "SUCCESS"
                error_msg = None
                try:
                    if attempt > 0:
                        print(f"🔄 Retrying {stage_name}: Attempt {attempt}/{max_retries}...")
                    
                    # CHANGE HERE: Save the result instead of returning immediately
                    result = func(*args, **kwargs)
                    
                    # Trigger success logs and Slack notification
                    duration = time.time() - start_time
                    log_telemetry(stage_name, func.__name__, job_status, duration, error_msg)
                    return result
                    
                except Exception as e:
                    job_status = "FAILED"
                    error_msg = str(e)
                    attempt += 1
                    if attempt > max_retries:
                        duration = time.time() - start_time
                        log_telemetry(stage_name, func.__name__, job_status, duration, error_msg)
                        raise e
                    time.sleep(delay_seconds)
        return wrapper
    return decorator


def log_telemetry(stage, function_name, status, duration, error):
    structured_log = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "stage": stage,
        "function_name": function_name,
        "status": status,
        "duration_seconds": round(duration, 2),
        "error_message": error
    }
    print(f"\n🚀 [{stage} METRICS MONITOR]:")
    print(json.dumps(structured_log, indent=2))
    
    # Trigger the Slack notification for every execution trace
    send_slack_notification(structured_log)
    print("="*45 + "\n")

@pipeline_orchestrator(stage_name="BigQuery_Fetch_Audit_Logs", max_retries=1)
def fetch_live_audit_metrics():
    client = bigquery.Client(project="database-502011", location="africa-south1")
    query = """
        SELECT 
          FORMAT_TIMESTAMP('%Y-%m-%d %H:%M:%S', start_time) as run_time,
          statement_type, duration_seconds, estimated_cost_usd, job_status
        FROM `database-502011.monitoring.pipeline_performance_audit`
        ORDER BY start_time DESC LIMIT 5;
    """
    query_job = client.query(query)
    print(query_job.to_dataframe().to_string(index=False))

if __name__ == "__main__":
    fetch_live_audit_metrics()
