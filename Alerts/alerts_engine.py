import pandas as pd
import os

# Input reconciliation results
input_path = "data/processed/reconciliation_results.csv"

# Output alerts file
output_path = "data/processed/discrepancy_alerts.csv"

# Ensure processed folder exists
os.makedirs("data/processed", exist_ok=True)

def generate_alerts():

    print("Generating discrepancy alerts...\n")

    # Load reconciliation results
    df = pd.read_csv(input_path)

    # Filter only failed reconciliations
    alerts_df = df[
        df["reconciliation_status"] != "MATCHED"
    ]

    # Save alerts
    alerts_df.to_csv(output_path, index=False)

    print(f"🚨 {len(alerts_df)} discrepancy alerts generated!")

# Run alerts
generate_alerts()