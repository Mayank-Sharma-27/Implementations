""" 
Part 1: Parse a string in the format "USD:CAD:DHL:5,USD:GBP:FEDX:10", representing currency conversion rates from a source to a target currency and the associated shipping method. Write a method to convert a given amount from one currency to another. Only direct conversions are allowed.

Part 2: Write a method that returns the cost and shipping methods involved, allowing at most one hop in the conversion from one currency to another.

Part 3: Write a method that returns the minimum cost and involved shipping methods, allowing at most one hop for the conversion.

During the phone screen, I successfully solved the first three parts and ran test cases for each. Unfortunately, I ran out of time before I could get to the fourth part. I coded in C++, though I’d recommend using a language like Python to simplify input parsing. """

from collections import defaultdict

class Conversion:
    
    def create_conversion_graph(self, log: str) -> dict :
        graph = defaultdict(lambda : defaultdict(list))
        
        log_tokens = log.split(",")
        for log_token in log_tokens:
            source, destination, carrier, amount = log_token.split(":")
            graph[source][destination].append({
                "carrier": carrier,
                "amount": int(amount)
            })
        
        return graph
    
    def convert(self, log: str ,source: str, destination: str, amount: int) -> int:
        graph = self.create_conversion_graph(log)
        
        if source not in graph or destination not in graph[source]:
            return []
        
        destination_map = graph[source]
        
        if destination not in destination_map:
            return ValueError("No destination present")
        
        results = []
        for route in destination_map[destination]:
            results.append({
                "from": source,
                "to": destination,
                "carrier": route["carrier"],
                "rate": route["amount"],
                "total_cost": amount * route["amount"]
            })
        return results
        
        ans = sorted(ans, key=lambda a:a["conversion_cost"])       
        return ans
    
    def convert_with_one_hop(self, log: str ,source: str, required_destination: str, amount: int) -> dict:
        graph = self.create_conversion_graph(log)
        results = []

        # Direct
        results.extend(self.convert(log, source, required_destination, amount))

        # One-hop
        for mid in graph[source]:
            if required_destination in graph[mid]:
                for route1 in graph[source][mid]:
                    for route2 in graph[mid][required_destination]:
                        total_cost = amount * (route1["amount"] + route2["amount"])
                        results.append({
                            "from": source,
                            "via": mid,
                            "to": required_destination,
                            "carriers": [route1["carrier"], route2["carrier"]],
                            "rates": [route1["amount"], route2["amount"]],
                            "total_cost": total_cost
                        })
        return results
    
    def minimum_cost_coversion(self, log: str, source: str, target: str) -> dict:
        all_routes = self.convert_with_one_hop(log, source, target, 1.0)
        if not all_routes:
            return {}
        return min(all_routes, key=lambda x: x["total_cost"])                 

           
       
if __name__ == "__main__":
     conversion = Conversion()
     
     conversion_string = "USD:CAD:DHL:2,USD:GBP:FEDX:4,CAD:INR:UPS:3,GBP:INR:DHL:1"
     
     
     print(conversion.convert(conversion_string,"USD", "CAD", 10))
     print(conversion.convert_with_one_hop(conversion_string, "USD","INR", 10))
     print(conversion.minimum_cost_coversion(conversion_string, "USD","INR"))
     
        
        
            
        