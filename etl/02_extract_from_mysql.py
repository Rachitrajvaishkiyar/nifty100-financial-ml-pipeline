import os
import shutil
import pandas as pd

# Define paths matching your clean folder structure
RAW_DIR = "data/raw"
CLEAN_DIR = "data/clean"

# Force recreate the clean directory to fix filesystem errors
if os.path.exists(CLEAN_DIR):
    if os.path.isdir(CLEAN_DIR):
        shutil.rmtree(CLEAN_DIR)
    else:
        os.remove(CLEAN_DIR)

os.makedirs(CLEAN_DIR, exist_ok=True)
def standardize_year_label(val):
    """Maps messy dates like 'Mar-24' or 'Mar 2024' into standard formats."""
    if pd.isna(val):
        return None
    s = str(val).strip()
    if s.upper() == 'TTM':
        return 'TTM'
    # Fix dash formats like 'Mar-24' -> 'Mar 2024'
    if '-' in s:
        parts = s.split('-')
        month = parts[0]
        year_short = parts[1]
        if len(year_short) == 2:
            century = "20" if int(year_short) < 50 else "19"
            return f"{month} {century}{year_short}"
    return s

def extract_fiscal_year(val):
    """Extracts just the number year as an integer (e.g., 'Mar 2024' -> 2024)."""
    if pd.isna(val):
        return None
    s = str(val).strip()
    if s.upper() == 'TTM':
        return 2025 # Assign TTM data to the trailing frontier year
    # Extract digits
    digits = [int(i) for i in s.split() if i.isdigit()]
    if digits:
        return digits[0]
    # Check fallback for dash string if not standardized yet
    if '-' in s:
        year_short = s.split('-')[1]
        if year_short.isdigit() and len(year_short) == 2:
            return 2000 + int(year_short)
    return None

def process_pipeline():
    print("🔄 Step 1: Reading Excel files from data/raw/...")
    
    # 1. COMPANIES
    print("📊 Cleaning: companies.xlsx")
    df_comp = pd.read_excel(os.path.join(RAW_DIR, "companies.xlsx"))
    df_comp.columns = df_comp.columns.str.strip().str.lower()
    df_comp.to_csv(os.path.join(CLEAN_DIR, "dim_company.csv"), index=False)
    
    # 2. PROFIT & LOSS
    print("📊 Cleaning: profitandloss.xlsx & Calculating Margins...")
    df_pnl = pd.read_excel(os.path.join(RAW_DIR, "profitandloss.xlsx"))
    df_pnl.columns = df_pnl.columns.str.strip().str.lower()
    
    # Standardize time columns
    time_col = 'year' if 'year' in df_pnl.columns else df_pnl.columns[1]
    df_pnl['year_label'] = df_pnl[time_col].apply(standardize_year_label)
    df_pnl['fiscal_year'] = df_pnl[time_col].apply(extract_fiscal_year)
    
    # Add formulas requested by manager
    if 'net_profit' in df_pnl.columns and 'sales' in df_pnl.columns:
        df_pnl['net_profit_margin_pct'] = (df_pnl['net_profit'] / df_pnl['sales']) * 100
    if 'expenses' in df_pnl.columns and 'sales' in df_pnl.columns:
        df_pnl['expense_ratio_pct'] = (df_pnl['expenses'] / df_pnl['sales']) * 100
    if 'operating_profit' in df_pnl.columns and 'interest' in df_pnl.columns:
        # replace 0 with small value to avoid division by zero error
        df_pnl['interest_coverage'] = df_pnl['operating_profit'] / df_pnl['interest'].replace(0, 0.001)
        
    df_pnl.to_csv(os.path.join(CLEAN_DIR, "fact_profit_loss.csv"), index=False)

    # 3. BALANCE SHEET
    print("📊 Cleaning: balancesheet.xlsx & Calculating Leverage...")
    df_bs = pd.read_excel(os.path.join(RAW_DIR, "balancesheet.xlsx"))
    df_bs.columns = df_bs.columns.str.strip().str.lower()
    
    bs_time = 'year' if 'year' in df_bs.columns else df_bs.columns[1]
    df_bs['year_label'] = df_bs[bs_time].apply(standardize_year_label)
    df_bs['fiscal_year'] = df_bs[bs_time].apply(extract_fiscal_year)
    
    # Formula: debt_to_equity = borrowings / (equity_capital + reserves)
    if all(col in df_bs.columns for col in ['borrowings', 'equity_capital', 'reserves']):
        denom = (df_bs['equity_capital'] + df_bs['reserves']).replace(0, 0.001)
        df_bs['debt_to_equity'] = df_bs['borrowings'] / denom
        
    df_bs.to_csv(os.path.join(CLEAN_DIR, "fact_balance_sheet.csv"), index=False)

    # 4. CASH FLOW
    print("📊 Cleaning: cashflow.xlsx & Calculating Free Cash Flow...")
    df_cf = pd.read_excel(os.path.join(RAW_DIR, "cashflow.xlsx"))
    df_cf.columns = df_cf.columns.str.strip().str.lower()
    
    cf_time = 'year' if 'year' in df_cf.columns else df_cf.columns[1]
    df_cf['year_label'] = df_cf[cf_time].apply(standardize_year_label)
    df_cf['fiscal_year'] = df_cf[cf_time].apply(extract_fiscal_year)
    
    # Formula: free_cash_flow = operating_activity + investing_activity
    if 'operating_activity' in df_cf.columns and 'investing_activity' in df_cf.columns:
        df_cf['free_cash_flow'] = df_cf['operating_activity'] + df_cf['investing_activity']
        
    df_cf.to_csv(os.path.join(CLEAN_DIR, "fact_cash_flow.csv"), index=False)

    # 5. ANALYSIS & OTHERS
    print("📊 Cleaning remaining support sheets...")
    for sheet in ["analysis", "documents", "prosandcons"]:
        df_temp = pd.read_excel(os.path.join(RAW_DIR, f"{sheet}.xlsx"))
        df_temp.columns = df_temp.columns.str.strip().str.lower()
        df_temp.to_csv(os.path.join(CLEAN_DIR, f"fact_{sheet}.csv"), index=False)

    print("\n🎉 Success! All clean, calculated tables are saved in data/clean/ as CSVs.")

if __name__ == "__main__":
    process_pipeline()