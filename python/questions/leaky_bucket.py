"""
Problem 3: API Rate Limiter (Leaky Bucket)
Story
You are implementing a "leaky bucket" rate limiter to protect a critical API endpoint. Requests of different "sizes" add "water" to a bucket. The bucket leaks at a constant rate. A request is rejected if adding its size would cause the bucket to overflow.

Input Format
A log of API requests separated by ~. Format: timestamp;api_key;request_id;request_size.
Initial parameters: bucket_capacity, leak_rate_per_second.
The Task
Simple Request Counter: Implement a basic rate limiter that only counts the number of requests in the last 60 seconds per api_key.
Leaky Bucket Implementation: Implement the core leaky bucket logic. At the time of each request, calculate how much has leaked, then determine if the new request fits.
Request Outcomes: Process the log chronologically and return a map of each request_id to its outcome: ACCEPTED or REJECTED.
Per-Key Summary: Generate a summary report for each api_key, including total requests received, accepted, and rejected.
Sample Input
requests_log = "2025-01-01T10:00:00Z;key_A;req_1;10~2025-01-01T10:00:00Z;key_A;req_2;15~2025-01-01T10:00:01Z;key_A;req_3;20"
bucket_capacity = 30
leak_rate_per_second = 10


Make sure to sort the events before doing anything

"""

from collections import defaultdict
from datetime import datetime
class LeakyBucket:
    
    def parse_events(self, request_logs: str, leak_rate_per_second: int, bucket_capacity: int) -> dict:
        api_map = defaultdict(dict)
        request_map = defaultdict(list)
        
        request_logs_tokens = request_logs .split("~")
        buckets = defaultdict(lambda: {"current_size": 0.0, "last_updated_time": None})
        
        all_events = []
        for request_logs_token in request_logs.strip().split("~"):
            try:
                timestamp_str, api_key, request_id, size = request_logs_token.split(";")
                all_events.append({
                    "timestamp": datetime.fromisoformat(timestamp_str.replace('Z', '+00:00')),
                    "api_key": api_key,
                    "request_id": request_id,
                    "size": int(size)
                })
            except (ValueError, IndexError):
                continue

        # --- FIX: Step 2 - Sort events to process them chronologically ---
        sorted_events = sorted(all_events, key=lambda e: e["timestamp"])
        api_map = defaultdict(lambda: defaultdict(list))

        for event in sorted_events:
            api_key = event["api_key"]
            current_time = event["timestamp"]
            
            # Initialize the bucket's time on its first request.
            if buckets[api_key]["last_updated_time"] is None:
                buckets[api_key]["last_updated_time"] = current_time

            # --- FIX: Step 4 - Calculate leak based on TIME ELAPSED ---
            time_delta = (current_time - buckets[api_key]["last_updated_time"]).total_seconds()
            leaked_amount = time_delta * leak_rate_per_second
            
            current_size = buckets[api_key]["current_size"]
            new_size_after_leak = max(0, current_size - leaked_amount)
            
            # This is the event object that will be stored.
            event_output = {
                "request_id": event["request_id"],
                "size": event["size"],
                "timestamp": event["timestamp"].isoformat().replace('+00:00', 'Z'),
            }

            # Check if the new request fits.
            if new_size_after_leak + event["size"] <= bucket_capacity:
                event_output["status"] = "ACCEPTED"
                buckets[api_key]["current_size"] = new_size_after_leak + event["size"]
            else:
                event_output["status"] = "REJECTED"
                buckets[api_key]["current_size"] = new_size_after_leak

            # Update the time for the bucket.
            buckets[api_key]["last_updated_time"] = current_time
            
            # Store the result in the nested structure your code expects.
            minute = event['timestamp'].strftime('%M')
            api_map[api_key][minute].append(event_output)
               
        return api_map
    
    def get_number_of_requests_per_api(self, request_logs: str, leak_rate_per_second: int, bucket_capacity: int) -> dict:
        api_map = self.parse_events(request_logs, leak_rate_per_second, bucket_capacity)
        
        request_counts = {}
        
        for api in api_map:
            request_counts[api] = defaultdict(int)
            for keys in api_map[api].keys():
                request_counts[api][keys] += len(api_map[api][keys]) 
        
        return  request_counts       
    
    def get_leaky_bucket(self, request_logs: str, leak_rate_per_second: int, bucket_capacity: int)  -> dict:
        api_map = self.parse_events(request_logs, leak_rate_per_second, bucket_capacity)   
        return api_map
    
    def get_request_map(self, request_logs: str, leak_rate_per_second: int, bucket_capacity: int) -> dict:
        api_map = self.parse_events(request_logs, leak_rate_per_second, bucket_capacity)  
        ans = {}
        for api in api_map:
            for list in api_map[api].values():
                for event in list:
                    request_id = event["request_id"]
                    outcome = event["status"]
                    ans[request_id] = outcome
        
        return ans                     
                         
    def  get_summary(self, request_logs: str, leak_rate_per_second: int, bucket_capacity: int) -> dict:
        api_map = self.parse_events(request_logs, leak_rate_per_second, bucket_capacity)   
        return api_map 
        
if __name__ == "__main__":
    requests_log = "2025-01-01T10:00:00Z;key_A;req_1;10~2025-01-01T10:00:00Z;key_A;req_2;15~2025-01-01T10:00:01Z;key_A;req_3;20"
    bucket_capacity = 30
    leak_rate_per_second = 10 
    leaky_bucket = LeakyBucket()
    
    print("Part 1")
    
    print(dict(leaky_bucket.get_number_of_requests_per_api(requests_log, leak_rate_per_second, bucket_capacity))) 
    
    print("part 2")
    
    print(leaky_bucket.get_leaky_bucket(requests_log, leak_rate_per_second, bucket_capacity)) 
    
    print("part 3")
    print(leaky_bucket.get_request_map(requests_log, leak_rate_per_second, bucket_capacity))     
    
    
    print("part4")
    
    print(leaky_bucket.get_summary(requests_log, leak_rate_per_second, bucket_capacity))    
              
        