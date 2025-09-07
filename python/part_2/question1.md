"""
You're processing payment transaction logs in JSON format. Build a system to parse and analyze this data.

### Input Data

```json
[
  {
    "id": "txn_123",
    "amount": 2500,
    "currency": "USD",
    "status": "succeeded",
    "customer_id": "cus_abc",
    "created": "2024-01-15T10:30:00Z",
    "payment_method": "card"
  },
  {
    "id": "txn_124",
    "amount": 1000,
    "currency": "EUR",
    "status": "failed",
    "customer_id": "cus_xyz",
    "created": "2024-01-15T11:00:00Z",
    "payment_method": "bank_transfer",
    "failure_code": "insufficient_funds"
  }
]
```

### Part 1 (15 minutes)

Build a function that:

1. **Parses the JSON data**
2. **Returns total successful transaction amount in USD** (assume EUR to USD rate is 1.1)
3. **Lists all unique customer IDs**

### Part 2 (15 minutes)

Add functionality to:

1. **Group transactions by payment method**
2. **Calculate success rate for each payment method**
3. **Find the customer with the highest total transaction volume**

### Part 3 (15 minutes)

Handle these new requirements:

1. **Filter transactions by date range**
2. **Support new currency conversion rates** (passed as parameter)
3. **Generate a summary report** showing daily totals

"""

from collections import defaultdict
from datetime import datetime

class TransactionManager:

    def get_transactions(self, data: list[dict]) -> dict:
        customer_mappings = defaultdict(list)
        total_transaction_amount = 0
        for d in data:
            customer_id = d["customer_id"]
            status = d['status']
            transacitons = customer_mappings.get(customer_id, [])
            transacitons.append(d)
            currency = d['currency']
            customer_mappings[customer_id] = transacitons
            if status == 'succeeded':
                amount = int(d['amount'])
                if currency == 'EUR':
                    amount = 1.1 * amount
                total_transaction_amount += amount
        return {"total_transactions_amount": total_transaction_amount, "customer_transactions" : customer_mappings}

    def get_payment_methods_info(self, customer_transactions) -> dict:
        customer_ids = customer_transactions.keys()
        payment_method_transactions_mapping = defaultdict(list)
        max_volume = 0
        customer_with_max_transcation_volume = None
        for customer_id in customer_ids:
            transcations = customer_transactions[customer_id]
            total_transaction_volume = 0
            for transaction in transcations:
                payment_method = transaction["payment_method"]
                payment_method_transactions_mapping[payment_method].append(transaction)
                status = transaction['status']
                currency = transaction['currency']
                if status == 'succeeded':
                    amount = int(transaction['amount'])
                    if currency == 'EUR':
                        amount = 1.1 * amount
                    total_transaction_volume += amount

            if total_transaction_volume > max_volume:
                customer_with_max_transcation_volume = customer_id
            max_volume = max(max_volume, total_transaction_volume)
        payment_methods = payment_method_transactions_mapping.keys()
        payment_methods_success_mapping = {}

        for payment_method in payment_methods:
            transcations = payment_method_transactions_mapping[payment_method]
            total_transactions = len(transcations)
            success_transactions = 0
            for transaction in transcations:
                status = transaction['status']
                if status == 'succeeded':
                    success_transactions += 1
            payment_methods_success_mapping[payment_method] = (success_transactions/total_transactions) * 100

        return {"payment_methods_success_mapping": payment_methods_success_mapping, "customer_with_max_transcation_volume": customer_with_max_transcation_volume,
                "payment_method_transactions_mapping": payment_method_transactions_mapping}

    def get_filtered_transacitons(self, data: list[dict], start_date: str, end_date: str) -> list[dict] :
        """ Return transactions withing [start_date, end_data] inclusive """
        start = datetime.fromisoformat(start_date.replace("Z", "+00:00"))
        end = datetime.fromisoformat(end_date.replace("Z", "+00:00"))

        filtered = []
        for transaction in data:
            created = datetime.fromisoformat(transaction["created"].replace("Z", "+00:00"))
            if start <= created <= end:
                filtered.append(transaction)
        return filtered

    def get_summary_report(self, data: list[dict], conversion_rates: dict) -> dict:
        daily_totals = defaultdict(float)

        for transaction in data:
            if transaction["status"] != "succeeded":
                continue
            transaction_date = transaction["created"][10]
            amount = int(transaction["amount"])
            rate = conversion_rates.get(transaction["currency"], 1.0)
            daily_totals[transaction_date] += amount * rate

        return dict(daily_totals)

transaction_manager = TransactionManager()

data = [
{
"id": "txn_123",
"amount": 2500,
"currency": "USD",
"status": "succeeded",
"customer_id": "cus_abc",
"created": "2024-01-15T10:30:00Z",
"payment_method": "card"
},
{
"id": "txn_124",
"amount": 1000,
"currency": "EUR",
"status": "failed",
"customer_id": "cus_xyz",
"created": "2024-01-15T11:00:00Z",
"payment_method": "bank_transfer",
"failure_code": "insufficient_funds"
}
]

ans = transaction_manager.get_transactions(data)
customer_transactions = ans['customer_transactions']
print(customer_transactions)

payment_method_info = transaction_manager.get_payment_methods_info(customer_transactions)
print(payment_method_info)
filtered = transaction_manager.get_filtered_transacitons(data, "2024-01-15T00:00:00Z", "2024-01-15T23:59:59Z")
print("Filtered transactions:", filtered)

# Example: Daily summary with custom conversion rates

conversion_rates = {"USD": 1.0, "EUR": 1.1}
summary = transaction_manager.get_summary_report(data, conversion_rates)
print("Daily Summary:", summary)
