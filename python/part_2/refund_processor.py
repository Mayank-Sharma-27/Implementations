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

class RefundProcessor:
    
    def process_refunds(self, data: dict) -> dict:
        transactions = data["original_transactions"]
        refunded_transactions = {}
        transaction_mapping = {}
        transaction_mapping = {transaction_mapping["id"]: t for t in transactions}
        refunds = data["refund_requests"]
        
        for refund in refunds:
            transaction_id = refund["payment_id"]
            transaction = transaction_mapping[transaction_id]
            if not transaction or transaction["status"] != "succeeded":
                continue
            refunded_transactions[transaction_id]  = min(refund["amount"], transaction["amount"])
     
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
print(refundprocessor.process_refunds(data))    
    
    
    
    
    

