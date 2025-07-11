"""
Stripe-Style Multi-Part Problem: API Endpoint Versioning and Traffic Routing

This problem simulates an API routing layer at Stripe. The goal is to process
a log containing route deployments and API requests to track which backend service
handles each request based on API versioning rules.

The log is a single string with entries separated by newlines.
- Route Deployment: ROUTE::endpoint={path};versions=[{v1:s1},{v2:s2},...]
- API Request:     REQ::{req_id}::{path}::api_version={version}

Key Rule: A new ROUTE deployment for an endpoint completely replaces any
previous route configuration for that same endpoint.

---

Part 1: Request to Service Mapping
- Process the log to map each request_id to the correct service_name.
- A request is unroutable if its version is not defined for the endpoint at
  the time of the request.

Part 2: Service Traffic Tally
- Count the total number of successful requests handled by each service.

Part 3: Default Version Routing
- Add support for default versions, marked with a '*' (e.g., v2*).
- Requests with a blank api_version should be routed to the default service.

Part 4: Historical Route Analysis Report
- For a specific endpoint, generate a formatted report detailing its entire
  versioning history, showing which services were mapped to which versions
  over time.
"""

from collections import defaultdict
import ast
class Routing:
    
    def _get_endpoint(self, endpoint_info: str) -> str:
        return endpoint_info.split("=")[1]
    
    def get_version_info(self, version_info: str):
        versions_tokens = version_info.split("=")
        version_information = versions_tokens[1][1: len(versions_tokens[1]) -1]
        
        mapping = {}
        default_endpoint = ""
        for version in version_information.split(","):
            key = version.split(":")[0]
            endpoint = version.split(":")[1]
            if "*" in key:
                key = key[:-1]
                default_endpoint = endpoint
                mapping[key]= endpoint
            else:
                mapping[key]= endpoint    
                
        return mapping, default_endpoint    
                     
    def parse_logs(self, log: str) -> dict:
        events = log.split("\n")
        api_requests_mapping = {}
        route_mapping = defaultdict(lambda: {"default_endpoint": ""})
        service_requests_count = defaultdict(int)
        route_history = defaultdict(list)
        deployment_counter = defaultdict(int)
        for event in events:
            if not event:
                continue
            request_type = event.split("::")[0]
            rest_of_body = event.split("::")[1]
            
            if request_type == "ROUTE":
               endpoint_info = rest_of_body.split(";")[0]
               version_info = rest_of_body.split(";")[1]
               endpoint = self._get_endpoint(endpoint_info)
               mapping, default_endpoint = self.get_version_info(version_info)
               route_mapping[endpoint] = mapping
               route_mapping[endpoint]["default_endpoint"] = default_endpoint
               deployment_counter[endpoint] += 1
               route_history[endpoint].append({
                "versions": mapping.copy(),
                "order": deployment_counter[endpoint]
            })

            elif request_type == "REQ":
                request_id = event.split("::")[1]
                endpoint = event.split("::")[2]
                version =  event.split("::")[3].split("=")[1]
                if endpoint in route_mapping and version in route_mapping[endpoint]:
                    api_requests_mapping[request_id] = route_mapping[endpoint][version]
                    service_requests_count[endpoint] += 1
                else:
                    default_endpoint = route_mapping[endpoint]["default_endpoint"]
                    api_requests_mapping[request_id] = default_endpoint  
                    
        return {
            "api_requests_mapping" : api_requests_mapping,
            "service_requests_count": service_requests_count,
            "route_history": route_history  
            
        }  
    def get_mapping(self, log: str) -> dict:
        result = self.parse_logs(log)
        return result["api_requests_mapping"] 
    
    def get_service_tally(self, log: str) -> dict:
        result = self.parse_logs(log)
        return result["service_requests_count"]
     
    def get_service_tally_with_default(self, defalut_log: str) -> dict:
        result = self.parse_logs(defalut_log)
        return result["api_requests_mapping"] 
    
    def get_routing_history(self, log: str, endpoint: str) -> dict:
        result = self.parse_logs(log)
         
        return result["route_history"].get(endpoint, {})               
               
                
    
if __name__ == "__main__":
    log = """ROUTE::endpoint=/v1/charges;versions=[2022-11-15:charges-v2,2023-08-01:charges-v3]
REQ::req_a::/v1/charges::api_version=2022-11-15
REQ::req_b::/v1/charges::api_version=2023-08-01
REQ::req_c::/v1/customers::api_version=2022-11-15
ROUTE::endpoint=/v1/charges;versions=[2024-01-01:charges-v4-final]
REQ::req_d::/v1/charges::api_version=2023-08-01
"""
    routing = Routing()
    print("--- Part 1: Service Traffic Tally (with Default Routing) ---")
    print(routing.get_mapping(log))
    print("--- Part 2: Service Traffic Tally ---")
    print(dict(routing.get_service_tally(log)))
    print("--- Part 3: Service Traffic Tally Default Version Routing---")
    
    defalut_log = """ROUTE::endpoint=/v1/payouts;versions=[v1:payouts-legacy,v2*:payouts-stable]
REQ::req_p1::/v1/payouts::api_version=v1
REQ::req_p2::/v1/payouts::api_version=
ROUTE::endpoint=/v1/tokens;versions=[v3*:tokens-v3]
REQ::req_p3::/v1/payouts::api_version=v2
REQ::req_t1::/v1/tokens::api_version="""    
    print(dict(routing.get_service_tally_with_default(defalut_log)))
    
    print("--- Part 4: Service Traffic Tally Default Version Routing---")
    
    log = """ROUTE::endpoint=/a;versions=[v1:service_X,v2*:service_Y]
ROUTE::endpoint=/b;versions=[v1:service_Z]
ROUTE::endpoint=/a;versions=[v3:service_X,v4*:service_Y]
REQ::req_1::/a::api_version=v1
ROUTE::endpoint=/a;versions=[v5*:service_X]
"""

    print(routing.get_routing_history(log, "/a"))

                    
                         
                