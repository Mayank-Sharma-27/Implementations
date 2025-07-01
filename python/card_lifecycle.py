from collections import defaultdict
class CardLifeCycle:
    def parse_card_events(self, events: str):
        card_events = defaultdict(list)
        card_last_status = {}
        card_limits = {}
        transaction_events = defaultdict(list)
       
        card_events_tokens = events.split("&")
       
        for card_event in card_events_tokens:
            event_info = {}
            id = None
            transaction_id = None
            timestamp = card_event.split(";")[0].strip()
            event_info["timestamp"] = card_event.split(";")[0].strip()
            event = card_event.split(";")[1].strip()
            event_info["event"] = event
            for event in card_event.split(";")[2:]:
                key = event.split("=")[0].strip()
     
                value = event.split("=")[1].strip()
                
                if key == "card_id":
                    id = value
                if key == "transaction_id" :
                    transaction_id = value   
                event_info[key] = value
            
            if transaction_id:
               transaction_events[transaction_id].append(event_info)    
            if id:
                card_events[id].append(event_info)  
               
        
        for transaction_id in transaction_events.keys():
            transaction_events[transaction_id] = sorted(transaction_events[transaction_id], key=lambda k: k ["timestamp"])
        
        for card_id in card_events.keys():
            card_events[card_id] = sorted(card_events[card_id], key=lambda k: k ["timestamp"])
            if card_id is None:
                print(card_id)
            for events in card_events[card_id]:
                if events.get("status"):
                   card_last_status[card_id] = events["status"]
                if events.get("limit"):
                   card_limits[card_id] = {"initial_limit": int(events["limit"]), "current_limit": int(events["limit"])}    
                 
        return card_events, card_last_status,card_limits, transaction_events     
               
    def get_last_known_card_status(self, events: str) -> dict:
        card_events, card_last_status, card_limits, transaction_events = self.parse_card_events(events)  
    
        return card_last_status

    def get_transaction_auth(self, events: str) -> dict:
        card_events, card_last_status, card_limits, transaction_events = self.parse_card_events(events)  
        authorized= []
        declined =[]
        for id, events in transaction_events.items():
            for event in events:
                if event["event"] == "TX_AUTH_REQUEST":
                    card_id = event["card_id"]
                    if card_last_status[card_id] == "ACTIVE":
                        authorized.append(id)
                    else:
                        declined.append(id)
                    
        return {"declined": declined, "authorized":authorized} 

    def get_transaction_auth_v2(self, events: str):
        card_events, card_last_status, card_limits, transaction_events = self.parse_card_events(events)  
        authorized= []
        declined =[]
        settled_transactions = {}
        for id, events in transaction_events.items():
            for event in events:
                if event["event"] == "TX_AUTH_REQUEST":
                    amount = int(event["amount"])
                    card_id = event["card_id"]
                    if card_last_status[card_id] == "ACTIVE" and int(card_limits[card_id]["current_limit"]) > amount:
                        card_limits[card_id]["current_limit"] -= amount
                        authorized.append(id)
                    else:
                        declined.append(id)
                elif event["event"] == "TX_SETTLED":
                    card_id = None
                    for data in transaction_events[id]:
                        if data.get("card_id"):
                           card_id = data.get("card_id") 
                    if card_id:
                        settled_transactions[id] = card_id 
                        
        ans = {"declined": declined, "authorized":authorized}             
        return ans, card_limits, card_last_status, settled_transactions
    
    
    def get_summary(self, events: str) -> dict:
        card_events, card_last_status, card_limits, transaction_events = self.parse_card_events(events)
        transaction_information, card_limits, card_last_status, settled_transactions = self.get_transaction_auth_v2(events)
        settled_transactions_for_card = {}
        print(f"transaciton events {settled_transactions}")
        print("\n")
        card_summary = {}
        #print(card_events)
        for card_id in card_events.keys():
            events =  card_events[card_id]
            status = card_last_status[card_id]
            card_summary[card_id] = {
            "status" :  status,
            "total_limit": card_limits[card_id]["initial_limit"],
            "available_limit": card_limits[card_id]["current_limit"],
            "settled_transactions": []
            }
        for key in settled_transactions.keys():
            if settled_transactions[key]:
               card_summary[settled_transactions[key]]["settled_transactions"].append(key)
               
        for summary in card_summary.values():
            summary["settled_transactions"] = sorted(summary["settled_transactions"])         
                      
                
        return card_summary                 
                
if __name__ == "__main__":
    # --- Test Data for Parts 1 & 2 (Simpler Logic) ---
    log_simple = (
        "2025-07-01T10:00:00Z;CARD_CREATED;card_id=card_A;limit=1000&"
        "2025-07-01T10:01:00Z;CARD_STATUS_CHANGED;card_id=card_A;status=ACTIVE&"
        "2025-07-01T10:02:00Z;CARD_CREATED;card_id=card_B;limit=500&"
        "2025-07-01T10:03:00Z;CARD_STATUS_CHANGED;card_id=card_B;status=ACTIVE&"
        "2025-07-01T10:04:00Z;CARD_STATUS_CHANGED;card_id=card_B;status=INACTIVE&"
        "2025-07-01T10:05:00Z;TX_AUTH_REQUEST;transaction_id=tx_1;card_id=card_A;amount=100&" # Should be authorized
        "2025-07-01T10:06:00Z;TX_AUTH_REQUEST;transaction_id=tx_2;card_id=card_B;amount=100"  # Should be declined
    )

    # --- Test Data for Parts 3 & 4 (Complex State Logic) ---
    log_complex = (
        "2025-07-01T10:00:00Z;CARD_CREATED;card_id=card_X;limit=1000&"
        "2025-07-01T10:01:00Z;CARD_STATUS_CHANGED;card_id=card_X;status=ACTIVE&"
        "2025-07-01T10:02:00Z;CARD_CREATED;card_id=card_Y;limit=2000&"
        "2025-07-01T10:05:00Z;TX_AUTH_REQUEST;transaction_id=tx_A;card_id=card_X;amount=800&"  # Authorized, available limit becomes 200
        "2025-07-01T10:03:00Z;CARD_STATUS_CHANGED;card_id=card_Y;status=ACTIVE&"
        "2025-07-01T10:06:00Z;TX_AUTH_REQUEST;transaction_id=tx_B;card_id=card_X;amount=300&"  # Declined, exceeds available limit
        "2025-07-01T10:08:00Z;TX_SETTLED;transaction_id=tx_A&"
        "2025-07-01T10:07:00Z;TX_AUTH_REQUEST;transaction_id=tx_C;card_id=card_Y;amount=1500" # Authorized
    )

    # Instantiate your solution class
    service = CardLifeCycle() # Replace with your class name

    # --- Part 1 ---
    print("## Part 1: Card Lifecycle Tracking ##")
    # Expected: A map like {'card_A': 'ACTIVE', 'card_B': 'INACTIVE'}
    print(dict(service.get_last_known_card_status(log_simple)))
    print("-" * 50)


    # --- Part 2 ---
    print("## Part 2: Simple Transaction Authorization ##")
    # Expected: A map like {'authorized': ['tx_1'], 'declined': ['tx_2']}
    print(service.get_transaction_auth(log_simple))
    print("-" * 50)


    # --- Part 3 ---
    print("## Part 3: Managing Authorization Holds ##")
    # Expected: A map like {'authorized': ['tx_A', 'tx_C'], 'declined': ['tx_B']}
    print(service.get_transaction_auth_v2(log_complex)[0])
    print("-" * 50)


    # --- Part 4 ---
    print("## Part 4: Final Card Ledger Summary ##")
    # Expected: A map mapping card_id to its summary.
    # For card_X: {'status': 'ACTIVE', 'total_limit': 1000, 'available_limit': 200, 'settled_txs': ['tx_A']}
    # For card_Y: {'status': 'ACTIVE', 'total_limit': 2000, 'available_limit': 500, 'settled_txs': []}
    print(service.get_summary(log_complex))
    print("-" * 50)

               
           
            