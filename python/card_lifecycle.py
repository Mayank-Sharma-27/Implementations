"""
Stripe-Style Multi-Part Problem: Card Authorization Service

This problem simulates the core authorization engine for a product like Stripe
Issuing. The service must process a stream of events for virtual cards,
tracking their lifecycle and approving or declining transactions based on the
card's status and available limit.

The input is a single log string with events separated by '&'. Events must be
processed chronologically by their timestamp.

The event format is: `timestamp;event_type;data`
- event_type: CARD_CREATED, CARD_STATUS_CHANGED, TX_AUTH_REQUEST, or TX_SETTLED.
- data: A semicolon-separated string of key-value pairs (e.g., card_id=c_123).

---

Part 1: Card Lifecycle Tracking
- Determine the final status (ACTIVE, INACTIVE, CANCELED) of each card.

Part 2: Simple Transaction Authorization
- Categorize transactions as 'authorized' or 'declined' based only on whether
  the card is ACTIVE.

Part 3: Managing Authorization Holds
- Enhance authorization logic to use the card's available limit, which decreases
  as transactions are authorized.

Part 4: Final Card Ledger Summary
- Generate a summary for each card, including its final status, limits, and a
  list of settled transactions.
"""
from collections import defaultdict

# ===================================================================================
# User's Original Approach
#
# This solution works but can be complex. It uses multiple functions that each
# re-parse and re-process the data. State is calculated in different places and
# passed between functions, which can be hard to follow and debug.
# ===================================================================================
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
                    # Bug: This uses the FINAL status and limit, not the status/limit at the time of the transaction.
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
        card_summary = {}

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

# ===================================================================================
# Optimized, Modular Solution
#
# This refactored solution follows the "single timeline" principle. A core
# private function `_get_final_system_state` processes all events in one
# chronological pass to build a complete "state" object. The public methods are
# simple, clean wrappers that just format the data from that central state.
# This makes the code more efficient, easier to debug, and more robust.
# ===================================================================================
class AuthorizationService:
    """A clean, modular solution for the Card Authorization Service problem."""

    def _parse_and_sort_log(self, log: str) -> list:
        """Parses the raw log string and sorts all events chronologically."""
        events = []
        for line in log.strip().split('&'):
            if not line:
                continue
            try:
                timestamp, event_type, data_str = line.split(';', 2)
                data = {k: v for k, v in (item.split('=') for item in data_str.split(';')) if item}
                events.append({"timestamp": timestamp, "type": event_type, "data": data})
            except (ValueError, IndexError):
                continue  # Skip malformed lines
        
        return sorted(events, key=lambda e: e["timestamp"])

    def _get_final_system_state(self, log: str) -> dict:
        """
        The core processing engine. Iterates through the sorted log once
        to build a comprehensive final state for the entire system.
        """
        # This check prevents re-computing for the same log string (memoization).
        if hasattr(self, '_cached_state') and self._cached_log == log:
            return self._cached_state
            
        sorted_events = self._parse_and_sort_log(log)
        
        # --- State Tracking Dictionaries ---
        card_info = defaultdict(lambda: {"status": None, "total_limit": 0, "available_limit": 0})
        auth_results = defaultdict(list)
        settled_txs = defaultdict(list)
        tx_to_card_map = {} # Helper to link a settled transaction back to its card

        for event in sorted_events:
            event_type = event["type"]
            data = event["data"]
            card_id = data.get("card_id")

            if event_type == "CARD_CREATED":
                limit = int(data.get("limit", 0))
                card_info[card_id]["total_limit"] = limit
                card_info[card_id]["available_limit"] = limit
            
            elif event_type == "CARD_STATUS_CHANGED":
                if card_id in card_info:
                    card_info[card_id]["status"] = data.get("status")

            elif event_type == "TX_AUTH_REQUEST":
                tx_id = data.get("transaction_id")
                amount = int(data.get("amount", 0))
                
                # Authorization Logic uses the card's state *at this moment in time*
                if card_id in card_info and card_info[card_id]["status"] == "ACTIVE" and card_info[card_id]["available_limit"] >= amount:
                    auth_results["authorized"].append(tx_id)
                    card_info[card_id]["available_limit"] -= amount
                    tx_to_card_map[tx_id] = card_id
                else:
                    auth_results["declined"].append(tx_id)
            
            elif event_type == "TX_SETTLED":
                tx_id = data.get("transaction_id")
                if tx_id in tx_to_card_map:
                    card_id_for_tx = tx_to_card_map[tx_id]
                    settled_txs[card_id_for_tx].append(tx_id)

        # Cache the result for efficiency
        self._cached_log = log
        self._cached_state = {
            "card_info": card_info,
            "auth_results": auth_results,
            "settled_txs": settled_txs
        }
        return self._cached_state

    # --- Public Methods For Each Part ---

    def track_card_lifecycles(self, log: str) -> dict:
        """Solves Part 1."""
        state = self._get_final_system_state(log)
        return {cid: info["status"] for cid, info in state["card_info"].items()}

    def authorize_transactions_simple(self, log: str) -> dict:
        """Solves Part 2."""
        state = self._get_final_system_state(log) # We can reuse the state engine
        # But for this part, the logic is simpler and doesn't use the limit.
        auth_results = defaultdict(list)
        card_statuses = {}
        for event in self._parse_and_sort_log(log): # Reprocess for simpler logic
            if event['type'] == 'CARD_STATUS_CHANGED':
                card_statuses[event['data']['card_id']] = event['data']['status']
            elif event['type'] == 'TX_AUTH_REQUEST':
                tx_id = event['data']['transaction_id']
                card_id = event['data']['card_id']
                if card_statuses.get(card_id) == 'ACTIVE':
                    auth_results['authorized'].append(tx_id)
                else:
                    auth_results['declined'].append(tx_id)
        return dict(auth_results)

    def authorize_with_holds(self, log: str) -> dict:
        """Solves Part 3."""
        state = self._get_final_system_state(log)
        return dict(state["auth_results"])

    def generate_ledger_summary(self, log: str) -> dict:
        """Solves Part 4."""
        state = self._get_final_system_state(log)
        summary = {}
        for cid, info in state["card_info"].items():
            summary[cid] = {
                "status": info["status"],
                "total_limit": info["total_limit"],
                "available_limit": info["available_limit"],
                "settled_txs": sorted(state["settled_txs"].get(cid, []))
            }
        return summary
        

if __name__ == "__main__":
    log_simple = (
        "2025-07-01T10:00:00Z;CARD_CREATED;card_id=card_A;limit=1000&"
        "2025-07-01T10:01:00Z;CARD_STATUS_CHANGED;card_id=card_A;status=ACTIVE&"
        "2025-07-01T10:02:00Z;CARD_CREATED;card_id=card_B;limit=500&"
        "2025-07-01T10:03:00Z;CARD_STATUS_CHANGED;card_id=card_B;status=ACTIVE&"
        "2025-07-01T10:04:00Z;CARD_STATUS_CHANGED;card_id=card_B;status=INACTIVE&"
        "2025-07-01T10:05:00Z;TX_AUTH_REQUEST;transaction_id=tx_1;card_id=card_A;amount=100&"
        "2025-07-01T10:06:00Z;TX_AUTH_REQUEST;transaction_id=tx_2;card_id=card_B;amount=100"
    )

    log_complex = (
        "2025-07-01T10:00:00Z;CARD_CREATED;card_id=card_X;limit=1000&"
        "2025-07-01T10:01:00Z;CARD_STATUS_CHANGED;card_id=card_X;status=ACTIVE&"
        "2025-07-01T10:02:00Z;CARD_CREATED;card_id=card_Y;limit=2000&"
        "2025-07-01T10:05:00Z;TX_AUTH_REQUEST;transaction_id=tx_A;card_id=card_X;amount=800&"
        "2025-07-01T10:03:00Z;CARD_STATUS_CHANGED;card_id=card_Y;status=ACTIVE&"
        "2025-07-01T10:06:00Z;TX_AUTH_REQUEST;transaction_id=tx_B;card_id=card_X;amount=300&"
        "2025-07-01T10:08:00Z;TX_SETTLED;transaction_id=tx_A&"
        "2025-07-01T10:07:00Z;TX_AUTH_REQUEST;transaction_id=tx_C;card_id=card_Y;amount=1500"
    )

    # Use the cleaner, optimized solution for testing
    service = AuthorizationService()

    print("## Part 1: Card Lifecycle Tracking ##")
    print(service.track_card_lifecycles(log_simple))
    print("-" * 50)

    print("## Part 2: Simple Transaction Authorization ##")
    print(service.authorize_transactions_simple(log_simple))
    print("-" * 50)

    print("## Part 3: Managing Authorization Holds ##")
    print(service.authorize_with_holds(log_complex))
    print("-" * 50)

    print("## Part 4: Final Card Ledger Summary ##")
    print(service.generate_ledger_summary(log_complex))
    print("-" * 50)