""" 
Part 1: Parse a string in the format "USD:CAD:DHL:5,USD:GBP:FEDX:10", representing currency conversion rates from a source to a target currency and the associated shipping method. Write a method to convert a given amount from one currency to another. Only direct conversions are allowed.

Part 2: Write a method that returns the cost and shipping methods involved, allowing at most one hop in the conversion from one currency to another.

Part 3: Write a method that returns the minimum cost and involved shipping methods, allowing at most one hop for the conversion.

During the phone screen, I successfully solved the first three parts and ran test cases for each. Unfortunately, I ran out of time before I could get to the fourth part. I coded in C++, though I’d recommend using a language like Python to simplify input parsing. """


class Conversion:
    
    def parse_input(self, conversion_string: str) -> dict:
        currecy_tokens = conversion_string.split(",")
        conversion_dict = {}
        for currency_token in currecy_tokens:
            source = currency_token.split(":")[0].strip()
            target = currency_token.split(":")[1].strip()
            shipment = currency_token.split(":")[2].strip()
            cost = currency_token.split(":")[3].strip()
            key = f"{source}:{target}"
            conversion_dict[key] = (shipment, float(cost))
        
        return conversion_dict
    
    def convert(self, source: str, target: str, conversion_dict: dict, amount: str) -> float:
        key = f"{source}:{target}"
        amount = float(amount)
        ans = -1
        if key not in conversion_dict:
            return -1
        value = conversion_dict[key][1]
        ans = float(amount * value)
        return ans    
        
    def convert_with_one_hop(self, source: str, target: str, conversion_dict: dict, amount: str)  -> tuple[float, list[str]]:
        min_cost = 10000000
        ans = []
        for middle in self.get_all_currencies(conversion_dict): 
            key1 = f"{source}:{middle}"
            key2 = f"{middle}:{target}"
            if key1 in conversion_dict and key2 in conversion_dict:
                ship1, cost1 = conversion_dict[key1]
                ship2, cost2 = conversion_dict[key2]
                total_cost = (cost1+cost2)*amount
                
                if (min_cost > total_cost):
                    min_cost = total_cost
                    ans = (total_cost, [ship1, ship2])  
            return ans 
    
    def get_all_currencies(self, conversion_dict: dict):
        ans = set()
        for key in conversion_dict.keys():
            src, trg = key.split(":")
            ans.add(src)
            ans.add(trg)   
        return ans     
    
if __name__ == "__main__":
     conversion = Conversion()
     
     conversion_string = "USD:CAD:DHL:2,USD:GBP:FEDX:4,CAD:INR:UPS:3,GBP:INR:DHL:1"
     
     conversion_dict = conversion.parse_input(conversion_string)
     print(conversion.convert("USD", "CAD", conversion_dict, 10 ))
     print(conversion.convert_with_one_hop("USD","INR", conversion_dict, 10))
     
        
        
            
        