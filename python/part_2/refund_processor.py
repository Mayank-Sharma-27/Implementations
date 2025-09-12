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
class RefundProcessor:
    
    def process_refunds(self, data: dict) -> dict:
        transactions = data["original_transactions"]
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
            if not transaction or transaction["status"] != "succeeded":
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
                "status_after_refund": status
            })
            
        return refunded_transactions   
                            
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
data2  = {
    "original_transactions": [
        {
            "id": "pay_123",
            "amount": 10000,          # $100.00
            "currency": "USD",
            "status": "succeeded",
            "customer_id": "cus_abc"
        },
        {
            "id": "pay_456",
            "amount": 5000,           # $50.00
            "currency": "USD",
            "status": "succeeded",
            "customer_id": "cus_xyz"
        },
        {
            "id": "pay_789",
            "amount": 8000,           # $80.00
            "currency": "USD",
            "status": "failed",       
            "customer_id": "cus_fail"
        }
    ],
    "refund_requests": [
        # --- Multiple refunds on pay_123 ---
        {
            "id": "rfnd_001",
            "payment_id": "pay_123",
            "amount": 3000,           # $30.00 (partial)
            "reason": "customer_request",
            "requested_at": "2024-02-01T10:00:00Z"
        },
        {
            "id": "rfnd_002",
            "payment_id": "pay_123",
            "amount": 7000,           # $70.00 (completes full refund)
            "reason": "product_defect",
            "requested_at": "2024-02-05T12:30:00Z"
        },

        # --- Single partial refund on pay_456 ---
        {
            "id": "rfnd_003",
            "payment_id": "pay_456",
            "amount": 2000,           # $20.00 (partial)
            "reason": "shipping_delay",
            "requested_at": "2024-02-03T09:15:00Z"
        },

        # --- Attempt to refund a failed payment ---
        {
            "id": "rfnd_004",
            "payment_id": "pay_789",
            "amount": 1000,           # Ignored (status != succeeded)
            "reason": "customer_request",
            "requested_at": "2024-02-04T11:45:00Z"
        }
    ]
}
print(refundprocessor.process_refunds(data))   
print(refundprocessor.process_partial_refunds(data2)) 
    
    
    
    
    

