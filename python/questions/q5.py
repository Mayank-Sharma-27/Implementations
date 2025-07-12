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
    
    def parse_events(self, log: str) -> dict:
        log_tokens = log.split(",")
        events = []
        for log_token in log_tokens:
            transaction_id, merchant_id, currency, amount, event_type, timestamp = log_token.split(":")[0:6]
            if event_type == "REFUND":
                amount = int(amount)
            events.append({
                "transaction_id": transaction_id,
                "merchant_id": merchant_id,
                "currency": currency,
                "amount": int(amount),
                "event_type": event_type,
                "timestamp": timestamp
            })
            
        events = sorted(events, key=lambda p:p["timestamp"])
        
        merchant_mapping = defaultdict(lambda: {"total_amount": 0, "currency_mappinng" : defaultdict(list)})
        
        for event in events:
            merchant_id = event["merchant_id"]
            amount = int(event["amount"])
            event_type = event["event_type"]
            timestamp = event["timestamp"]
            currency  = event["currency"]
            transaction_id = event["transaction_id"] 
            merchant_mapping[merchant_id]["total_amount"] += amount
            currency_mappinng = merchant_mapping[merchant_id]["currency_mappinng"]
            currency_mappinng[currency].append({
                "amount": amount,
                "timestamp": timestamp,
                "transaction_id": transaction_id
            })
            merchant_mapping[merchant_id]["currency_mappinng"] = currency_mappinng
          
        
        return merchant_mapping    
    
    def get_transactions(self, log: str) -> dict:
        transactions_dict = self.parse_events(log)
        #print(transactions_dict)
        ans = defaultdict(lambda: defaultdict(int))
        
        for merchant_id in transactions_dict:
            for currency in  sorted(transactions_dict[merchant_id]["currency_mappinng"].keys()):
                events = transactions_dict[merchant_id]["currency_mappinng"][currency]
                for event in events:
                    amount = int(event["amount"])
                    ans[merchant_id][currency] += amount
        return ans
    
    def get_transactions_with_cutoff_date(self, log: str, cutoff_date: str) -> dict:
        transactions_dict = self.parse_events(log)
        #print(transactions_dict)
        ans = defaultdict(lambda: defaultdict(int))
        
        for merchant_id in transactions_dict:
            for currency in  sorted(transactions_dict[merchant_id]["currency_mappinng"].keys()):
                events = transactions_dict[merchant_id]["currency_mappinng"][currency]
                for event in events:
                    time = event["timestamp"].split("T")[0]
                    amount = int(event["amount"])
                    if time <= cutoff_date:
                        #print(amount)
                        ans[merchant_id][currency] += amount
        return ans
    
    def get_transactions_with_unique_transactions(self, log: str, cutoff_date: str) -> dict:
        transactions_dict = self.parse_events(log)
        #print(transactions_dict)
        ans = defaultdict(lambda: defaultdict(int))
        done_transactions = set()
        for merchant_id in transactions_dict:
            for currency in  sorted(transactions_dict[merchant_id]["currency_mappinng"].keys()):
                events = transactions_dict[merchant_id]["currency_mappinng"][currency]
                for event in events:
                    time = event["timestamp"].split("T")[0]
                    amount = int(event["amount"])
                    transaction_id = event["transaction_id"]
                    if time <= cutoff_date and transaction_id not in done_transactions:
                        done_transactions.add(transaction_id)
                        #print(amount)
                        ans[merchant_id][currency] += amount
        return ans
    
    def generate_reconciliation_report(self, log: str, cutoff_date: str) -> dict:
        transactions_dict = self.parse_events(log)
        #print(transactions_dict)
        ans = defaultdict(lambda: defaultdict(int))
        done_transactions = set()
        for merchant_id in transactions_dict:
            for currency in  sorted(transactions_dict[merchant_id]["currency_mappinng"].keys()):
                events = transactions_dict[merchant_id]["currency_mappinng"][currency]
                for event in events:
                    time = event["timestamp"].split("T")[0]
                    amount = int(event["amount"])
                    transaction_id = event["transaction_id"]
                    if time <= cutoff_date and transaction_id not in done_transactions:
                        done_transactions.add(transaction_id)
                        #print(amount)
                        ans[merchant_id][currency] += amount
            ans[merchant_id]["total_amount"]  = transactions_dict[merchant_id]["total_amount"]      
        return ans
                     
                
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
    
    print(dict(transactions.get_transactions(log)))
    print(dict(transactions.get_transactions_with_cutoff_date(log,cutoff_date)))
    print(dict(transactions.get_transactions_with_unique_transactions(log, cutoff_date)))
    print(transactions.generate_reconciliation_report(log, cutoff_date))
                  