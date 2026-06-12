import os
import json
from datetime import datetime
from django.db import connection
from celery import shared_task

@shared_task
def generate_daily_pipeline_report():
    """
    Assembles a corporate daily audit report capturing pipeline statistics, 
    analytics counts, and database structural health autonomously at 08:00 AM.
    """
    report_date = datetime.now().strftime("%Y-%m-%d")
    
    with connection.cursor() as cursor:
        # 1. Fetch total record performance counts from your live profit & loss table
        cursor.execute('SELECT COUNT(*) FROM fact_profit_loss;')
        total_records = cursor.fetchone()[0]
        
        # 2. Fetch analytics tracking data points from your live metrics table
        cursor.execute('SELECT COUNT(*) FROM fact_analysis;')
        total_analysis_metrics = cursor.fetchone()[0]
        
    # Assemble structured JSON log payload mirroring your production environment
    report_payload = {
        "report_identifier": f"RE-DAILY-{report_date}",
        "timestamp": datetime.now().isoformat(),
        "metrics": {
            "total_profit_loss_records": total_records,
            "total_analytical_metrics_computed": total_analysis_metrics,
        },
        "system_status": "HEALTHY" if total_records > 0 else "EMPTY_WAREHOUSE"
    }
    
    # Write to local tracking repository inside your project directory
    report_dir = "data/daily_reports/"
    os.makedirs(report_dir, exist_ok=True)
    
    report_filename = f"{report_dir}report_{report_date}.json"
    with open(report_filename, "w") as f:
        json.dump(report_payload, f, indent=4)
        
    print(f"✅ Daily Audit Report successfully compiled and exported to: {report_filename}")
    return f"Report {report_date} generated successfully."