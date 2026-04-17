# Invoice Discrepancy Detection Tool

## Business Problem
Organizations processing thousands of invoices face challenges with:
- Manual invoice matching being time-consuming
- Billing discrepancies causing financial leakage
- Missing invoices delaying payment cycles

## Solution
This Python tool automates reconciliation of purchase orders against vendor invoices by:
- Identifying missing invoices
- Detecting extra invoices
- Flagging amount discrepancies
- Finding duplicate bookings

## Technologies Used
- Python 3.x
- Pandas library

## Sample Output
Total Purchase Orders Value: £8,285.75
Total Vendor Invoices Value: £8,975.50
Missing Invoices: 1
Extra Invoices: 1
Amount Discrepancies: 1
## 📊 Live Dashboard

View the interactive dashboard here:  
**[Invoice Discrepancy Dashboard - Looker Studio](https://datastudio.google.com/reporting/201d3a90-7031-4062-8740-48fa852657d5)**

### Dashboard Preview

The dashboard visualizes:
- **Total discrepancies found** (Scorecard)
- **Breakdown by discrepancy type** (Missing, Extra, Amount Mismatch)
- **Financial impact by discrepancy type**
- **Detailed list of all discrepancies**

### Data Source
The dashboard reads from `output/discrepancy_dashboard.csv`, which is generated automatically by running the Python script.

### How to Refresh the Dashboard
1. Run `python scripts/invoice_reconciliation.py`
2. Upload the new `discrepancy_dashboard.csv` to GitHub
3. The Looker Studio dashboard will update automatically (if connected to the CSV)
