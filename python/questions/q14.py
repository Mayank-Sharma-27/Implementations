"""
Problem 13: Top-Up Balance and Threshold Alerts
Story
Some Stripe products require a user to maintain a "top-up" balance from which fees are deducted. You are building a monitoring service to send alerts when a balance drops below a threshold.

Input Format
A log of balance-affecting events, separated by |. Format: timestamp;account_id;type;amount.
type: TOP_UP (adds), FEE (subtracts).
An alert_threshold value.
The Task
Final Balances: Process all events and calculate the final balance for each account.
Balance History: For a specific account, return its entire balance history (timestamp and balance after each event).
Threshold Alert Generation: Identify every time an account's balance crosses the threshold from above to below. Return a list of all alerts.
"At Risk" Report: An account is "at risk" if it has dropped below the threshold more than twice. Generate a list of all "at risk" accounts.
Sample Input
balance_log = "2025-09-01T10:00:00Z;acct_A;TOP_UP;10000|2025-09-02T11:00:00Z;acct_A;FEE;3000|2025-09-03T12:00:00Z;acct_A;FEE;3000"
alert_threshold = 5000

"""

from collections import defaultdict

class BalanceReport:
    def parse_events(self, logs: str) -> dict:
        events = []
        log_tokens = logs.split("|")
        
        for log_token in log_tokens:
            timestamp, account_id, event_type, amount = log_token.split(";")
            events.append({
                "timestamp": timestamp,
                "account_id": account_id,
                "event_type": event_type,
                "amount": int(amount)
            })
        
        events = sorted(events, key=lambda p: p["timestamp"]) 
        #print(events)
        account_id_mapping = defaultdict(list)
        for event in events:
            timestamp = event["timestamp"]
            amount = int(event["amount"])
            event_type = event["event_type"]
            account_id = event["account_id"]
            account_id_mapping[account_id].append({
               "timestamp": timestamp,
               "amount": amount,
               "event_type": event_type 
            })
        
        return account_id_mapping
    
    def get_final_balance(self, logs: str) -> dict:
        account_id_mapping = self.parse_events(logs)
        #print(account_id_mapping)
        account_id_balance = defaultdict(int)
        for account_id in account_id_mapping.keys():
            infor = account_id_mapping[account_id]
            for info in infor:
                event_type = info["event_type"]
                amount = int(info["amount"])
                if event_type == "TOP_UP":
                    account_id_balance[account_id] += amount 
                else:
                    account_id_balance[account_id] -= amount        
        
        
        return account_id_balance
    
    def get_balance_history(self, logs: str, account_id: str) -> dict:
        account_id_mapping = self.parse_events(logs)
        account_id_balance = defaultdict(list)
        
        current_balance = 0
        for info in account_id_mapping[account_id]:
            event_type = info["event_type"]
            amount = int(info["amount"])
            timestamp = info["timestamp"]
            if event_type == "TOP_UP":
                current_balance += amount 
            else:
                current_balance -= amount
            account_id_balance[account_id].append({
                    "timestamp": timestamp,
                    "amount" : current_balance
                })
                            
        
        return account_id_balance
    
    def get_alerts(self, logs: str, alert_threshold: int) -> dict :
        
        account_id_mapping = self.parse_events(logs)
        alerts = defaultdict(list)
        prev_amount = None
        for account_id in account_id_mapping.keys(): 
            balance_history = self.get_balance_history(logs, account_id)
            for history in balance_history[account_id]:
                amount = history["amount"]
                if prev_amount is None:
                    prev_amount = amount
                
                if prev_amount >= alert_threshold:
                    if amount < alert_threshold:
                        alerts[account_id].append("Balance dropped")
                prev_amount = amount
        
        return alerts
    
    def get_alerts_when_at_risk(self, logs: str, alert_threshold: int) -> dict :
        alerts = self.get_alerts(logs, alert_threshold)
        
        prev_amount = None
        accounts_at_risk = []
        for alert in alerts.keys():
            number_of_alerts = len(alerts[alert])
            if number_of_alerts >=2:
               accounts_at_risk.append(alert) 
            
        return accounts_at_risk    
                   
            
if __name__ == "__main__":
    # --- Test Data ---
    # This log includes multiple accounts and threshold crossings to test all parts.
    balance_log = (
        "2025-09-01T10:00:00Z;acct_A;TOP_UP;10000|"  # A: 10000
        "2025-09-01T11:00:00Z;acct_B;TOP_UP;8000|"   # B: 8000
        "2025-09-01T12:00:00Z;acct_C;TOP_UP;6000|"   # C: 6000
        "2025-09-02T10:00:00Z;acct_A;FEE;3000|"      # A: 7000
        "2025-09-02T11:00:00Z;acct_B;FEE;4000|"      # B: 4000 (Alert #1)
        "2025-09-03T10:00:00Z;acct_A;FEE;3000|"      # A: 4000 (Alert #1)
        "2025-09-03T11:00:00Z;acct_C;FEE;500|"       # C: 5500
        "2025-09-04T10:00:00Z;acct_B;TOP_UP;8000|"   # B: 12000
        "2025-09-05T10:00:00Z;acct_B;FEE;7500|"      # B: 4500 (Alert #2)
        "2025-09-06T10:00:00Z;acct_B;TOP_UP;2000|"   # B: 6500
        "2025-09-07T10:00:00Z;acct_B;FEE;2000"       # B: 4500 (Alert #3)
    )
    alert_threshold = 5000

    # Instantiate your solution class
    monitor = BalanceReport() # Replace with your class name

    # --- Part 1 ---
    print("## Part 1: Final Balances ##")
    # Expected: {'acct_A': 4000, 'acct_B': 4500, 'acct_C': 5500}
    print(monitor.get_final_balance(balance_log))
    print("-" * 50)


    # --- Part 2 ---
    print("## Part 2: Balance History for acct_A ##")
    # Expected: A list of tuples like [('2025-09-01T10:00:00Z', 10000), ('2025-09-02T10:00:00Z', 7000), ('2025-09-03T10:00:00Z', 4000)]
    print(monitor.get_balance_history(balance_log, "acct_A"))
    print("-" * 50)


    # --- Part 3 ---
    print("## Part 3: Threshold Alert Generation ##")
    # Expected: A list of 4 alert objects, one for acct_A and three for acct_B.
    # For acct_B's first alert: {'account_id': 'acct_B', 'timestamp': '2025-09-02T11:00:00Z', 'balance': 4000}
    print(monitor.get_alerts(balance_log,  alert_threshold))
    print("-" * 50)


    # --- Part 4 ---
    print("## Part 4: 'At Risk' Report ##")
    # Expected: A list containing 'acct_B' since it dropped below the threshold more than twice. ['acct_B']
    print(monitor.get_alerts_when_at_risk(balance_log, alert_threshold))
    print("-" * 50)            