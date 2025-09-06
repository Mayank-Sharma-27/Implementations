"""

You're building a subscription billing system for Stripe. Customers can have multiple subscriptions with different billing cycles, and you need to process billing events and calculate prorated charges.

{
  "customers": [
    {
      "id": "cus_123",
      "email": "john@example.com",
      "subscriptions": [
        {
          "id": "sub_abc",
          "plan_id": "plan_premium",
          "status": "active",
          "current_period_start": 1640995200,
          "current_period_end": 1643673600,
          "created": 1640995200
        }
      ]
    }
  ],
  "plans": [
    {
      "id": "plan_premium", 
      "amount": 2999,
      "currency": "usd",
      "interval": "month",
      "interval_count": 1
    }
  ],
  "events": [
    {
      "id": "evt_001",
      "type": "customer.subscription.created",
      "created": 1640995200,
      "data": {
        "customer_id": "cus_123",
        "subscription_id": "sub_abc",
        "plan_id": "plan_premium"
      }
    },
    {
      "id": "evt_002", 
      "type": "customer.subscription.updated",
      "created": 1641081600,
      "data": {
        "customer_id": "cus_123",
        "subscription_id": "sub_abc", 
        "plan_id": "plan_basic"
      }
    }
  ]
}
"""

from collections import defaultdict

class SubscriptionManager:
    
    def get_all_subscriptions_for_customer(self, info: dict) -> list[dict]:
        customers = info["customers"]
        customer_mappings = defaultdict()
        for customer in customers:
            c_id = customer["id"]
            email = customer["email"]
            subscriptions = customer["subscriptions"]
            customer_mappings[c_id] = {
                "email": email,
                "subscriptions": subscriptions
            }
        return customer_mappings
        
    def get_all_events_for_customer(self, info: dict) -> list[dict]:
        events = info["events"]
        customer_event_mappings = defaultdict(list)
        for event in events:
            customer_id = event["data"]["customer_id"]
            events_list = customer_event_mappings.get(customer_id, [])
            events_list.append(event)
            customer_event_mappings[customer_id] = events_list
        
        for customer_id in customer_event_mappings.keys():
            customer_event_mappings[customer_id] = sorted(customer_event_mappings[customer_id], key=lambda e: e      ["created"])    
        return customer_event_mappings   
        
    def get_plan_mapping(self, info: dict) -> list[dict]:
        plans = info["plans"]
        plan_mapping = defaultdict()
        for plan in plans:
            plan_id = plan["id"]
            amount = plan["amount"]
            plan_mapping[plan_id] = {
                "amount": int(amount)
            }
        return plan_mapping
    
    def get_all_active_subscriptions_for_customer(self, customer_mappings: dict) -> list[dict]:
        active_subs = []
        
        for key in customer_mappings.keys():
            for sub in  customer_mappings.get(key)["subscriptions"]:
                if sub["status"] == "active":
                    active_subs.append(sub)
                    
        return active_subs 
        
                    
                    
    def get_total_revenue_across_sub(self, active_subs: dict, sub_id: str, plan_mapping: dict) -> int:
        ans = 0
        for active_sub in active_subs:
            if active_sub["id"] == sub_id:
                plan_id = active_sub["plan_id"]
                ans += plan_mapping[plan_id]["amount"] 
        return ans       
                        

data = {
  "customers": [
    {
      "id": "cus_123",
      "email": "john@example.com",
      "subscriptions": [
        {
          "id": "sub_abc",
          "plan_id": "plan_premium",
          "status": "active",
          "current_period_start": 1640995200,
          "current_period_end": 1643673600,
          "created": 1640995200
        }
      ]
    }
  ],
  "plans": [
    {
      "id": "plan_premium", 
      "amount": 2999,
      "currency": "usd",
      "interval": "month",
      "interval_count": 1
    }
  ],
  "events": [
    {
      "id": "evt_001",
      "type": "customer.subscription.created",
      "created": 1640995200,
      "data": {
        "customer_id": "cus_123",
        "subscription_id": "sub_abc",
        "plan_id": "plan_premium"
      }
    }
  ]
}

subs = SubscriptionManager()
customer_mappings = subs.get_all_subscriptions_for_customer(data)
print(customer_mappings["cus_123"])
active_subscriptions = subs.get_all_active_subscriptions_for_customer(customer_mappings)
print(active_subscriptions)
plan_mapping = subs.get_plan_mapping(data)
print(subs.get_total_revenue_across_sub(active_subscriptions, "sub_abc", plan_mapping))
customer_event_mappings = subs.get_all_events_for_customer(data)
print(customer_event_mappings["cus_123"])