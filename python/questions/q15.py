"""
You are building a service for a SaaS company that automatically assigns users to subscription tiers ('Bronze', 'Silver', 'Gold') based on their monthly usage.

Input Format
A definition of tier boundaries, format: Bronze:0,Silver:1000,Gold:5000.
A log of daily usage events, separated by &. Format: date;customer_id;usage_amount.
The Task
Total Monthly Usage: For a given month, calculate the total usage_amount for each customer.
Tier Assignment: Determine the correct subscription tier for each customer for that month.
Tier Change Notifications: Compare the assigned tier for the current month to the previous month. Generate a notification for any customer whose tier has changed.
Projected Tier Calculation: Halfway through the current month, calculate each customer's projected total monthly usage (assume usage rate is constant) and determine their "projected tier".
Sample Input
tier_boundaries = "Bronze:0,Silver:1000,Gold:5000"
usage_log = "2025-01-10;cust_A;600&2025-01-12;cust_B;30&2025-01-15;cust_A;100"

"""

from collections import defaultdict

class SubscriptionTier:
    
    def parse_events(self, logs: str, tier_boundries: str) -> dict:
        logs_token = logs.split("&")
        customer_monthly_mapping = defaultdict(lambda:  defaultdict(list))
        tier_mapping = {}
        
        tier_boundries_tokens = {}
        
        for token in tier_boundries.split(","):
            value = token.split(":")[1]
            tier = token.split(":")[0]
            tier_boundries_tokens[value] = tier
        
        total_monthly_usage_mapping = defaultdict(lambda: defaultdict(lambda: {"total_usage": 0, "tier": "Bronze"}))
        for log_token in logs_token:
            date, customer_id, usage_amount = log_token.split(";")
            month = date.split("-")[1]
            usage_amount = int(usage_amount)
                    
            customer_monthly_mapping[customer_id][month].append({
                "usage_amount": int(usage_amount),
                "date": date
            })
            total_monthly_usage_mapping[customer_id][month]["total_usage"] += usage_amount
            monthly_amount_used = int(total_monthly_usage_mapping[customer_id][month]["total_usage"])
           
            for tier_value in tier_boundries_tokens.keys():
                if monthly_amount_used > int(tier_value):
                    tier = tier_boundries_tokens[tier_value]
            total_monthly_usage_mapping[customer_id][month]["tier"]= tier
        
        return {"customer_monthly_mapping": customer_monthly_mapping, "total_monthly_usage_mapping": total_monthly_usage_mapping}
    
    def get_total_usage(self, logs: str, tier_boundries: str, month: str) -> dict:
        events =  self.parse_events(logs, tier_boundries)
        total_monthly_usage_mapping = events["total_monthly_usage_mapping"]
        
        customer_usage_monthly = defaultdict(lambda: {})
        for customer_id in total_monthly_usage_mapping.keys():
            months = total_monthly_usage_mapping[customer_id].keys()
            for month in months:
                customer_usage_monthly[customer_id][month] = total_monthly_usage_mapping[customer_id][month]["total_usage"]
        
        return customer_usage_monthly
    
    def get_tier_assesmment(self, logs: str, tier_boundries: str, month: str) -> dict:
        events =  self.parse_events(logs, tier_boundries)
        total_monthly_usage_mapping = events["total_monthly_usage_mapping"]
        
        customer_tier_mapping = defaultdict(lambda: {})
        for customer_id in total_monthly_usage_mapping.keys():
            months = total_monthly_usage_mapping[customer_id].keys()
            for month in months:
                customer_tier_mapping[customer_id][month] = total_monthly_usage_mapping[customer_id][month]["tier"]
        
        return customer_tier_mapping
    
    def get_tier_assesmment_notificaiton(self, logs: str, tier_boundries: str, current_month: str, previous_month: str) -> dict:
        events =  self.parse_events(logs, tier_boundries)
        total_monthly_usage_mapping = events["total_monthly_usage_mapping"]
        notifications = defaultdict(list)
        for customer_id in total_monthly_usage_mapping.keys():
            if total_monthly_usage_mapping[customer_id].get(previous_month) is None:
               notifications[customer_id].append({
                   "old_tier": "None",
                   "current_tier": current_tier,
                   "change": "NEW"
               }) 
            else:    
                previous_month_info = total_monthly_usage_mapping[customer_id][previous_month]
                tier = previous_month_info["tier"]
                prev_total_usage = int(previous_month_info["total_usage"])
                current_month_info = total_monthly_usage_mapping[customer_id][current_month]
                current_total_usage = int(current_month_info["total_usage"])
                change = "UPGRADE"
                current_tier = current_month_info["tier"]
                if current_total_usage < prev_total_usage:
                    change = "DOWNGRADE"    
                if current_tier != tier:
                    notifications[customer_id].append({
                        "old_tier": tier,
                        "current_tier": current_tier,
                        "change": change
                    }) 
            
        return notifications 
                
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
                 
        
                              
            
            
            
               
                   