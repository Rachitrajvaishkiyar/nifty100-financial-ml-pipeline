def run_corporate_rule_engine(profile):
    """
    Executes automated rule evaluation mapping out operational observations 
    based on the criteria outlined in Section 7.2.
    """
    pros = []
    cons = []

    # --- AUTOMATED PROS RULES ---
    if profile.get('debt_to_equity', 1.0) < 0.1:
        pros.append("Company is almost debt free.")
        
    if profile.get('roe_3y', 0.0) > 20.0:
        pros.append(f"Company has a good return on equity (ROE) track record: 3 Years ROE {profile['roe_3y']}%")
        
    if profile.get('consistent_dividend_5y', False):
        pros.append(f"Company has been maintaining a healthy dividend payout of {profile.get('avg_div_payout', 35)}%")
        
    if profile.get('cagr_sales_10y', 0.0) > 15.0:
        pros.append(f"Strong long-term revenue growth of {profile['cagr_sales_10y']}% CAGR over 10 years")
        
    if profile.get('opm_improved_3y', False):
        pros.append("Improving operating margins consistently for 3 years")
        
    if profile.get('ocf_exceeds_net_profit_3y', False):
        pros.append("Strong cash conversion — OCF exceeds reported profits")
        
    if profile.get('cagr_profit_3y', 0.0) > 15.0:
        pros.append(f"Profit growth accelerated significantly at {profile['cagr_profit_3y']}% CAGR")

    # --- AUTOMATED CONS RULES ---
    if profile.get('cagr_sales_5y', 15.0) < 10.0:
        cons.append("Below-average sales growth over past five years")
        
    if profile.get('borrowings_spike_1y', False):
        cons.append("Borrowings have increased significantly in the recent year")
        
    if profile.get('opm_declining_3y', False):
        cons.append("Operating margins have been declining for three consecutive years")
        
    if profile.get('debt_to_equity', 0.0) > 1.5:
        cons.append("Stock carries high debt — leverage levels require monitoring")
        
    if profile.get('earnings_quality_concern', False):
        cons.append("Earnings quality concern — reported profits exceed actual cash generation")
        
    if profile.get('interest_coverage', 5.0) < 2.0:
        cons.append("Low interest coverage ratio — debt repayment risk")

    return {"pros": pros, "cons": cons}