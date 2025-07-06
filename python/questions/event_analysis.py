"""
You are given a raw event log as a single string, where each event is
separated by a `|`. The events are not guaranteed to be in chronological order.
The format for each event is: `timestamp:user_id:subscription_id:plan_id:event_type`

Part 1: Identify all subscriptions that are currently 'active' (their most
        recent event by timestamp is not `CANCEL`).

Part 2: Calculate how many active subscriptions each user has.

Part 3: Find all subscriptions that have ever had an `UPGRADE` or `DOWNGRADE`
        event, regardless of their final status.

Part 4: Given a second input string with plan details (`plan_id:plan_name:price`),
        generate a formatted report listing each user's active subscriptions
        with their final plan name and price.
"""

from collections import defaultdict

class EventAnalyzer:
    
    def _create_dict(self, log: str) -> dict:
        subs_dict = defaultdict(list)
        
        logs_tokens = log.split("|")
        
        for log_token in logs_tokens:
            logs_information = log_token.split(":")
            date = "".join(logs_information[0:3]) 
            user_id = logs_information[3].strip()
            type = logs_information[5].strip()
            event_type = logs_information[6].strip()
            sub = logs_information[4].strip()
        
            subs_dict[user_id].append({
                "type": type,
                "event_type": event_type,
                "time": date,
                "sub": sub
            })  
        
        return subs_dict    
    
    def get_active_subscriptions(self, log: str) -> list[str]:
        subs_dict = self._create_dict(log)
        ans = set()
        active_sub_for_user = self._get_user_active_subs(subs_dict)
        
        for user in active_sub_for_user.keys():
            ans.update(active_sub_for_user[user])
        return sorted(list(ans))
    
    def get_user_active_subs(self, log: str) -> dict:
        subs_dict = self._create_dict(log)
        user_active_subs = defaultdict(int)
        active_sub_for_user = self._get_user_active_subs(subs_dict)
        for user in active_sub_for_user.keys():
            user_active_subs[user] = len(active_sub_for_user[user])
        return user_active_subs
    
    def _get_user_active_subs(self, subs_dict: dict) -> dict:
        user_active_subs = defaultdict(set)
        for user, plans in subs_dict.items():
            latest_events = {}
            for plan in plans:
                sub_id = plan["sub"]
                if sub_id not in latest_events or plan["time"] > latest_events[sub_id]["time"]:
                    latest_events[sub_id] = plan
            
            active_subs_for_user = set()
            for sub_id, latest_event in latest_events.items():
                if latest_event["event_type"] != "CANCEL":
                    active_subs_for_user.add(sub_id)        
                
            #print(active_subs)
            user_active_subs[user] = sorted(list(active_subs_for_user))
        return user_active_subs
    
    def get_plan_changes(self, log: str) -> list[str]:
        subs_dict = self._create_dict(log)
        ans = set()
        for user in subs_dict.keys():
            for plan in subs_dict[user]:
                if plan["event_type"] == "UPGRADE" or plan["event_type"]  == "DOWNGRADE":
                    ans.add(plan["sub"] )
        
        return sorted(list(ans))
    
    def get_report(self, log: str) -> str:
        lines = [f"User State Report"]
        subs_dict = self._create_dict(log)
        user_active_sub = self._get_user_active_subs(subs_dict)
        print(user_active_sub)
        for user in subs_dict.keys():
            lines.append(f"User: {user}")
            for plan in subs_dict[user]:
                sub = plan["sub"]
                type = plan["type"]
                active_subs = user_active_sub[user]
                print(f"{user} : {active_subs}")
                if user not in user_active_sub or sub not in active_subs:
                    continue
                
                lines.append(f"- {sub}:{type}") 
            lines.append("")  
        
        return "\n".join(lines)        
                             
                                                   
if __name__ == "__main__":
    event_log = "2025-01-05T09:00:00Z:u1:sub_1:pro:UPGRADE|2025-01-01T10:00:00Z:u1:sub_1:free:SUBSCRIBE|2025-01-07T10:00:00Z:u1:sub_3:pro:CANCEL|2025-01-02T11:00:00Z:u2:sub_2:pro:SUBSCRIBE|2025-01-06T14:00:00Z:u2:sub_2:free:DOWNGRADE|2025-01-03T12:00:00Z:u1:sub_3:pro:SUBSCRIBE"
    plan_data = "free:Basic Plan:0|pro:Professional Plan:1500|enterprise:Enterprise Plan:5000"

    # --- Create Analyzer ---
    analyzer = EventAnalyzer()
    
    # --- Execute and Print Each Part ---
    print("--- Part 1: Active Subscriptions ---")
    active_subs = analyzer.get_active_subscriptions(event_log)
    print(active_subs)
    print("\n" + "-"*40)

    print("--- Part 2: User Activity Summary ---")
    user_summary = analyzer.get_user_active_subs(event_log)
    print(user_summary)
    print("\n" + "-"*40)

    print("--- Part 3: Subscriptions with Plan Changes ---")
    plan_changes = analyzer.get_plan_changes(event_log)
    print(plan_changes)
    print("\n" + "-"*40)

    print("--- Part 4: Formatted User State Report ---")
    # Your get_report method must be updated to accept plan_data, like:
    # def get_report(self, log: str, plan_data: str) -> str:
    
        # This assumes your get_report method is updated
    report = analyzer.get_report(event_log)
    print(report)
                        