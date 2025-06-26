"""
Stripe-Style Multi-Part Problem: Merchant Transaction Reconciliation

You are given a long log of transaction strings, each in the format:

  transaction_id:merchant_id:currency:amount:type:timestamp

- The amount is in minor units (e.g., 1000 = $10.00)
- type is either "PAYMENT" or "REFUND"
- timestamp is in ISO 8601 format with time and Z

---

Part 1:
Parse this log and compute how much each merchant has earned, per currency. Output should be grouped by merchant, and currencies sorted alphabetically. Do not filter by time or duplicates.

Example:
    "m1 earned 800 in USD"
    "m2 earned 3000 in EUR"

---

Part 2:
Add support for a cutoff date (YYYY-MM-DD). Only transactions whose date part of the timestamp matches the cutoff should be included.

---

Part 3:
Some transactions may be duplicated (same `transaction_id`). De-duplicate them. Compute merchant earnings per currency, using only unique transactions, and only those on the cutoff date.

---

Part 4:
Generate a formatted reconciliation report:
- Show results grouped by merchant (sorted)
- Within each merchant, list currencies (sorted)
- Only include unique transactions on the cutoff date
- Add a global TOTAL section summing earnings across all merchants per currency

Sample output:

Reconciliation Report for 2025-06-24

Merchant: m1
  USD: 800

Merchant: m2
  EUR: 3000

TOTAL
  EUR: 3000
  USD: 800
"""

from collections import defaultdict

class Transactions:
    def create_dict(self, transaction: str) -> dict:
        
        if not transaction:
            return ValueError("Invalid Input")
        transaction_tokens = transaction.split(",")
        transaction_dict = defaultdict(list)
        
        for transaction_token in transaction_tokens:
            tx_id, merchant_id, currency, amount, tx_type, timestamp = transaction_token.strip().split(":", 5)
            transaction_dict[merchant_id].append({
                "tx_id": tx_id,
                "currency": currency,
                "amount": int(amount),
                "type": tx_type,
                "timestamp": timestamp,
            })
            
        return transaction_dict
    
    def get_transactions(self,transaction_dict: dict) -> list[str]:
        ans = [] 
        for merchant_id in sorted(transaction_dict.keys()):
            currency_dict = defaultdict(int)
            for tx in transaction_dict[merchant_id]:
                currency_dict[tx["currency"]] += tx["amount"]
            for currency in sorted(currency_dict):
                ans.append(f"{merchant_id} earned {currency_dict[currency]} in {currency}")
        return ans
    
    def get_transactions_with_cutoff_date(self, transaction_dict: dict, cutoff_date: str):
        result = []
        for merchant_id in sorted(transaction_dict.keys()):
            currency_dict = defaultdict(int)
            for tx in transaction_dict[merchant_id]:
                tx_date = tx["timestamp"].split("T")[0]
                if tx_date == cutoff_date:
                    currency_dict[tx["currency"]] += tx["amount"]
            for currency in sorted(currency_dict):
                result.append(f"{merchant_id} earned {currency_dict[currency]} in {currency} on {cutoff_date}")
        return result
    
    def get_transactions_with_unique_transactions(self, transaction_dict: dict, cutoff_date: str):
        result = []
        for merchant_id in sorted(transaction_dict.keys()):
            seen_tx_ids = set()
            currency_dict = defaultdict(int)
            for tx in transaction_dict[merchant_id]:
                if tx["tx_id"] in seen_tx_ids:
                    continue
                seen_tx_ids.add(tx["tx_id"])
                tx_date = tx["timestamp"].split("T")[0]
                if tx_date == cutoff_date:
                    currency_dict[tx["currency"]] += tx["amount"]
            for currency in sorted(currency_dict):
                result.append(f"{merchant_id} earned {currency_dict[currency]} in {currency} on {cutoff_date}")
        return result 
    
    def generate_reconciliation_report(self, transaction_dict: dict, cutoff_date: str) -> str:
        seen_tx_ids = set()
        merchant_currency_totals = defaultdict(lambda: defaultdict(int))
        global_currency_totals = defaultdict(int)

        for merchant_id in sorted(transaction_dict.keys()):
            for tx in transaction_dict[merchant_id]:
                tx_id = tx["tx_id"]
                if tx_id in seen_tx_ids:
                    continue
                seen_tx_ids.add(tx_id)

                tx_date = tx["timestamp"].split("T")[0]
                if tx_date != cutoff_date:
                    continue

                currency = tx["currency"]
                amount = tx["amount"]

                merchant_currency_totals[merchant_id][currency] += amount
                global_currency_totals[currency] += amount

        # Build report
        lines = [f"Reconciliation Report for {cutoff_date}\n"]
        for merchant_id in sorted(merchant_currency_totals.keys()):
            lines.append(f"Merchant: {merchant_id}")
            for currency in sorted(merchant_currency_totals[merchant_id].keys()):
                amt = merchant_currency_totals[merchant_id][currency]
                lines.append(f"  {currency}: {amt}")
            lines.append("")  # blank line between merchants

        # Add totals
        lines.append("TOTAL")
        for currency in sorted(global_currency_totals.keys()):
            lines.append(f"  {currency}: {global_currency_totals[currency]}")

        return "\n".join(lines)        
                
if __name__ == "__main__":
    log = (
        "txn1:m1:USD:1000:PAYMENT:2025-06-24T10:00:00Z,"
        "txn2:m1:USD:-200:REFUND:2025-06-24T10:10:00Z,"
        "txn3:m2:EUR:3000:PAYMENT:2025-06-24T11:00:00Z,"
        "txn1:m1:USD:1000:PAYMENT:2025-06-24T10:00:00Z,"  # duplicate
        "txn4:m1:EUR:500:PAYMENT:2025-06-25T09:00:00Z"    # not in cutoff
    )
    cutoff_date = "2025-06-24"
    transactions = Transactions()
    transactions_dict = transactions.create_dict(log)
    

    # You should implement this function or class method
    print(transactions.get_transactions(transactions_dict))
    print(transactions.get_transactions_with_cutoff_date(transactions_dict,cutoff_date))
    print(transactions.get_transactions_with_unique_transactions(transactions_dict, cutoff_date))
    print(transactions.generate_reconciliation_report(transactions_dict, cutoff_date))
                  