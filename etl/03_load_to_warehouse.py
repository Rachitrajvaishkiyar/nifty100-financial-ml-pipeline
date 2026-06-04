import os
import pandas as pd
from sqlalchemy import create_engine

DB_USER = "bluestock_user"
DB_PASSWORD = "bluestock_password"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "b100_warehouse"

CLEAN_DIR = "data/clean"

def load_tables_to_warehouse():
    print("🔌 Step 1: Connecting to your PostgreSQL Data Warehouse...")
    engine = create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
    
    tables_to_load = [
        ("dim_company.csv", "dim_company"),
        ("fact_profit_loss.csv", "fact_profit_loss"),
        ("fact_balance_sheet.csv", "fact_balance_sheet"),
        ("fact_cash_flow.csv", "fact_cash_flow"),
        ("fact_analysis.csv", "fact_analysis"),
        ("fact_documents.csv", "fact_documents"),
        ("fact_prosandcons.csv", "fact_pros_cons")
    ]
    
    print("\n🔄 Step 2: Beginning database upload batch...")
    for csv_file, table_name in tables_to_load:
        file_path = os.path.join(CLEAN_DIR, csv_file)
        if os.path.exists(file_path):
            print(f"📥 Loading '{csv_file}' into table '{table_name}'...")
            df = pd.read_csv(file_path)
            df.to_sql(table_name, con=engine, if_exists='replace', index=False)
            print(f"   ✅ Successfully pushed {len(df)} rows.")
        else:
            print(f"⚠️ Warning: Skip processing '{csv_file}' — file not found.")
            
    print("\n🎉 Mission Accomplished! Your Data Warehouse is officially populated and running.")

if __name__ == "__main__":
    try:
        load_tables_to_warehouse()
    except Exception as e:
        print(f"❌ Database load failed: {e}")