from collections import defaultdict

"""
Story: You are on the Stripe Global team, building a "Smart Payment Routing" service. When a customer in one country pays a merchant in another, the funds must be routed through various international payment networks. Your service's job is to find the most efficient path for the money to travel, minimizing processing fees. Different payment processors offer different routes between countries, each with an associated cost.

Input: You will be given a string representing all available payment routes. Each route is separated by a ~.

The format for each route is:
source_country_code:processor_name:destination_country_code:fee_in_basis_points

source_country_code and destination_country_code are 2-letter ISO codes (e.g., US, DE, JP).

processor_name is the name of the payment network (e.g., Swift, FedWire, StripeNet).

fee_in_basis_points: The cost of using this route. 100 basis points = 1%. The total fee for a path is the sum of the fees of each leg.

Part 1: Direct Route Availability
First, build a method that checks for a direct route between a source and a destination country. If a direct route exists, it should return the processor and the fee. If multiple direct routes exist, return the one with the lowest fee.

Your task is to implement a function that takes the routes string, a source country, and a destination country, and returns the processor and fee for the best direct route.

Part 2: One-Hop Routing Options
Now, expand your service to consider routes with at most one intermediate country (a "hop"). A payment can go from US -> GB -> JP, for example.

Your task is to implement a function that finds all possible paths (both direct and one-hop) from a source to a destination. It should return a data structure containing all valid paths, where each path details the sequence of processors used and the total calculated fee.

Part 3: Cheapest One-Hop Route
From the list of paths generated in Part 2, your service must now identify the single best route.

Your task is to implement a function that returns only the cheapest path (minimum total fee) among all direct and one-hop options. The output should detail the processor sequence and the minimum total fee.

"""

class PaymentRouting:
    
    def parse_events(self, logs: str) -> dict:
        logs_tokens = logs.split("~")
        routes = defaultdict(list)
        for log_token in logs_tokens:
            source_country_code, processor_name, destination_country_code, fee_in_basis_points = log_token.split(":")
            key = f"{source_country_code}:{destination_country_code}"
            routes[key].append({
               "processor_name": processor_name,
               "fee_in_basis_points": int(fee_in_basis_points)
            }) 
        
        for key in routes.keys():
            routes[key] = sorted(routes[key], key=lambda p: p["fee_in_basis_points"])
        
        ans = defaultdict(list)
        
        for key in routes.keys():
            processor_names = []
            total_cost = 0
            for route in routes[key]:
                processor_names.append(route["processor_name"])
                total_cost += int(route["fee_in_basis_points"])
            ans[key] = {"path": processor_names, "total_cost": total_cost}    
                
        results = {}
        results = {"routes" : routes, "routing_options" : ans}    
        return results
    
    def get_direct_route(self, logs: str, source: str, destination) -> int:
        results = self.parse_events(logs)
        key = f"{source}:{destination}"
        routes = results["routes"]
        
        if key in routes.keys():
            return routes[key][0]["processor_name"],routes[key][0]["fee_in_basis_points"]
    
    def get_routing_options(self, logs: str, source: str, destination) -> dict:
        results = self.parse_events(logs)
        valid_routes = defaultdict(list)
        key = f"{source}:{destination}"
        routes = results["routes"]
        lines = []
        routing_options = results["routing_options"]
        
        if key in routes.keys():
            total_cost = routing_options[key]["total_cost"]
            path = routing_options[key]["path"]
            lines.append(f"- Path: {path}  Fee : {total_cost}")
            valid_routes[key].append({
                "Path": path,
                "cost": total_cost
            })
        
        for route in self.get_all_currencies(routes):
            key1 = f"{source}:{route}"
            key2 = f"{route}:{destination}"
            
            if key1 in routes.keys() and key2 in routes.keys():
                path1 = routing_options[key1]["path"]
                cost1 = routing_options[key1]["total_cost"]
                path2 = routing_options[key2]["path"]
                cost2 = routing_options[key2]["total_cost"]
                key1 = key1.split(":")[0]
                key2 = key2.split(":")[1]
                valid_path_key = f"{key1}:{key2}"
                path = []
                for p in path1:
                    path.append(p)
                for p in path2:
                    path.append(p)    
                cost = int(cost1) + int(cost2)
                lines.append(f"- Path: {path}  Fee : {cost}")
                valid_routes[valid_path_key].append({
                "Path": path,
                "cost": cost
            })
                
        return  "\n".join(lines), valid_routes
    
    def get_cheapest_routing_options(self, logs: str, source: str, destination)   -> dict:
        lines, routing_options = self.get_routing_options(logs, source, destination) 
        key = f"{source}:{destination}"
        
        routing_options[key] =  sorted(routing_options[key], key=lambda p : p["cost"])
        
        return routing_options[key][0] 
                  
    
    def get_all_currencies(self, conversion_dict: dict):
        ans = set()
        for key in conversion_dict.keys():
            src, trg = key.split(":")
            ans.add(src)
            ans.add(trg)   
        return ans  
    
class SmartRouter:
    def _build_graph(self, data: str) -> dict:
        graph = defaultdict(list)
        for route_str in routes_data.strip().split("~"):
            src, processor, destination, fee = route_str.split(":")
            graph[src].append({
                "destination": destination,
                "processor": processor,
                "fee": int(fee)
                
            })          
        return graph
    
    def find_direct_route(self, source: str, destination: str, data: str) -> tuple:
        graph = self._build_graph(data)
        best_route = None
        for route in graph[source]:
            dest = route["destination"]
            if dest == destination:
                if best_route is None or best_route["fee"] > route["fee"]:
                    best_route = route
        
        if best_route:
            return (best_route["processor"], best_route["fee"])     
        
        return best_route
    
    def find_one_hop_options(self, routes_data: str, source: str, destination: str) -> list:
        graph = self._build_graph(routes_data)  
        paths = []
        
        for route in graph[source]:
            dest = route["destination"]
            if dest == destination:
               paths.append({
                   "path": [route["processor"]],
                   "total_fee": route["fee"]
               })  
        for route in graph["source"]:
            intermediate = route["destination"]
            for intermediate_route in graph[intermediate]:
                if intermediate_route["destination"] == destination:
                    paths.append({
                        "path": [route["processor"], intermediate_route["processor"]],
                        "total_fee": route["fee"] + intermediate_route["fee"]
                    })
        return paths            
                  
    def find_cheapest_one_hop_route(self, routes_data: str, source: str, destination: str) -> dict:
        """Solves Part 3 by reusing the logic from Part 2."""
        all_options = self.find_one_hop_options(routes_data, source, destination)
        if not all_options:
            return None
        
        return min(all_options, key=lambda x: x["total_fee"])            
                
            
if __name__ == "__main__":
    # A comprehensive set of routes designed to test all scenarios.
    routes_data = (
        "US:StripeNet:GB:15~"  # US -> GB (15)
        "GB:Swift:JP:25~"      # GB -> JP (25) -> One-hop US->JP is 40
        "US:FedWire:DE:20~"    # US -> DE (20)
        "DE:Swift:JP:30~"      # DE -> JP (30) -> One-hop US->JP is 50
        "US:Routely:JP:90~"    # A direct, but expensive, route US->JP
        "GB:LocalNet:DE:5~"    # GB -> DE (5)
        "CA:StripeNet:US:10"   # A route for the multi-hop test
    )

    # Instantiate your solution class
    router = PaymentRouting() # Replace with your class name

    # --- Part 1 ---
    print("## Part 1: Direct Route Availability ##")
    # Expected: ('Routely', 90)
    print(router.get_direct_route(routes_data, "US", "JP"))
    print("-" * 50)


    # --- Part 2 ---
    print("## Part 2: One-Hop Routing Options ##")
    # Expected: A list/dict containing these paths and their total fees:
    # - Path: ['Routely'], Fee: 90
    # - Path: ['StripeNet', 'Swift'], Fee: 40
    # - Path: ['FedWire', 'Swift'], Fee: 50
    print(router.get_routing_options(routes_data, "US", "JP")[0])
    print("-" * 50)


    # --- Part 3 ---
    print("## Part 3: Cheapest One-Hop Route ##")
    # Expected: A tuple/dict like (['StripeNet', 'Swift'], 40)
    print(router.get_cheapest_routing_options(routes_data, "US", "JP"))
    print("-" * 50)


    # --- Part 4 ---
    print("## Part 4: Cheapest Overall Route (Any Hops) ##")
    # This tests a path with more than one hop: CA -> US -> GB -> DE -> JP
    # Path: CA -> US (10) -> GB (15) -> DE (5) -> JP (30) = Total Fee 60
    # print(router.find_cheapest_overall_route(routes_data, "CA", "JP"))
    print("-" * 50)
            
        
