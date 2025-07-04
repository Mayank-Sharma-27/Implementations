from collections import defaultdict

class SubscriptionEngine:
    
    def parse_events(self, logs: str) -> dict: 
        customer_events = defaultdict(dict)
        event_logs = logs.split("&")
        
        monthly_events = defaultdict(list)
        for event_log in event_logs:
            #print(event_log.split(";"))
            timestamp, customer_id, event_type, plan_id = event_log.split(";")
            month = timestamp.split("-")[1].strip()
            if customer_events[customer_id].get(month) is None:
               customer_events[customer_id] = defaultdict(list)
            customer_events[customer_id][month].append({
                "timestamp": timestamp,
                "event_type": event_type,
                "plan_id": plan_id
            })
               
        for month in sorted(customer_events[customer_id].keys()):
            customer_events[customer_id][month] = sorted(customer_events[customer_id][month], key=lambda p : p["timestamp"])    
        
        return customer_events
    
    def find_last_status(self, logs: str) -> dict:
        customer_events = self.parse_events(logs)
        ans = {}
        for customer in customer_events.keys():
            monthly_events = customer_events[customer]
            last_month = list(monthly_events.keys())[-1]
            last_event = monthly_events[last_month][-1]["plan_id"]
            ans[customer]= last_event
        
        return ans 
    
    def get_monthly_bill_for_last_month(self, logs: str) -> str:
        customer_events = self.parse_events(logs)
        ans = {}
        plan_costs = {"basic": 1000, "pro":5000}
        for customer in customer_events.keys():
            monthly_events = customer_events[customer]
            last_month = list(monthly_events.keys())[-1]
            plan_id = monthly_events[last_month][-1]["plan_id"]
            ans[customer] = plan_costs[plan_id]
        return ans
    
    def get_monthly_bill_for_last_month_porated(self, logs: str) -> str:          
        customer_events = self.parse_events(logs)
        ans = {}
        plan_costs_per_day = {"basic": 1000, "pro":5000}
        for customer in customer_events.keys():
            monthly_events = customer_events[customer]
            last_month = list(monthly_events.keys())[-1]
            sorted_events = monthly_events[last_month]
            customer_total_cost = 0
            for i, current_event in enumerate(sorted_events):
                current_plan = current_event["plan_id"]
                start_day = int(current_event["timestamp"].split("-")[2].split("T")[0])
                monthly_cost = plan_costs_per_day[current_plan]
                end_day = 0
                if i + 1 < len(sorted_events):
                    # The segment ends the day the next event starts
                    next_event = sorted_events[i+1]
                    end_day = int(next_event["timestamp"].split('-')[2].split('T')[0])
                else:
                    # This is the last segment, so it runs to the end of the 30-day month.
                    # We use 31 as the "end" to correctly calculate a 30-day period.
                    end_day = 31
                duration = end_day - start_day
                if duration > 0:
                    # 4. Use integer math to calculate the segment cost and add it to the total
                    segment_cost = (monthly_cost * duration) // 30
                    customer_total_cost += segment_cost    
                    
            ans[customer] = customer_total_cost           
                        
                
        return ans
    
if __name__ == "__main__" :

    event_log = "2025-01-01T00:00:00Z;cust_A;SUBSCRIBE;basic&2025-01-15T00:00:00Z;cust_A;UPGRADE;pro&2025-01-01T00:00:00Z;cust_B;SUBSCRIBE;pro"
    plan_costs_str = "basic:1000,pro:5000"

    # Instantiate your solution class
    calculator = SubscriptionEngine() # Replace with your class name

    # --- Part 1 ---
    print("## Part 1: Final Subscription Status ##")
    # Expected: {'cust_A': 'pro', 'cust_B': 'pro'}
    print(calculator.find_last_status(event_log))
    print("-" * 50)


    # --- Part 2 ---
    print("## Part 2: Simple Monthly Cost ##")
    # Expected: {'cust_A': 5000, 'cust_B': 5000}
    print(calculator.get_monthly_bill_for_last_month(event_log))
    print("-" * 50)


    # --- Part 3 ---
    print("## Part 3: Proration Calculation ##")
    # Expected: {'cust_A': 3132, 'cust_B': 5000} (Using integer math for daily rates)
    print(calculator.get_monthly_bill_for_last_month_porated(event_log))
    print("-" * 50)


    # --- Part 4 ---
    print("## Part 4: Final Invoice Generation ##")
    # Expected: A formatted summary object for each customer. For cust_A:
    # {
    #   'customer_id': 'cust_A',
    #   'line_items': [
    #     {'description': 'Charge for basic plan (14 days)', 'amount': 466},
    #     {'description': 'Charge for pro plan (16 days)', 'amount': 2666}
    #   ],
    #   'total': 3132
    # }
    # print(calculator.generate_invoices(event_log, plan_costs_str))
    print("-" * 50)
    
        
        
        
              
                   