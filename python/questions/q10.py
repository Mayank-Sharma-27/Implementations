""" 
Part 1: Parse a string in the format "USD:CAD:DHL:5,USD:GBP:FEDX:10", representing currency conversion rates from a source to a target currency and the associated shipping method. Write a method to convert a given amount from one currency to another. Only direct conversions are allowed.

Part 2: Write a method that returns the cost and shipping methods involved, allowing at most one hop in the conversion from one currency to another.

Part 3: Write a method that returns the minimum cost and involved shipping methods, allowing at most one hop for the conversion.

During the phone screen, I successfully solved the first three parts and ran test cases for each. Unfortunately, I ran out of time before I could get to the fourth part. I coded in C++, though I’d recommend using a language like Python to simplify input parsing. """

from collections import defaultdict

class Conversion:
    
    def get_currency_conversion_graph(self, conversion_string: str) -> dict:
       if not conversion_string:
           return ValueError("Invalid Input")
       conversion_string_tokens = conversion_string.split(",")
       graph = defaultdict(lambda: defaultdict(list))
       for token in conversion_string_tokens:
           source, destination, carrier, amount = token.split(":")
           graph[source][destination].append({
               "amount": int(amount),
               "carrier": carrier
           })
        
       return graph
    
    def convert(self, conversion_string: str , source: str, destination: str, amount:int) -> list:
        graph = self.get_currency_conversion_graph(conversion_string)
        
        if source not in graph:
            return ValueError("Invalid Valu")
        
        destination_map = graph[source]
        ans = []
        for conversion in destination_map[destination]:
            conversion_amount = int(conversion["amount"])
            amount_final = conversion_amount * amount
            ans.append(
                {
                    "carrier": conversion["carrier"],
                    "amount_final": amount_final
                }
            )
        return ans
    
    def convert_with_one_hop(self, conversion_string: str , source: str, destination: str, amount:int)  -> list:
        graph = self.get_currency_conversion_graph(conversion_string) 
        if source not in graph:
            return ValueError("Invalid Valu")
        
        destination_map = graph[source] 
        direct_conversion = self.convert(conversion_string, source, destination, amount)
        if direct_conversion:
            return direct_conversion
        ans = []
        ans.extend(direct_conversion)
        for mid in graph[source]:
            if destination in graph[mid]:
                for route1 in graph[source][mid]:
                    for route2 in graph[mid][destination]:
                        total_cost = amount * (route1["amount"] + route2["amount"])
                        ans.append({
                            "from": source,
                            "to": destination,
                            "via": mid,
                            "carriers": [route1["carrier"], route2["carrier"]],
                            "rates": [route1["amount"], route2["amount"]],
                            "total_cost": total_cost
                            
                        })
        return ans 
    
    def minimum_cost_coversion(self, log: str, source: str, target: str) -> dict:
        all_routes = self.convert_with_one_hop(log, source, target, 1.0)
        if not all_routes:
            return {}
        return min(all_routes, key = lambda x:x["total_cost"])         
                   
    
if __name__ == "__main__":
    conversion = Conversion()
     
    conversion_string = "USD:CAD:DHL:2,USD:GBP:FEDX:4,CAD:INR:UPS:3,GBP:INR:DHL:1"
     
     
    print(conversion.convert(conversion_string,"USD", "CAD", 10))
    print(conversion.convert_with_one_hop(conversion_string, "USD","INR", 10))
    print(conversion.minimum_cost_coversion(conversion_string, "USD","INR"))
     
        
        
            
        