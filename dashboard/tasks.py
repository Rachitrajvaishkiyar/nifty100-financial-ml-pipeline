import os
import json
from datetime import datetime
from django.db import connection

def generate_daily_pipeline_report():
    """
    Assembles a corporate daily audit report capturing pipeline statistics, 
    ML execution health metrics, and database anomalies.
    """
    report_date = datetime.now().strftime("%Y-%m-%d")
    
    with connection.cursor() as cursor:
        # 1. Fetch performance counts for the day
        cursor.execute("SELECT COUNT(*) FROM fact_ml_scores;")
        total_companies_scored = cursor.fetchone()[0]
        
        # 2. Extract health breakdown
        cursor.execute("SELECT COUNT(*) FROM fact_ml_scores WHERE health_label = 'EXCELLENT';")
        excellent_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM fact_ml_scores WHERE health_label IN ('WEAK', 'POOR');")
        attention_count = cursor.fetchone()[0]
        
    # Assemble structured JSON log payload
    report_payload = {
        "report_identifier": f"RE-DAILY-{report_date}",
        "timestamp": datetime.now().isoformat(),
        "metrics": {
            "total_records_processed": total_companies_scored,
            "excellent_health_assets": excellent_count,
            "attention_required_assets": attention_count
        },
        "system_status": "HEALTHY" if attention_count < 15 else "WARNING"
    }
    
    # Write to local tracking repository
    report_dir = "data/daily_reports/"
    os.makedirs(report_dir, exist_ok=True)
    
    report_filename = f"{report_dir}report_{report_date}.json"
    with open(report_filename, "w") as f:
        json.dump(report_payload, f, indent=4)
        
    print(f"✅ Daily Audit Report successfully compiled and exported to: {report_filename}")