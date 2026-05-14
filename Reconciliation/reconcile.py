import pandas as pd
import os

# Input files
internal_path = "data/internal/internal_transactions.csv"

gateway_path = "data/external/gateway_transactions.csv"

bank_path = "data/external/bank_settlements.csv"

# Output file
output_path = "data/processed/reconciliation_results.csv"

# Ensure processed folder exists
os.makedirs("data/processed", exist_ok=True)

def reconcile_transactions():

    print("Running reconciliation...\n")

    # Load datasets
    internal_df = pd.read_csv(internal_path)

    gateway_df = pd.read_csv(gateway_path)

    bank_df = pd.read_csv(bank_path)

    reconciliation_results = []

    for _, txn in internal_df.iterrows():

        txn_id = txn["transaction_id"]

        internal_amount = txn["amount"]

        # -------------------------
        # MATCH IN GATEWAY
        # -------------------------

        gateway_match = gateway_df[
            gateway_df["transaction_id"] == txn_id
        ]

        # -------------------------
        # MATCH IN BANK
        # -------------------------

        bank_match = bank_df[
            bank_df["transaction_id"] == txn_id
        ]

        issue = "MATCHED"

        # Missing in gateway
        if gateway_match.empty:
            issue = "MISSING_IN_GATEWAY"

        # Missing in bank
        elif bank_match.empty:
            issue = "MISSING_IN_BANK"

        else:

            gateway_amount = gateway_match.iloc[0]["amount"]

            # Amount mismatch
            if internal_amount != gateway_amount:
                issue = "AMOUNT_MISMATCH"

        reconciliation_results.append({
            "transaction_id": txn_id,
            "internal_amount": internal_amount,
            "reconciliation_status": issue
        })

    results_df = pd.DataFrame(reconciliation_results)

    results_df.to_csv(output_path, index=False)

    print("✅ Reconciliation complete!")

# Run reconciliation
reconcile_transactions()