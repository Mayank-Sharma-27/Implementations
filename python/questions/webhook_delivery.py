"""
Problem 11: Webhook Delivery Attempt Simulator
Story
When an event occurs, Stripe sends a "webhook" notification to a user's server. If the server fails to respond, Stripe retries with an exponential backoff delay. You are building a simulator for this logic.

Input Format
A list of webhook events to be sent, format: event_id;url.
Retry policy parameters: initial_delay_seconds, max_retries.
A log of server responses, separated by &. Format: timestamp;event_id;http_status. 200 is a success.
The Task
Initial Delivery Status: Determine if each event's first delivery attempt was a success or failure.
Retry Schedule: For every event that initially failed, generate a schedule of when subsequent retries should have occurred.
Final Event Status: Determine the final status for each event: DELIVERED or FAILED.
Unreliable Endpoints: An "unreliable" url is one that failed to accept an event more than 3 times in a row for any single event. Identify all unreliable URLs.
Sample Input
events_to_send = ["evt_A;http://endpoint.com/a", "evt_B;http://endpoint.com/b"]
policy = {"initial_delay_seconds": 60, "max_retries": 3}
response_log = "2025-08-01T12:00:00Z;evt_A;503&2025-08-01T12:01:00Z;evt_A;503&2025-08-01T12:02:00Z;evt_B;200&2025-08-01T12:03:00Z;evt_A;200"
"""
from collections import defaultdict
from datetime import datetime, timedelta
class WebhookDelivery:
    def parse_events(self, logs: str) -> dict:
        response_logs_tokens = logs.split("&")
        events = []
        for response_log_token in response_logs_tokens:
            timestamp, event_id, http_status = response_log_token.split(";")
            
            events.append({
                "timestamp": timestamp,
                "event_id": event_id,
                "http_status": int(http_status)
            })
        events = sorted(events, key=lambda p:p["timestamp"])
        
        events_mapping = defaultdict(list)
        
        for event in events:
            event_id = event["event_id"]
            time = datetime.fromisoformat(event["timestamp"].replace('Z', '+00:00'))
            http_status = event["http_status"]
            events_mapping[event_id].append({
                "time": time,
                "http_status": http_status
            })
        return events_mapping   
        
    def get_initial_status(self, logs: str) ->  dict:
        events_mapping = self.parse_events(logs)
        
        event_initial_status_map = {}
        
        for id, events in events_mapping.items():
            initial_status = events[0]["http_status"]
            print(f"{events[0]} : {id}")
            if initial_status != 200:
               event_initial_status_map[id] = "FAILED"
            else:
               event_initial_status_map[id] = "DELIVERED"  
        
        return event_initial_status_map
    
    def get_retry_schedule(self, logs: str, policy: dict) -> dict:
        events_mapping = self.parse_events(logs)
        events_to_retry_schdule = defaultdict(list)
        max_retries = int(policy["max_retries"])
        delay = int(policy["initial_delay_seconds"])
        for id, events in events_mapping.items():
            initial_status = events[0]["http_status"]
            if initial_status != 200:
               time = events[0]["time"]
               current_delay = int(policy["initial_delay_seconds"]) # Start with the initial delay
               time = events[0]["time"]    
               for i in range (0, max_retries):
                   time =  time + timedelta(seconds=current_delay)
                   events_to_retry_schdule[id].append(time)
                   current_delay = current_delay * 2
        
        return events_to_retry_schdule
    
    def get_final_event_status(self, logs: str) -> dict:
        events_mapping = self.parse_events(logs)
        
        event_final_status_map = {}
        
        for id, events in events_mapping.items():
            event_index = len(events) -1
            initial_status = events[event_index]["http_status"]
            if initial_status != 200:
               event_final_status_map[id] = "FAILED"
            else:
               event_final_status_map[id] = "DELIVERED"  
        
        return event_final_status_map
    
    def get_unreliable_url(self, logs: str, events_to_send: dict) -> dict:
        events_mapping = self.parse_events(logs)
        
        unreliable_events = []
        events_mapping_url = {}
        for event in events_to_send:
            token = event.split(";")
            id = token[0].strip()
            url = token[1].strip()
            events_mapping_url[id] = url
           
        
        for id, events in events_mapping.items():
            consecutive = 0
            last_event = None
            for event in events:
                status = event["http_status"]
                if status != 200:
                    consecutive += 1
                else:
                    consecutive = 0
                if consecutive == 3:
                   unreliable_events.append(events_mapping_url[id])        
                          
                
        return unreliable_events

if __name__ == "__main__":
    # --- Test Data ---
    events_to_send = [
        "evt_A;http://endpoint.com/a",  # Will fail, then succeed
        "evt_B;http://endpoint.com/b",  # Will succeed on the first try
        "evt_C;http://endpoint.com/a"   # Will fail all retries
    ]
    
    policy = {"initial_delay_seconds": 60, "max_retries": 3}
    
    response_log = (
        "2025-08-01T12:00:00Z;evt_A;503&"  # evt_A: First attempt fails
        "2025-08-01T12:01:00Z;evt_A;503&"  # evt_A: First retry fails
        "2025-08-01T12:02:00Z;evt_B;200&"  # evt_B: First attempt succeeds
        "2025-08-01T12:03:00Z;evt_A;200&"  # evt_A: Second retry succeeds
        "2025-08-01T12:10:00Z;evt_C;500&"  # evt_C: First attempt fails
        "2025-08-01T12:11:00Z;evt_C;500&"  # evt_C: First retry fails
        "2025-08-01T12:13:00Z;evt_C;500&"  # evt_C: Second retry fails
        "2025-08-01T12:17:00Z;evt_C;503"   # evt_C: Third retry fails
    )

    # Instantiate your solution class
    simulator = WebhookDelivery() # Replace with your class name

    # --- Part 1 ---
    print("## Part 1: Initial Delivery Status ##")
    # Expected: A map like {'evt_A': 'FAILURE', 'evt_B': 'SUCCESS', 'evt_C': 'FAILURE'}
    print(simulator.get_initial_status(response_log))
    print("-" * 50)


    # --- Part 2 ---
    print("## Part 2: Retry Schedule ##")
    # Expected: For evt_A (failed at 12:00:00), schedule would be [12:01:00, 12:03:00, 12:07:00]
    # {'evt_A': ['2025-08-01T12:01:00Z', '2025-08-01T12:03:00Z', ...], 'evt_C': [...]}
    print(dict(simulator.get_retry_schedule(response_log, policy)))
    print("-" * 50)


    # --- Part 3 ---
    print("## Part 3: Final Event Status ##")
    # Expected: {'evt_A': 'DELIVERED', 'evt_B': 'DELIVERED', 'evt_C': 'FAILED'}
    print(simulator.get_final_event_status(response_log))
    print("-" * 50)


    # --- Part 4 ---
    print("## Part 4: Unreliable Endpoints ##")
    # Expected: A list containing 'http://endpoint.com/a' because evt_C failed more than 3 times in a row.
    # ['http://endpoint.com/a']
    print(simulator.get_unreliable_url( response_log, events_to_send))
    print("-" * 50)    
                   
                   
            
              
        
    
        
        