"""
Invoice Discrepancy Detection Tool
Author: Surendhar Jagannathan
Purpose: Automatically detects mismatches between purchase orders and vendor invoices
"""

import pandas as pd
import os

# Create output folder if it doesn't exist
os.makedirs('output', exist_ok=True)

print("=" * 50)
print("INVOICE DISCREPANCY DETECTION TOOL")
print("=" * 50)

# Step 1: Load the data
print("\n[1] Loading data files...")
purchase_orders = pd.read_csv('data/purchase_orders.csv')
vendor_invoices = pd.read_csv('data/vendor_invoices.csv')

print(f"    - Purchase orders loaded: {len(purchase_orders)} records")
print(f"    - Vendor invoices loaded: {len(vendor_invoices)} records")

# Step 2: Merge the two datasets
print("\n[2] Comparing purchase orders against vendor invoices...")
merged = purchase_orders.merge(
    vendor_invoices, 
    on='InvoiceNumber', 
    how='outer', 
    suffixes=('_PO', '_Invoice')
)

# Step 3: Find missing invoices (in PO but not in vendor invoices)
print("\n[3] Checking for missing invoices...")
missing_invoices = merged[merged['Amount_Invoice'].isna()]
if len(missing_invoices) > 0:
    print(f"    ⚠️ WARNING: {len(missing_invoices)} invoice(s) found in purchase orders but not in vendor invoices:")
    for idx, row in missing_invoices.iterrows():
        print(f"       - {row['InvoiceNumber']} from {row['Supplier_PO']} for £{row['Amount_PO']:,.2f}")
else:
    print("    ✓ All purchase orders have corresponding invoices")

# Step 4: Find extra invoices (in vendor invoices but not in PO)
print("\n[4] Checking for extra invoices...")
extra_invoices = merged[merged['Amount_PO'].isna()]
if len(extra_invoices) > 0:
    print(f"    ⚠️ WARNING: {len(extra_invoices)} invoice(s) found in vendor invoices but not in purchase orders:")
    for idx, row in extra_invoices.iterrows():
        print(f"       - {row['InvoiceNumber']} from {row['Supplier_Invoice']} for £{row['Amount_Invoice']:,.2f}")
else:
    print("    ✓ No unexpected invoices found")

# Step 5: Find amount discrepancies
print("\n[5] Checking for amount discrepancies...")
discrepancies = merged[
    (~merged['Amount_PO'].isna()) & 
    (~merged['Amount_Invoice'].isna()) & 
    (merged['Amount_PO'] != merged['Amount_Invoice'])
]

if len(discrepancies) > 0:
    print(f"    ⚠️ WARNING: {len(discrepancies)} amount discrepancy/ies found:")
    for idx, row in discrepancies.iterrows():
        diff = row['Amount_Invoice'] - row['Amount_PO']
        print(f"       - {row['InvoiceNumber']}: PO = £{row['Amount_PO']:,.2f}, Invoice = £{row['Amount_Invoice']:,.2f}, Difference = £{diff:,.2f}")
else:
    print("    ✓ All amounts match")

# Step 6: Find duplicate bookings
print("\n[6] Checking for duplicate invoices...")
duplicates = vendor_invoices[vendor_invoices.duplicated('InvoiceNumber', keep=False)]
if len(duplicates) > 0:
    print(f"    ⚠️ WARNING: {len(duplicates)} duplicate invoice(s) found:")
    print(duplicates[['InvoiceNumber', 'Supplier', 'Amount']].to_string(index=False))
else:
    print("    ✓ No duplicate invoices found")

# Step 7: Generate summary report
print("\n" + "=" * 50)
print("SUMMARY REPORT")
print("=" * 50)

total_po_amount = purchase_orders['Amount'].sum()
total_invoice_amount = vendor_invoices['Amount'].sum()
discrepancy_total = discrepancies['Amount_Invoice'].sum() - discrepancies['Amount_PO'].sum() if len(discrepancies) > 0 else 0

print(f"Total Purchase Orders Value:  £{total_po_amount:,.2f}")
print(f"Total Vendor Invoices Value: £{total_invoice_amount:,.2f}")
print(f"Net Discrepancy:             £{discrepancy_total:,.2f}")

# Save report to file
report_path = 'output/discrepancy_report.txt'
with open(report_path, 'w') as f:
    f.write("INVOICE DISCREPANCY REPORT\n")
    f.write("=" * 40 + "\n\n")
    f.write(f"Total Purchase Orders: {len(purchase_orders)}\n")
    f.write(f"Total Vendor Invoices: {len(vendor_invoices)}\n")
    f.write(f"Missing Invoices: {len(missing_invoices)}\n")
    f.write(f"Extra Invoices: {len(extra_invoices)}\n")
    f.write(f"Amount Discrepancies: {len(discrepancies)}\n")
    f.write(f"Duplicate Invoices: {len(duplicates)}\n\n")
    f.write(f"Total Discrepancy Value: £{discrepancy_total:,.2f}\n")

print(f"\n✓ Detailed report saved to: {report_path}")
print("\n" + "=" * 50)