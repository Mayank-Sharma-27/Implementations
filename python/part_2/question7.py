"""
### Background
Process transaction data to identify potentially fraudulent patterns.

### Input Data
```json
{
  "transactions": [
    {
      "id": "tx_001",
      "customer_id": "cus_123",
      "amount": 100,
      "location": "US",
      "timestamp": "2024-01-15T10:00:00Z",
      "ip_address": "192.168.1.1"
    },
    {
      "id": "tx_002",
      "customer_id": "cus_123", 
      "amount": 5000,
      "location": "RU",
      "timestamp": "2024-01-15T10:05:00Z",
      "ip_address": "10.0.0.1"
    }
  ]
}
```
### Part 1 (15 minutes)
Build detection functions:
1. **Calculate transaction velocity** (transactions per hour per customer)
2. **Detect location anomalies** (same customer, different countries)
3. **Flag high-amount transactions**

### Part 2 (15 minutes)
Add pattern analysis:
1. **Detect rapid-fire transactions** (multiple transactions in minutes)
2. **Check IP address changes**
3. **Calculate risk scores** (0-100 scale)

### Part 3 (15 minutes)
Generate reports:
1. **List high-risk transactions** 
2. **Customer risk profiles**
3. **Real-time alerts system**
"""

from collections import defaultdict, Counter
class Transactions:
    
    def get_customer_transactions(self, data: dict) -> dict:    
        customer_transactions_mappings = defaultdict(list)
        
        for transaciton in data.get("transactions", []):
            customer_id = transaciton["customer_id"]
            customer_transactions_mappings[customer_id].append(transaciton)
        return customer_transactions_mappings
    
    def get_transaction_info(self, data: dict) -> dict:
        ans = {}
        customers_with_anomalies = set()
        high_transacitons = set()
        for customer_id in data.keys():
            hour_map = Counter()
            locations = set()
            for t in data[customer_id]:

                hour = t["timestamp"].split("T")[1].split(":")[0]
                locations.add(t["location"])
                hour_map[hour] += 1
                if hour_map[hour] > 5:
                    high_transacitons.add(customer_id)
                if len(locations) > 1:
                    customers_with_anomalies.add(customer_id)       
            
            ans[customer_id] = dict(hour_map)
               
        
        return dict(ans), list(customers_with_anomalies), list(high_transacitons)
data = {
  "transactions": [
    {
      "id": "tx_001",
      "customer_id": "cus_123",
      "amount": 100,
      "location": "US",
      "timestamp": "2024-01-15T10:00:00Z",
      "ip_address": "192.168.1.1"
    },
    {
      "id": "tx_002",
      "customer_id": "cus_123", 
      "amount": 5000,
      "location": "RU",
      "timestamp": "2024-01-15T10:05:00Z",
      "ip_address": "10.0.0.1"
    }
  ]
}
transacitons = Transactions()
customer_transactions_mappings = transacitons.get_customer_transactions(data)
print(transacitons.get_transaction_info(customer_transactions_mappings))
              
        
        


