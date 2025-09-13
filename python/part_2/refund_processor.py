"""
## Question 8: Refund Processing System

### Background
Process refund requests and update transaction states.

### Input Data
```json
{
  "original_transactions": [
    {
      "id": "pay_123",
      "amount": 10000,
      "currency": "USD",
      "status": "succeeded",
      "customer_id": "cus_abc"
    }
  ],
  "refund_requests": [
    {
      "id": "rfnd_001",
      "payment_id": "pay_123",
      "amount": 3000,
      "reason": "customer_request",
      "requested_at": "2024-01-16T10:00:00Z"
    }
  ]
}
```

### Part 1 (15 minutes)
Build refund processor:
1. **Validate refund amount** (can't exceed original payment)
2. **Check payment status** (can only refund successful payments)
3. **Calculate remaining refundable amount**

### Part 2 (15 minutes)
Handle partial refunds:
1. **Track multiple refunds** for same payment
2. **Update payment status** (fully_refunded vs partially_refunded)
3. **Generate refund confirmation**

### Part 3 (15 minutes)
Add business logic:
1. **Refund deadline enforcement** (30 days from payment)
2. **Fee calculations** (refund fees)
3. **Batch refund processing**
"""

from collections import defaultdict
from datetime import datetime
class RefundProcessor:
    
    def process_refunds(self, data: dict) -> dict:
        refunded_transactions = {}
        transaction_mapping = {t["id"]: t for t in data["original_transactions"]}
        refunds = data["refund_requests"]
        
        for refund in refunds:
            transaction_id = refund["payment_id"]
            transaction = transaction_mapping[transaction_id]
            if not transaction or transaction["status"] != "succeeded":
                continue
            refunded_transactions[transaction_id]  = min(refund["amount"], transaction["amount"])
     
        return refunded_transactions           
                  
    def process_partial_refunds(self, data: dict) -> dict:
        transactions = data["original_transactions"]
        refunded_transactions = []
        transaction_mapping = {t["id"]: t for t in transactions}
        refunds = data["refund_requests"]
        refunded = defaultdict(int)
        
        for refund in refunds:
            transaction = transaction_mapping.get(refund["payment_id"])
            if self.is_not_eligible_for_refund(refund, transaction):
                continue
            remaining = transaction["amount"] - refunded[refund["payment_id"]]    
            amount = min(refund["amount"], remaining)
            refunded[refund["payment_id"]] += amount
            total_refunded = refunded[refund["payment_id"]]
            if total_refunded == transaction["amount"]:
                status = "fully_refunded"
            elif total_refunded > 0:
                status = "partially_refunded"
            else:
                status = transaction["status"]  
            refunded_transactions.append({
                "refund_id": refund["id"],
                "payment_id" : refund["payment_id"],
                "refunded_amount" :amount,
                "amount_left":  transaction["amount"] - total_refunded,
                "status_after_refund": status,
                "refund_fee": 3
            })
            
        return refunded_transactions
    
    def is_not_eligible_for_refund(self, refund: dict, transaction: dict) -> bool:
        transaction_date = datetime.fromisoformat(transaction["date"].replace("Z","+00:00"))
        refund_date = datetime.fromisoformat(refund["requested_at"].replace("Z","+00:00"))
        if not transaction or transaction["status"] != "succeeded":
            return True
        if (refund_date - transaction_date).total_seconds() / 86400 > 30:
            return True
        return False            
                                    
refundprocessor = RefundProcessor()
data = {
  "original_transactions": [
    {
      "id": "pay_123",
      "amount": 10000,
      "currency": "USD",
      "status": "succeeded",
      "customer_id": "cus_abc"
    }
  ],
  "refund_requests": [
    {
      "id": "rfnd_001",
      "payment_id": "pay_123",
      "amount": 3000,
      "reason": "customer_request",
      "requested_at": "2024-01-16T10:00:00Z"
    }
  ]
}
print(refundprocessor.process_refunds(data)) 
  

data3 = {
    "original_transactions": [
        {
            "id": "pay_101",
            "amount": 12000,          # $120.00
            "currency": "USD",
            "status": "succeeded",
            "customer_id": "cus_new",
            "date": "2024-01-10T09:00:00Z"   # within 30 days
        },
        {
            "id": "pay_102",
            "amount": 15000,          # $150.00
            "currency": "USD",
            "status": "succeeded",
            "customer_id": "cus_old",
            "date": "2023-11-01T10:00:00Z"   # >30 days old
        },
        {
            "id": "pay_103",
            "amount": 8000,
            "currency": "USD",
            "status": "failed",
            "customer_id": "cus_fail",
            "date": "2024-01-05T15:30:00Z"
        }
    ],
    "refund_requests": [
        # --- Valid refund within 30 days ---
        {
            "id": "rfnd_101",
            "payment_id": "pay_101",
            "amount": 4000,           # $40.00
            "reason": "product_damage",
            "requested_at": "2024-01-25T14:00:00Z"
        },
        # --- Second partial refund for same payment (still within deadline) ---
        {
            "id": "rfnd_102",
            "payment_id": "pay_101",
            "amount": 6000,           # $60.00
            "reason": "late_delivery",
            "requested_at": "2024-01-28T09:15:00Z"
        },
        # --- Refund request AFTER 30-day window (should be rejected) ---
        {
            "id": "rfnd_103",
            "payment_id": "pay_102",
            "amount": 5000,
            "reason": "customer_request",
            "requested_at": "2024-01-15T12:30:00Z"  # too late
        },
        # --- Attempt to refund failed payment ---
        {
            "id": "rfnd_104",
            "payment_id": "pay_103",
            "amount": 1000,
            "reason": "test_refund",
            "requested_at": "2024-01-20T08:00:00Z"
        }
    ]
}
print(refundprocessor.process_partial_refunds(data3)) 
print(refundprocessor.process_partial_refunds(data3))    
    
    
    
    

