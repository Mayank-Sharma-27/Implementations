from collections import defaultdict

class SubscriptionTier:
    def parse_events(self, usage_log: str, tier_boundries: str) -> dict:
        events = []
        
        usage_log_tokens = usage_log.split("&")
        tier_map = {}
        
        tier_boundries_token = tier_boundries.split(",")
        tiers = []
        for t in tier_boundries_token:
            key, value = t.split(":")
            tiers.append(int(value))
        
        for usage_log_token in usage_log_tokens:
            date, customer_id, usage = usage_log_token.split(";")
            month = date.split("-")[1]
            events.append({
                "date": date,
                "customer_id": customer_id,
                "month": month,
                "usage": usage
            })
        events = sorted(events, key=lambda e : e["date"])
        custmer_subs = defaultdict(dict)
        
        for event in events:
            customer_id = event["customer_id"] 
            month = event["month"]
            usage = int(event["usage"])
            if custmer_subs[customer_id].get(month) is None:
               custmer_subs[customer_id][month] = {}
               custmer_subs[customer_id][month]["usage_amount"] = 0
               custmer_subs[customer_id][month]["subscription_tier"] = "Bronze"
               custmer_subs[customer_id][month]["project_tier"] = ""
            
            usage_amount = custmer_subs[customer_id][month]["usage_amount"] + usage
                
            # Assuming tiers = [0, 1000, 5000]
            if usage_amount >= tiers[2]:  # 5000+
                custmer_subs[customer_id][month]["subscription_tier"] = "Gold"
            elif usage_amount >= tiers[1]: # 1000-4999
                custmer_subs[customer_id][month]["subscription_tier"] = "Silver"
            else: # 0-999
                custmer_subs[customer_id][month]["subscription_tier"] = "Bronze"    
        
        return custmer_subs
    
    def get_total_usage(self, usage_log: str, tier_boundries: str, month: str) -> dict:
        custmer_subs = self.parse_events(usage_log, tier_boundries)
        customer_usage_for_month = defaultdict(dict)
        #print(custmer_subs)
        for customer_id in custmer_subs.keys():
            if custmer_subs[customer_id][month]:
               if customer_usage_for_month[customer_id].get(month) is None:
                  customer_usage_for_month[customer_id][month] = {}   
               customer_usage_for_month[customer_id][month] = custmer_subs[customer_id][month]["usage_amount"]
        
        return customer_usage_for_month
    
    def get_tier_assesmment(self, usage_log: str, tier_boundries: str, month: str) -> dict:      
        custmer_subs = self.parse_events(usage_log, tier_boundries)
        customer_tier_for_month = defaultdict(dict)
        
        for customer_id in custmer_subs.keys():
            if custmer_subs[customer_id].get(month) is not None:
                if customer_tier_for_month[customer_id].get(month) is None:
                  customer_tier_for_month[customer_id][month] = {}  
                customer_tier_for_month[customer_id][month] = custmer_subs[customer_id][month]["subscription_tier"]
        
        return customer_tier_for_month
    
    def get_tier_assesmment_notificaiton(self, usage_log: str, tier_boundries: str, month: str, pre_month: str) ->dict:       
        customer_tier_for_month = self.get_tier_assesmment(usage_log, tier_boundries, month)
        customer_tier_for_pre_month = self.get_tier_assesmment(usage_log, tier_boundries, pre_month)
        notification = {}
        for key in customer_tier_for_month.keys():
            if customer_tier_for_pre_month[key].get(pre_month) is None:
               notification[key] = {"old_tier": None, "new_tier": customer_tier_for_month[key][month] , "change": "NEW"} 
               continue
            if customer_tier_for_month[key][month] != customer_tier_for_pre_month[key][pre_month]:
               notification[key] = {"old_tier": customer_tier_for_pre_month[key][pre_month], "new_tier": customer_tier_for_month[key][month] }
                
        return notification    
    
    def get_projections(self, usage_log: str, tier_boundries: str) -> dict:
        custmer_subs = self.parse_events(usage_log, tier_boundries)
        return custmer_subs   
    
if __name__ == "__main__":
    # --- Test Data ---
    tier_boundaries = "Bronze:0,Silver:1000,Gold:5000"
    
    # This log contains data for two months (January and February 2025)
    # to test the tier change logic.
    usage_log = (
        # -- January Data --
        "2025-01-10;cust_A;500&"
        "2025-01-15;cust_B;200&"
        "2025-01-20;cust_A;300&"  # cust_A Jan total: 800 (Bronze)
        # -- February Data --
        "2025-02-05;cust_A;400&"
        "2025-02-10;cust_B;300&"
        "2025-02-18;cust_A;800&"  # cust_A Feb total: 1200 (Silver)
        "2025-02-20;cust_C;5500"   # cust_C Feb total: 5500 (Gold)
    )

    # Instantiate your solution class
    service = SubscriptionTier() # Replace with your class name

    # --- Part 1 ---
    print("## Part 1: Total Monthly Usage (for 2025-02) ##")
    # Expected: {'cust_A': 1200, 'cust_B': 300, 'cust_C': 5500}
    print(service.get_total_usage(usage_log, tier_boundaries,"02"))
    print("-" * 50)


    # --- Part 2 ---
    print("## Part 2: Tier Assignment (for 2025-02) ##")
    # Expected: {'cust_A': 'Silver', 'cust_B': 'Bronze', 'cust_C': 'Gold'}
    print(service.get_tier_assesmment(usage_log, tier_boundaries, "02"))
    print("-" * 50)


    # --- Part 3 ---
    print("## Part 3: Tier Change Notifications (Feb vs Jan) ##")
    # Expected: A map showing changes. cust_A went from Bronze to Silver.
    # {'cust_A': {'old_tier': 'Bronze', 'new_tier': 'Silver', 'change': 'UPGRADE'}, 'cust_C': {'old_tier': None, 'new_tier': 'Gold', 'change': 'NEW'}}
    print(service.get_tier_assesmment_notificaiton(usage_log, tier_boundaries, "02", "01"))
    print("-" * 50)


    # --- Part 4 ---
    print("## Part 4: Projected Tier Calculation (as of 2025-02-15) ##")
    # Expected: A report comparing actual tier (based on full month data) to projected tier.
    # For cust_A: usage is 400 so far. Projection: (400/15)*30=800 -> Bronze.
    # {
    #   'cust_A': {'current_tier': 'Silver', 'projected_tier': 'Bronze'},
    #   'cust_B': {'current_tier': 'Bronze', 'projected_tier': 'Bronze'},
    #   'cust_C': {'current_tier': 'Gold', 'projected_tier': 'Bronze'}
    # }
    print(service.get_projections(usage_log, tier_boundaries))
    print("-" * 50)    
                 
        
                              
            
            
            
               
                   