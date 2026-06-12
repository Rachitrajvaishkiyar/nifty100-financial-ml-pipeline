# Nifty 100 Asynchronous Financial Analytics & ETL Pipeline

An enterprise-grade data warehousing and automated analytics platform built to process historical financial data, execute calculations, and handle background task scheduling.

## 🛠️ System Architecture & Tech Stack
- **Backend Framework:** Django (Python 3)
- **Data Warehouse:** PostgreSQL (Hosted via Docker Containers)
- **Asynchronous Task Queue:** Celery Engine
- **Message Broker & Event Loop:** Redis
- **Automation Scheduler:** Celery Beat (Cron Daemon)

## 🚀 Key Features & Automation
- **Decoupled Task Processing:** Financial metrics are computed asynchronously to prevent UI main-thread blocking.
- **Cron-Scheduled Audit Engine:** Celery Beat activates an automated reporting script daily at 08:00 AM, scanning the live PostgreSQL data warehouse (`fact_profit_loss` and `fact_analysis`) to compile a JSON state matrix.
- **Dynamic System Grading:** Automated evaluation of database volume and processing pipeline state flags (`HEALTHY` / `WARNING`).

## 📊 Live Sample Audit Output
```json
{
    "report_identifier": "RE-DAILY-2026-06-12",
    "timestamp": "2026-06-12T17:11:34.149986",
    "metrics": {
        "total_profit_loss_records": 1277,
        "total_analytical_metrics_computed": 21
    },
    "system_status": "HEALTHY"
}