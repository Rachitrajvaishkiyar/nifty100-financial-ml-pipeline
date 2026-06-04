import os
import sys

def verify_project_compliance():
    print("=" * 70)
    print("⚡ RUNNING DIRECT CORE COMPLIANCE CHECK")
    print("=" * 70)
    
    missing_items = 0

    # 1. Check Section 6 Jupyter Notebooks Folder Integrity
    print("\n🔍 Checking Section 6: Machine Learning Notebooks Folder Integrity...")
    required_notebooks = [
        "notebooks/01_exploratory_data_analysis.ipynb",
        "notebooks/02_financial_health_scoring.ipynb",
        "notebooks/03_anomaly_detection.ipynb",
        "notebooks/04_sector_clustering.ipynb",
        "notebooks/05_peer_comparison_engine.ipynb",
        "notebooks/06_trend_analysis_and_forecasting.ipynb"
    ]
    
    for nb in required_notebooks:
        if os.path.exists(nb):
            print(f"  ✅ Found: {nb}")
        else:
            print(f"  ❌ Missing Required Asset: {nb}")
            missing_items += 1

    # 2. Check Architecture Blueprint Implementations
    print("\n🔍 Checking App Architecture Blueprints...")
    required_code_files = {
        "dashboard/measures.py": "Section 5 - Python Measures Logical Layer",
        "bluestock_project/celery.py": "Section 7.3 - Background Task Automation Engine"
    }

    for path, description in required_code_files.items():
        if os.path.exists(path):
            print(f"  ✅ Found: {path} ({description})")
        else:
            print(f"  ❌ Missing Architecture File: {path}")
            missing_items += 1

    # 3. Final Verification Status
    print("\n" + "=" * 70)
    if missing_items == 0:
        print("🏆 VERIFICATION SUCCESS: All core deliverables present locally!")
        print("Your architecture components match the project layout specification.")
    else:
        print(f"⚠️ VERIFICATION ALERT: Found {missing_items} missing items.")
    print("=" * 70)

if __name__ == "__main__":
    verify_project_compliance()