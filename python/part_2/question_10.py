"""
## Question 10: API Rate Limiting System

### Background
Implement a rate limiting system for API requests.

### Input Data
```json
{
  "requests": [
    {
      "api_key": "sk_test_123",
      "endpoint": "/v1/charges",
      "timestamp": 1640995200,
      "ip": "192.168.1.1"
    },
    {
      "api_key": "sk_test_123",
      "endpoint": "/v1/charges", 
      "timestamp": 1640995201,
      "ip": "192.168.1.1"
    }
  ],
  "limits": {
    "sk_test_123": {
      "requests_per_minute": 100,
      "requests_per_hour": 1000
    }
  }
}
```

### Part 1 (15 minutes)
Build rate limiter:
1. **Track requests per API key**
2. **Check minute and hour limits**
3. **Return allow/deny decision**

### Part 2 (15 minutes)
Add sliding window:
1. **Implement sliding window counter**
2. **Clean up old request data**
3. **Handle burst traffic**

### Part 3 (15 minutes)
Advanced features:
1. **Different limits per endpoint**
2. **IP-based rate limiting**
3. **Rate limit headers** (X-RateLimit-Remaining, etc.)
"""

from collections import defaultdict, Counter, deque
from datetime import datetime
class RateLimiter:
      
    def track_requests(self, data: dict) -> dict:
        key_request_mappings = defaultdict(list)
        minute_request_mapping = Counter()
        hour_mapping = Counter()
        decision_mapping = {}
        requests = data["requests"]
        for i,request in enumerate(requests):
            api_key = request["api_key"]
            limits = data["limits"][api_key]
            key_request_mappings[api_key].append(request)
            dt = datetime.fromtimestamp(request["timestamp"])
            minute = dt.strftime("%Y-$m%d %H:%M")
            hour = dt.strftime("%y-%m-%d %H")
            
            minute_key = f"{minute}:{api_key}"
            hour_key = f"{hour}:{api_key}"
            
            minute_request_mapping[minute_key] +=1
            hour_mapping[hour_key] +=1
            
            decision_key= f"{api_key}:{request["timestamp"]}:{i}"
            
            if minute_request_mapping[minute_key]> limits["requests_per_minute"]:
                decision_mapping[decision_key] ="DENY"
            elif hour_mapping[hour_key] > limits["requests_per_hour"]:
                decision_mapping[decision_key] ="DENY"
            else:
                decision_mapping[decision_key] ="ALLOW"        
      
        return {"decision_mapping": decision_mapping, "key_request_mappings":key_request_mappings}  

    def track_requests_sliding_window(self, data: dict) -> dict:
        key_request_mappings = defaultdict(list)
        minute_request_mapping = defaultdict(deque)
        hour_mapping = defaultdict(deque)
        decision_mapping = {}
        requests = data["requests"]
        for i,request in enumerate(requests):
            api_key = request["api_key"]
            limits = data["limits"][api_key]
            
            endpoint = request["endpoint"]
            ip = request["ip"]
            timestamp = request["timestamp"]
            req_per_min = limits.get("requests_per_minute", 100)
            req_per_hour = limits.get("requests_per_hour", 1000)
            composite_key = f"{api_key}:{endpoint}:{ip}"
            window_minute = minute_request_mapping[composite_key]
            key_request_mappings[api_key].append(request)
            while window_minute and timestamp - window_minute[0] >= 60:
                window_minute.popleft()
            window_minute.append(timestamp) 
            window_hour = hour_mapping[composite_key]
            
            while window_hour and timestamp - window_hour[0] >= 3600:
                window_hour.popleft()
            window_hour.append(timestamp)
                
            
            decision_key= f"{api_key}:{endpoint}:{ip}:{timestamp}:{i}"
            decision ="ALLOW"
            if len(window_minute) > limits["requests_per_minute"]:
                decision ="DENY"
            elif len(window_hour) > limits["requests_per_hour"]:
                decision ="DENY"
            else:
                decision ="ALLOW"        
            remaining_minute = max(0, req_per_min - len(window_minute))
            remaining_hour = max(0, req_per_hour - len(window_hour))
            decision_mapping[decision_key] = {
                "decision": decision,
                "X-RateLimit-Remaining-Minute": remaining_minute,
                "X-RateLimit-Remaining-Hour": remaining_hour
            }
        return {"decision_mapping": decision_mapping, "key_request_mappings":key_request_mappings}  

data= {
    "requests": [
        # These two are in the SAME minute and hour
        {
            "api_key": "sk_test_123",
            "endpoint": "/v1/charges",
            "timestamp": 1640995200,  # 2022-01-01 00:00:00 UTC
            "ip": "192.168.1.1"
        },
        {
            "api_key": "sk_test_123",
            "endpoint": "/v1/charges",
            "timestamp": 1640995205,  # 2022-01-01 00:00:05 UTC (same minute)
            "ip": "192.168.1.1"
        },
        # Next request is in a DIFFERENT minute but SAME hour
        {
            "api_key": "sk_test_123",
            "endpoint": "/v1/customers",
            "timestamp": 1640995265,  # 2022-01-01 00:01:05 UTC
            "ip": "192.168.1.2"
        },
        # Different hour entirely
        {
            "api_key": "sk_test_456",
            "endpoint": "/v1/charges",
            "timestamp": 1640998800,  # 2022-01-01 01:00:00 UTC
            "ip": "192.168.1.3"
        }
    ],
    "limits": {
        "sk_test_123": {
            "requests_per_minute": 2,
            "requests_per_hour": 3
        },
        "sk_test_456": {
            "requests_per_minute": 1,
            "requests_per_hour": 5
        }
    }
}        
rate_limiter = RateLimiter()
#print(rate_limiter.track_requests(data))
print(rate_limiter.track_requests_sliding_window(data))

