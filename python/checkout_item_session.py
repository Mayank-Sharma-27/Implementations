
from collections import defaultdict
class CheckoutItemSession:
    def parse_events(self, logs: str) -> dict:
        if not logs:
            return ValueError("Invalid Input")
        
        events = []
        logs_tokens = logs.split("|")
        for log_token in logs_tokens:
            parts = log_token.split(";")
            
            timestamp = parts[0]
            event_type = parts[1]
            data_fields = parts[2:] 
            #print(data_fields) 
            data ={} 
            if len(data_fields) < 2:
                
                data ={}    
            else:
                for field in data_fields:
                    key = field.split("=")[0].strip()
                    value = field.split("=")[1].strip()
                    data[key] = value
            
            events.append({
                "timestamp": timestamp,
                "event_type": event_type,
                "data": data
            })
        events = sorted(events, key=lambda e: e["timestamp"])
        
        order_information = {}
        order_information["items"] = {}
        order_information["subtotal"] = 0
        order_information["discount_applied"] = 0
        order_information["total_order"] = 0
        
        for event in events:
            event_type = event["event_type"]
            data = event["data"]
            
            if event_type == "ITEM_ADDED":
               item_id = data["item_id"]
               price = int(data["price"])
               quantity = int(data["quantity"])
               cost = price * quantity 
               order_information["items"][item_id] = {"item_id": item_id, "price": int(price), "quantity": int(quantity)}
               order_information["subtotal"] += cost
               order_information["total_order"] += cost
               
            elif event_type == "ITEM_REMOVED":
                 item_id = data["item_id"]
                 if order_information["items"].get(item_id) is None:
                     return ValueError("Invalid event") 
                 else:
                   quantity = int(data["quantity"])  
                   current_quantity = order_information["items"][item_id]["quantity"]
                   item_information = order_information["items"][item_id]
                   order_information["items"][item_id]["quantity"] = current_quantity - quantity
                   item_price = item_information["price"]
                   cost =  item_price * quantity
                   order_information["subtotal"] -= cost
                   order_information["total_order"] -= cost
                   if order_information["items"][item_id]["quantity"] == 0:
                       del order_information["items"][item_id]
            elif event_type == "COUPON_APPLIED":
                
                value = int(data["value"])
                current_total_order = int(order_information["total_order"])
                type = data["type"]
                if type == "PERCENT":
                    discount_applied =  (current_total_order * value) // 100 
                else:
                    discount_applied = value
                    
                order_information["total_order"] -= discount_applied
                order_information["discount_applied"] += discount_applied
                   
        return order_information
    
    def get_list_of_items(self, logs: str) -> list:
        order_information = self.parse_events(logs)
        return order_information["items"]
    
    def get_subtotal(self, logs: str) -> int:
        order_information = self.parse_events(logs)
        return order_information["subtotal"]
    
    def get_final_total(self, logs: str) -> int:
        order_information = self.parse_events(logs)
        return order_information["total_order"]
    
    def get_order_infomration(self, logs: str) -> dict:
        order_information = self.parse_events(logs)
        return order_information
    
if __name__ == "__main__":
        
       # --- Test Data ---
    session_log = (
        "2025-03-10T10:00:00Z;ITEM_ADDED;item_id=prod_A;price=1000;quantity=2|"
        "2025-03-10T10:01:00Z;ITEM_ADDED;item_id=prod_B;price=500;quantity=1|"
        "2025-03-10T10:02:00Z;ITEM_REMOVED;item_id=prod_A;quantity=1|"
        "2025-03-10T10:03:00Z;COUPON_APPLIED;coupon_id=SAVE10;type=PERCENT;value=10|"
        "2025-03-10T10:04:00Z;PURCHASE_CONFIRMED;"
    )

    # Instantiate your solution class
    service = CheckoutItemSession() # Replace with your class name

    # --- Part 1 ---
    print("## Part 1: Shopping Cart Contents ##")
    # Expected: A map like {'prod_A': 1, 'prod_B': 1}
    print(service.get_list_of_items(session_log))
    print("-" * 50)


    # --- Part 2 ---
    print("## Part 2: Subtotal Calculation ##")
    # Expected: An integer `1500`
    print(service.get_subtotal(session_log))
    print("-" * 50)


    # --- Part 3 ---
    print("## Part 3: Applying a Discount ##")
    # Expected: An integer `1350`
    print(service.get_final_total(session_log))
    print("-" * 50)


    # --- Part 4 ---
    print("## Part 4: Final Order Summary ##")
    # Expected: A summary object like:
    # {
    #   'items': {'prod_A': 1, 'prod_B': 1},
    #   'subtotal': 1500,
    #   'discount_applied': 150,
    #   'final_total': 1350
    # }
    print(service.get_order_infomration(session_log))
    print("-" * 50)                          
                   
            
                