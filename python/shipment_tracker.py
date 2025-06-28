"""
Problem: Shipment Event Tracker

You are building a shipment event tracker that processes raw event strings and supports generating meaningful reports. 
The events are given as a single string where each event is delimited by a semicolon (`;`). 
Each event has the following format:

    <shipment_id>|<carrier>|<status>|<timestamp>

### Status Normalization:
Since status updates come from various systems, the status can be inconsistent.
You must normalize statuses to one of the following:
- "PICKED_UP" (includes: "pickup", "collected", "PICKED_UP")
- "IN_TRANSIT" (includes: "in_transit", "moving", "ON_THE_WAY")
- "DELIVERED" (includes: "delivered", "DELIVERED")

### Your Task: Implement the following features

**Part 1: `get_shipment_info(events)`**
- Parse all events and group them by shipment ID
- Normalize the statuses
- Sort events for each shipment by timestamp
- Return a dictionary of shipments and their sorted status timelines (status + timestamp)

**Part 2: `generate_status_report(events)`**
- Use the result from Part 1
- Print a user-friendly status report:
  - One section per shipment, with carrier and sorted status history

**Part 3: `get_unique_events(events)`**
- Remove duplicate event entries (identical event strings)
- Then parse and sort as in Part 1

**Part 4: `get_last_known_status(events)`**
- From the unique events, get the most recent status per shipment based on timestamp

---

### Sample Input:
```python
events = (
    "ship123|UPS|pickup|2024-12-01T10:00:00Z;"
    "ship123|UPS|in_transit|2024-12-02T14:30:00Z;"
    "ship124|DHL|PICKED_UP|2024-12-01T09:00:00Z;"
    "ship123|UPS|in_transit|2024-12-02T14:30:00Z;"   # duplicate
    "ship124|DHL|moving|2024-12-01T12:00:00Z;"
    "ship125|FEDEX|delivered|2024-12-03T08:00:00Z"
)
"""

from collections import defaultdict

class ShipmentTracker:
    
    def _get_shipment_dict(self, events: str) -> dict:
        events_token = events.split(";")
        return self._get_dict(events_token)
    
    def _get_dict(self, events_token: str) -> dict:
        shipment_info = defaultdict(list)
        for event_token in events_token:
            event = event_token.split("|")
            shipment_id = event[0].strip()
            status = self._get_normalized_status(event[2].strip())
            timestamp = event[3].strip()
            carrier = event[1].strip()
            shipment_info[shipment_id].append({
                "status": status,
                "timestamp": timestamp,
                "carrier": carrier
            })
        return shipment_info     
        
    
    def get_shipment_info(self, events: str) -> dict:
        ans = defaultdict(list)
        
        shipments= self.get_unique_events(events)
        for shipment_id  in  shipments.keys():
            for event in shipments[shipment_id]:
                ans[shipment_id].append({
                    "status": event["status"],
                    "timestamp": event["timestamp"]
                }) 
        
        for shipment_id in ans.keys():
            ans[shipment_id] = sorted(ans[shipment_id], key=lambda p: p["timestamp"])          
        
        return ans
    
    def generate_status_report(self, events: str) -> str:
        lines = []
        shipment_info = self.get_unique_events(events)
        
        for shipment_id  in  shipment_info.keys():
            shipment_info[shipment_id] = sorted(shipment_info[shipment_id], key=lambda p: p["timestamp"])
        
        for shipment_id  in  shipment_info.keys():
            carrier = shipment_info[shipment_id][0]["carrier"]
            lines.append(f"Shipment {shipment_id} with carrier {carrier} has status updates")
            for event in shipment_info[shipment_id]:
                status = event["status"]
                timestamp = event["timestamp"]
                lines.append(f"- {status} at {timestamp}")
            lines.append("")
        
        return "\n".join(lines)
    
    def get_unique_events(self, events: str) -> dict:
        unique_events = set()
        events_token = events.split(";")
        for event_token in events_token:
            unique_events.add(event_token)
        shipment_info = self._get_dict(unique_events)
        
        for shipment_id  in  shipment_info.keys():
            shipment_info[shipment_id] = sorted(shipment_info[shipment_id], key=lambda p: p["timestamp"])
        
        return shipment_info
    
    def get_last_known_status(self, events: str) -> str:
        shipment_info = self.get_unique_events(events)
        lines = []
        
        for shipment_id in sorted(shipment_info.keys()):
            events = shipment_info[shipment_id]
            if events:
                event = events[-1]
                carrier = event["carrier"]
                status = event["status"]
                lines.append(f"{shipment_id} - {carrier}: {status}")
                lines.append("")
        return "\n".join(lines)        
                
                               
    
    def _get_normalized_status(self, status: str) -> str:
        if status == "pickup" or status == "collected" or status == "PICKED_UP":
            return "PICKED_UP" 
        elif status == "in_transit" or status == "moving" or status == "ON_THE_WAY":
            return "IN_TRANSIT" 
        elif status == "delivered" or status == "DELIVERED":
            return "DELIVERED"  

if __name__ == "__main__":
    events = (
    "ship123|UPS|pickup|2024-12-01T10:00:00Z;"
    "ship123|UPS|in_transit|2024-12-02T14:30:00Z;"
    "ship124|DHL|PICKED_UP|2024-12-01T09:00:00Z;"
    "ship123|UPS|in_transit|2024-12-02T14:30:00Z;"   # duplicate
    "ship124|DHL|moving|2024-12-01T12:00:00Z;"
    "ship125|FEDEX|delivered|2024-12-03T08:00:00Z"
    )
    shipmentTracker = ShipmentTracker()
    
    print(dict(shipmentTracker.get_shipment_info(events)))
    print("\n")
    print(shipmentTracker.generate_status_report(events))
    print("\n")
    print(dict(shipmentTracker.get_unique_events(events)))
    print("\n")
    print(shipmentTracker.get_last_known_status(events))
    

            
        