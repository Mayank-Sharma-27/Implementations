# -----------------------------------
# 📝 Question: Digital Contract Action Tracker
#
# You are building a system to track user activity on digital contracts. 
# Each log entry captures when a user has viewed, signed, or forwarded a contract.
# These logs arrive in a semi-structured string format.
# You are expected to process these logs and extract actionable insights.
#
# Each log is separated by a semicolon (`;`) and is of the form:
#   contract_id|user_id|action|timestamp
#
# Actions are one of: "VIEWED", "SIGNED", or "FORWARDED".
#
# ---------------------
# Part 1: create_user_dict(logs: str) -> dict
# Parse the input logs and return a dictionary mapping each contract_id
# to a list of action events (sorted by timestamp). Each event includes:
#   {
#     "user_id": str,
#     "action": str,
#     "time": str
#   }
#
# ---------------------
# Part 2: get_most_recent_actions(logs: str) -> str
# For each contract, print the last action performed with this format:
#   Contact {contract_id} last action {action} by {user_id} at {time}
#
# ---------------------
# Part 3: get_our_of_order_actions(logs: str) -> list[str]
# Return a list of contract_ids where the actions appear out-of-order.
# The valid order is: VIEWED → SIGNED → FORWARDED.
# A contract is considered "out-of-order" if actions appear earlier than expected.
#
# ---------------------
# Part 4: create_action_report(logs: str) -> str
# Generate a readable report for each contract showing all actions chronologically:
#   Contact {contract_id}
#   - {user_id} {action} at {timestamp}
#
# ---------------------
# Example Input:
# logs = (
#   "c123|u1|VIEWED|2024-10-01T09:00:00Z;"
#   "c123|u2|SIGNED|2024-10-01T09:15:00Z;"
#   "c124|u1|FORWARDED|2024-10-01T10:00:00Z;"
#   "c125|u3|SIGNED|2024-10-01T08:30:00Z;"
#   "c125|u3|VIEWED|2024-10-01T08:45:00Z"
# )
#
# ---------------------
# Expected Output (for parts):
# - Part 1: {'c123': [...], 'c124': [...], 'c125': [...]}
# - Part 2: Contact c123 last action SIGNED by u2 at ...
# - Part 3: ['c125']
# - Part 4: Full contract action listing grouped and sorted
# -----------------------------------

from collections import defaultdict
class DigitalContact:
    def create_user_dict(self, logs: str) -> dict:
        logs_tokens = logs.split(";")
        user_logs = defaultdict(list)
        
        for log_token in logs_tokens:
            log = log_token.split("|")
            contract_id = log[0].strip()
            user_id = log[1].strip()
            action = log[2].strip()
            time = log[3].strip()
            user_logs[contract_id].append({
                "user_id" : user_id,
                "action": action,
                "time": time
            })
        for user_log in user_logs.keys():
            user_logs[user_log] = sorted(user_logs[user_log], key=lambda p : p["time"])
        
        return user_logs
    
    def get_most_recent_actions(self, logs: str) -> str:
        user_logs = self.create_user_dict(logs)
        lines = []
        
        for user_log in user_logs.keys():
            events = user_logs[user_log]
            if events:
                event = events[-1]
                user_id = event["user_id"]
                action = event["action"]
                time = event["time"]
                lines.append(f"Contact {user_log} last action {action} by {user_id} at {time}")
            
            lines.append("")
        return "\n".join(lines)
    
    def get_our_of_order_actions(self, logs: str) -> list[str]:
        user_logs = self.create_user_dict(logs)
        valid_actions = ["VIEWED", "SIGNED", "FORWARDED"]
        action_index = {action: idx for idx, action in enumerate(valid_actions)}  
        ans = []
        for user_log in user_logs.keys():
            events = user_logs[user_log] 
            prev_index = -1
            for event in events:
                action = event["action"]
                current_index = action_index.get(action, -1)
                if current_index < prev_index:
                    ans.append(user_log)
                    break
                prev_index = max(prev_index, current_index)
        return ans
    
    def create_action_report(self, logs: str) -> str:
        user_logs = self.create_user_dict(logs)     
        lines = []
        
        for contract ,events in user_logs.items():
            lines.append(f"Contact {contract}")
            for event in events:
                action = event["action"]
                user_id = event["user_id"]
                time = event["time"]
                lines.append(f"- {user_id} {action} at {time}") 
            lines.append("")
        return "\n".join(lines)                    
            
    
if __name__ == "__main__":
    digitalContact = DigitalContact()
    log = (
    "c123|u1|VIEWED|2024-10-01T09:00:00Z;"
    "c123|u2|SIGNED|2024-10-01T09:15:00Z;"
    "c124|u1|FORWARDED|2024-10-01T10:00:00Z;"
    "c125|u3|SIGNED|2024-10-01T08:30:00Z;"
    "c125|u3|VIEWED|2024-10-01T08:45:00Z"
)
    print(dict(digitalContact.create_user_dict(log)))    
    print("\n")
    print(digitalContact.get_most_recent_actions(log))  
    print("\n")
    print(digitalContact.get_our_of_order_actions(log))
    print("\n")
    print(digitalContact.create_action_report(log))      