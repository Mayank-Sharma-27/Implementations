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
from datetime import datetime
class Transactions:
    
    def get_customer_transactions(self, data: dict) -> dict:    
        customer_transactions_mappings = defaultdict(list)
        
        for transaciton in data.get("transactions", []):
            customer_id = transaciton["customer_id"]
            customer_transactions_mappings[customer_id].append(transaciton)
        for cust_id, txn in customer_transactions_mappings.items():
            txn.sort(key= lambda x:x["timestamp"])   
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
    
    def get_pattern_analysis(self, customer_transactions_mappings: dict, minimum_time: int, amount_threshold: int):
        ip_address_changed_customers = set()
        rapid_fire_customers = set()
        risk_scores = {}
        high_risk_transactions = []
        for cus_id, txn in customer_transactions_mappings.items():
            last_location = None
            last_transaction_time = None
            risk_score = 0
            for t in txn:
                location= t["location"]
                if last_location and last_location != location:
                    ip_address_changed_customers.add(cus_id)
                    risk_score +=10
                time = datetime.fromisoformat(t["timestamp"].replace("Z","+00:00")) 
                
                if last_transaction_time and (time - last_transaction_time).total_seconds() / 60 <= minimum_time:
                    rapid_fire_customers.add(cus_id)
                    risk_score += 10
                last_transaction_time = time
                last_location = location
                if t["amount"] > amount_threshold:
                    high_risk_transactions.append(t)
            risk_scores[cus_id]  = min(risk_score, 100) 
        alerts = [cid for cid, score in risk_scores.items() if score >=50]          
        return {"ip_changes": ip_address_changed_customers, "rapid_fire": rapid_fire_customers, "risk_scores": risk_scores, "high_risk_tranasctions": high_risk_transactions, "alerts": alerts}              
                    
        
        
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
print(transacitons.get_pattern_analysis(customer_transactions_mappings, 10, 3000))
              
        
        


