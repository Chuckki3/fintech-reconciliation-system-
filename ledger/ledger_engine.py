import pandas as pd
import os

# Paths
input_path = "data/internal/internal_transactions.csv"

output_path = "data/processed/ledger_entries.csv"

# Ensure processed folder exists
os.makedirs("data/processed", exist_ok=True)

def create_ledger_entries():

    print("Creating ledger entries...\n")

    df = pd.read_csv(input_path)

    ledger_entries = []

    for _, row in df.iterrows():

        txn_id = row["transaction_id"]

        amount = row["amount"]

        customer_id = row["customer_id"]

        timestamp = row["timestamp"]

        # -------------------------
        # DEBIT ENTRY
        # -------------------------

        ledger_entries.append({
            "transaction_id": txn_id,
            "account": f"{customer_id}_wallet",
            "entry_type": "DEBIT",
            "amount": amount,
            "timestamp": timestamp
        })

        # -------------------------
        # CREDIT ENTRY
        # -------------------------

        ledger_entries.append({
            "transaction_id": txn_id,
            "account": "company_settlement_account",
            "entry_type": "CREDIT",
            "amount": amount,
            "timestamp": timestamp
        })

    ledger_df = pd.DataFrame(ledger_entries)

    ledger_df.to_csv(output_path, index=False)

    print("✅ Ledger entries created!")

# Run script
create_ledger_entries()