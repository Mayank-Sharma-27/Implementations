"""
Build a system to process incoming webhook events from various payment providers.

### Input Data

```json
[
  {
    "id": "evt_001",
    "type": "payment.succeeded",
    "provider": "stripe",
    "timestamp": 1640995200,
    "data": {
      "payment_id": "pay_123",
      "amount": 5000,
      "customer": "cus_abc"
    }
  },
  {
    "id": "evt_002",
    "type": "payment_failed",
    "provider": "paypal",
    "timestamp": 1640995300,
    "data": {
      "transaction_id": "txn_456",
      "amount": 2500,
      "user_id": "user_xyz",
      "error": "card_declined"
    }
  }
]
```

### Part 1 (15 minutes)

Build a webhook processor that:

1. **Normalizes different provider formats** (stripe uses "customer", paypal uses "user_id")
2. **Converts timestamps to readable dates**
3. **Filters events by type**

### Part 2 (15 minutes)

Add event handling:

1. **Deduplicate events** (same id shouldn't be processed twice)
2. **Process events chronologically**
3. **Update customer payment status** based on events

### Part 3 (15 minutes)

Handle real-time requirements:

1. **Queue system simulation** (mark events as processing/completed)
2. **Retry failed events** with exponential backoff
3. **Generate event processing summary**
"""

from collections import defaultdict
from datetime import datetime

class EventsService:
    
    def handle_events(self, data: list[dict], event_type: str):
        processed_events = []
        
        for event in data:
            processed_event = {}
            
                
            processed_event["event_id"] = event["id"]
            processed_event["provider"] = event["provider"]
            processed_event["event_type"] = event["type"]
            processed_event["timestamp"] = datetime.fromtimestamp(event["timestamp"]).strftime("%Y-%m-%d %H:%M:%S")
            data = event["data"]
            if data.get("transaction_id") is not None:
                processed_event["transaction_id"] = data["transaction_id"]
            if data.get("payment_id") is not None:
                processed_event["transaction_id"] = data["payment_id"]
            if data.get("amount") is not None:
                processed_event["amount"] = data["amount"]
            if data.get("user_id") is not None: 
                processed_event["customer_id"] = data["user_id"]
            if data.get("customer") is not None:
               processed_event["customer_id"] = data["customer"] 
            if data.get("error") is not None:
                processed_event["error"] = data["error"]
            processed_events.append(processed_event)
           
        filtered_events = []
        for event in processed_events:
            if event["event_type"]  == event_type:
                filtered_events.append(event)    
        return filtered_events, processed_events
         
    {
    "id": "evt_002",
    "type": "payment_failed",
    "provider": "paypal",
    "timestamp": 1640995300,
    "data": {
      "transaction_id": "txn_456",
      "amount": 2500,
      "user_id": "user_xyz",
      "error": "card_declined"
    }
  }
    def get_deduplicated_evetns(self, processed_events: dict):
        deduped = {
            e["event_id"]: e for e in sorted(processed_events, key=lambda e:e["timestamp"])
        }
        customer_status = {
            e["customer_id"] : ("failed" if "error" in e else "") for e in deduped.values()
        }
        return customer_status , list(deduped.values())  
    
    def process_events(self, events: list[dict], max_retries: int =3) :
        queue = [{"event": e, "status": "pending", "retr"}]
            
             
data = [
  {
    "id": "evt_001",
    "type": "payment.succeeded",
    "provider": "stripe",
    "timestamp": 1640995200,
    "data": {
      "payment_id": "pay_123",
      "amount": 5000,
      "customer": "cus_abc"
    }
  },
  {
    "id": "evt_002",
    "type": "payment_failed",
    "provider": "paypal",
    "timestamp": 1640995300,
    "data": {
      "transaction_id": "txn_456",
      "amount": 2500,
      "user_id": "user_xyz",
      "error": "card_declined"
    }
  }
]

eventsService = EventsService()
filtered_events, processed_events = eventsService.handle_events(data, "payment.succeeded")
print(filtered_events)
print(processed_events)
customer_payment_stauts, processed_events_map = eventsService.get_deduplicated_evetns(processed_events)    
print(customer_payment_stauts)
print(processed_events_map)          
              
                               
        
        
        
        
      
            
            
             
    
