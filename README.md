### Data Pipeline Monitoring & Telemetry Framework
A lightweight, serverless monitoring framework designed for the Modern Data Stack. This framework tracks Python data execution tasks, captures pipeline telemetry, automates transient error retries, and extracts query analytics, performance metrics, and cost data directly from BigQuery's infrastructure in the africa-south1 (Johannesburg) region.

## System Architecture
The framework operates via a decoupled, two-tier logging design to ensure comprehensive observability across your entire infrastructure:
[ Python Pipeline Code ] ---> ( Decorator Tracker ) ---> Logs Success/Fail Metrics
                                                               |
                                                        [ Slack Webhook ]
                                                               ^
                                                               |
[ BigQuery Operations ]  ---> ( INFORMATION_SCHEMA ) ---> ( Audit View )

1. Application-Level Telemetry: A custom Python decorator (@pipeline_orchestrator) wraps code stages to handle automated retries and catch execution crashes before they drop out of memory.

2. Database-Level Telemetry: A BigQuery system view aggregates live processing metrics, query patterns, and direct cloud pricing estimations.

## Dashboard Visualization
You can map the compiled views directly into Looker Studio by establishing a connection to database-502011.monitoring.pipeline_performance_audit. Recommended layouts include:

1. Cost Ingestion Trackers: Line graphs summarizing historical trends of estimated_cost_usd.
2. Execution Failure Feeds: A dedicated monitoring panel filtering down exclusively to job_status = 'FAILED' to display standard stack exceptions.

## Project Setup & Installation
1. Pre-requisites & Dependencies
Ensure your local Python runtime environment has the required cloud ecosystem dependencies installed. Open your terminal and run:
```bash
pip install python-dotenv google-cloud-bigquery pandas db-dtypes

```
2. Google Cloud Authentication
Authenticate your local environment with Google Cloud Application Default Credentials (ADC) to grant your scripts access to BigQuery:
```bash
gcloud auth application-default login
```

This is a Python-based data pipeline monitoring system using Google BigQuery for backend storage and automation. It includes:

1. Pipeline decorator with error handling and Slack notifications
2. Data quality and volume assertion checking
3. BigQuery metrics extraction (performance, cost, logs)
4. A dashboard for visualization

### Dependencies:
- python-dotenv
- google-cloud-bigquery
- pandas
- db-dtypes

You'll need to install these using pip:
```bash
pip install python-dotenv google-cloud-bigquery pandas db-dtypes
```
