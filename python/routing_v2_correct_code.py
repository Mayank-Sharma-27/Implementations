from collections import defaultdict

class ApiRouterSolution:
    """
    A model solution for the API Endpoint Versioning and Traffic Routing problem.
    This class demonstrates modular design and robust parsing.
    """

    def _parse_log(self, log: str) -> list:
        """
        Parses the entire raw log string into a structured list of events.
        This is the core helper function that eliminates code duplication.
        """
        parsed_events = []
        for line in log.strip().split('\n'):
            if not line.strip():
                continue

            try:
                event_type, data = line.split("::", 1)
                if event_type == "ROUTE":
                    endpoint_part, versions_part = data.split(";", 1)
                    endpoint = endpoint_part.split("=", 1)[1]
                    versions_str = versions_part.split("=", 1)[1].strip("[]")
                    
                    versions_map = {}
                    default_service = None
                    if versions_str:
                        for pair in versions_str.split(','):
                            version_id, service_name = pair.split(':', 1)
                            if version_id.endswith('*'):
                                version_id = version_id.strip('*')
                                default_service = service_name
                            versions_map[version_id] = service_name
                    
                    parsed_events.append({
                        "type": "ROUTE",
                        "endpoint": endpoint,
                        "versions": versions_map,
                        "default": default_service
                    })

                elif event_type == "REQ":
                    req_id, endpoint, version_part = data.split("::", 2)
                    api_version = version_part.split("=", 1)[1]
                    parsed_events.append({
                        "type": "REQ",
                        "id": req_id,
                        "endpoint": endpoint,
                        "version": api_version
                    })
            except (ValueError, IndexError):
                # Safely skip any malformed lines
                continue
        
        return parsed_events

    def map_requests_to_services(self, log: str) -> dict:
        """Solves Part 1 of the problem."""
        events = self._parse_log(log)
        routing_table = {}
        request_mapping = {}
        
        for event in events:
            if event["type"] == "ROUTE":
                routing_table[event["endpoint"]] = event["versions"]
            elif event["type"] == "REQ":
                endpoint_routes = routing_table.get(event["endpoint"], {})
                service = endpoint_routes.get(event["version"])
                if service:
                    request_mapping[event["id"]] = service
        
        return request_mapping

    def tally_service_traffic(self, log: str) -> dict:
        """Solves Part 2 by reusing the logic from Part 1."""
        mapping = self.map_requests_to_services(log)
        tally = defaultdict(int)
        for service in mapping.values():
            tally[service] += 1
        return dict(tally)

    def tally_service_traffic_with_defaults(self, log: str) -> dict:
        """Solves Part 3 of the problem."""
        events = self._parse_log(log)
        routing_table = {}
        tally = defaultdict(int)

        for event in events:
            if event["type"] == "ROUTE":
                # The entire route config is stored, including versions and default
                routing_table[event["endpoint"]] = {
                    "versions": event["versions"],
                    "default": event["default"]
                }
            elif event["type"] == "REQ":
                route_config = routing_table.get(event["endpoint"])
                if not route_config:
                    continue # Unroutable

                service = None
                if event["version"]:
                    # Explicit version lookup
                    service = route_config["versions"].get(event["version"])
                else:
                    # Default version lookup
                    service = route_config["default"]
                
                if service:
                    tally[service] += 1
        
        return dict(tally)

    def generate_historical_report(self, log: str, endpoint_to_report: str) -> str:
        """Solves Part 4 of the problem."""
        events = self._parse_log(log)
        history = defaultdict(set)

        for event in events:
            if event["type"] == "ROUTE" and event["endpoint"] == endpoint_to_report:
                for version_id, service_name in event["versions"].items():
                    version_str = version_id
                    # Add back the '*' for the report if it was a default
                    if service_name == event["default"]:
                        version_str += "*"
                    history[service_name].add(version_str)
        
        if not history:
            return f"No versioning history found for Endpoint: {endpoint_to_report}"

        report_lines = []
        header = f"Versioning Report for Endpoint: {endpoint_to_report}"
        report_lines.append(header)
        report_lines.append("=" * len(header))

        for service_name in sorted(history.keys()):
            report_lines.append(f"\nService: {service_name}")
            for version_id in sorted(list(history[service_name])):
                report_lines.append(f"  - {version_id}")
        
        return "\n".join(report_lines)

if __name__ == '__main__':
    # --- Test Data ---
    log_part1_2 = """ROUTE::endpoint=/v1/charges;versions=[2022-11-15:charges-v2,2023-08-01:charges-v3]
REQ::req_a::/v1/charges::api_version=2022-11-15
REQ::req_b::/v1/charges::api_version=2023-08-01
REQ::req_c::/v1/customers::api_version=2022-11-15
ROUTE::endpoint=/v1/charges;versions=[2024-01-01:charges-v4-final]
REQ::req_d::/v1/charges::api_version=2023-08-01"""

    log_part3 = """ROUTE::endpoint=/v1/payouts;versions=[v1:payouts-legacy,v2*:payouts-stable]
REQ::req_p1::/v1/payouts::api_version=v1
REQ::req_p2::/v1/payouts::api_version=
ROUTE::endpoint=/v1/tokens;versions=[v3*:tokens-v3]
REQ::req_p3::/v1/payouts::api_version=v2
REQ::req_t1::/v1/tokens::api_version="""

    log_part4 = """ROUTE::endpoint=/a;versions=[v1:service_X,v2*:service_Y]
ROUTE::endpoint=/b;versions=[v1:service_Z]
ROUTE::endpoint=/a;versions=[v3:service_X,v4*:service_Y]
REQ::req_1::/a::api_version=v1
ROUTE::endpoint=/a;versions=[v5*:service_X]"""

    solver = ApiRouterSolution()

    print("--- Part 1: Request to Service Mapping ---")
    print(solver.map_requests_to_services(log_part1_2))
    print("\n" + "="*50 + "\n")

    print("--- Part 2: Service Traffic Tally ---")
    print(solver.tally_service_traffic(log_part1_2))
    print("\n" + "="*50 + "\n")

    print("--- Part 3: Service Traffic Tally with Defaults ---")
    print(solver.tally_service_traffic_with_defaults(log_part3))
    print("\n" + "="*50 + "\n")

    print("--- Part 4: Historical Route Analysis Report ---")
    print(solver.generate_historical_report(log_part4, "/a"))