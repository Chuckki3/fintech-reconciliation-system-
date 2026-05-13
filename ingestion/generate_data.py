import pandas as pd
import random
from datetime import datetime, timedelta
import os

# Create folders
os.makedirs("data/internal", exist_ok=True)
os.makedirs("data/external", exist_ok=True)

def generate_transactions(n=100):

    base_time = datetime.now()

    internal_data = []
    gateway_data = []
    bank_data = []

    for i in range(n):

        txn_id = f"txn_{i+1}"

        amount = round(random.uniform(1000, 500000), 2)

        customer_id = f"user_{random.randint(1, 50)}"

        timestamp = base_time + timedelta(seconds=i)

        # -------------------------
        # INTERNAL SYSTEM RECORD
        # -------------------------

        internal_data.append({
            "transaction_id": txn_id,
            "customer_id": customer_id,
            "amount": amount,
            "status": "SUCCESS",
            "timestamp": timestamp
        })

        # -------------------------
        # GATEWAY RECORD
        # Simulate mismatches
        # -------------------------

        if random.random() > 0.1:

            gateway_data.append({
                "transaction_id": txn_id,
                "gateway_status": "SUCCESS",

                # 10% chance amount mismatch
                "amount": amount if random.random() > 0.1 else round(amount * 0.9, 2),

                "timestamp": timestamp
            })

        # -------------------------
        # BANK SETTLEMENT RECORD
        # Simulate missing settlements
        # -------------------------

        if random.random() > 0.2:

            bank_data.append({
                "transaction_id": txn_id,
                "settlement_status": "SETTLED",
                "amount": amount,
                "timestamp": timestamp
            })

    # Save files

    pd.DataFrame(internal_data).to_csv(
        "data/internal/internal_transactions.csv",
        index=False
    )

    pd.DataFrame(gateway_data).to_csv(
        "data/external/gateway_transactions.csv",
        index=False
    )

    pd.DataFrame(bank_data).to_csv(
        "data/external/bank_settlements.csv",
        index=False
    )

    print("✅ Data generation complete!")

# Run script
generate_transactions(200)
