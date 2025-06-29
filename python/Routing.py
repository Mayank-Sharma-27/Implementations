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
class Routing:
                      
    def _get_endpoint(self, log: str) -> str:
        
        return log[0].split("=")[1]
    
    def _get_versions(self, log: str) -> tuple:
        versions = {}
        versions_tokens = log.split("=")
        default_version = ""
        versions_information = versions_tokens[1][1: len(versions_tokens[1])]
        for version_information in versions_information.split(","):
            version = version_information.split(":")[0]
 
            version_value = version_information.split(":")[1]
            if "*" in version:
               default_version = version_value
            versions[version] = version_value
        return versions, default_version
    
    def get_mapping(self, log: str) -> dict:
        routing_info = defaultdict(defaultdict)
        log_tokens = log.split("\n")
        mapping = {}
        routing_info = defaultdict(defaultdict)
        for log_token in log_tokens:
            entry = log_token.split("::")
            
            if entry[0].strip() == "REQ":
                request = entry[1].strip()
                api = entry[2].strip()
                api_version = entry[3].split("=")[1].strip()
                if api in routing_info and api_version in routing_info[api]:
                    mapping[request] = routing_info.get(api).get(api_version)
            elif entry[0].strip() == "ROUTE":
                entry_tokens = entry[1].split(";")
                endpoint = self._get_endpoint(entry_tokens)
                versions, default = self._get_versions(entry_tokens[1])
                routing_info[endpoint] = {}
                routing_info[endpoint] = versions
                        
        return mapping
    
    def get_service_tally(self, log: str)  -> dict:
        routing_info = defaultdict(defaultdict)
        
        ans = defaultdict(int)
        log_tokens = log.split("\n")
        for log_token in log_tokens:
            entry = log_token.split("::")
            if entry[0].strip() == "REQ":
                request = entry[1]
                api = entry[2]
                api_version = entry[3].split("=")[1].strip()
                if api in routing_info and api_version in routing_info[api]:
                    ans[routing_info.get(api).get(api_version)] += 1
            elif entry[0].strip() == "ROUTE":
                entry_tokens = entry[1].split(";")
                endpoint = self._get_endpoint(entry_tokens)
                versions, default = self._get_versions(entry_tokens[1])
                routing_info[endpoint] = {}
                routing_info[endpoint] = versions        
        return ans
    
    def get_service_tally_with_default(self, log: str)  -> dict:
        routing_info = defaultdict(defaultdict)
        default = ""
        ans = defaultdict(int)
        log_tokens = log.split("\n")
        for log_token in log_tokens:
            entry = log_token.split("::")
            if entry[0].strip() == "REQ":
                request = entry[1]
                api = entry[2]
                api_version = entry[3].split("=")[1].strip()
                if api in routing_info and api_version in routing_info[api]:
                    ans[routing_info.get(api).get(api_version)] += 1
                else:
                    ans[default] += 1    
            elif entry[0].strip() == "ROUTE":
                entry_tokens = entry[1].split(";")
                endpoint = self._get_endpoint(entry_tokens)
                versions, default = self._get_versions(entry_tokens[1])
                routing_info[endpoint] = {}
                routing_info[endpoint] = versions        
        return ans
    
    def generate_historical_report(self, log: str, endpoint_to_report: str) -> str:
        history = defaultdict(set)
    
        for log_token in log.strip().split("\n"):
            if not log_token.strip().startswith("ROUTE"):
                continue
            
            _, route_data = log_token.split("::", 1)
            
            endpoint, version_part = route_data.split(";", 1)
            
            current_endpoint = endpoint.split("=", 1)[1]
            if current_endpoint != endpoint_to_report:
                    continue
            
            veresions_str = version_part.split("=", 1)[1].strip("[]")
            if not veresions_str:
                continue    
            
            for pair in veresions_str.split(","):
                version_id, service_name = pair.split(":", 1)
                history[service_name].add(version_id)

        report_lines = []
        header = f"Versioning Report for Endpoint: {endpoint_to_report}"
        report_lines.append(header)
        report_lines.append("=" * len(header))

        # Iterate through services sorted alphabetically
        for service_name in sorted(history.keys()):
            report_lines.append(f"\nService: {service_name}")
            
            # Iterate through versions for that service, sorted alphabetically
            for version_id in sorted(list(history[service_name])):
                report_lines.append(f"  - {version_id}")

        return "\n".join(report_lines)            
    
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

    print(routing.generate_historical_report(log, "/a"))

                    
                         
                