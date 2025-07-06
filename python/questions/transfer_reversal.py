from collections import defaultdict
from datetime import datetime

class TransferReversal:
    def parse_events(self, logs: str) -> dict:
        transfer_events = defaultdict(list)
        log_tokens = logs.split("|")
        account_id_transfer_mappings = defaultdict(set) 
        
        for log_token in log_tokens:
            timestamp, event_type, transfer_id, account_id, amount = log_token.split(";")
            transfer_events[transfer_id].append({
                "timestamp": timestamp,
                "event_type": event_type,
                "account_id": account_id,
                "amount": int(amount)
            })
            account_id_transfer_mappings[account_id].add(transfer_id)
        
        for transfer_id in transfer_events.keys():
            transfer_events[transfer_id] = sorted(transfer_events[transfer_id], key=lambda p: p["timestamp"])
            
        return transfer_events,account_id_transfer_mappings
    
    def get_transfer_status(self, logs: str) -> dict:
        transfer_events, account_id_transfer_mappings = self.parse_events(logs)
        
        transfer_id_status = {}
        for transfer_id in transfer_events:
            event_length = len(transfer_events[transfer_id])
            
            final_event = transfer_events[transfer_id][event_length-1]["event_type"]
            
            if final_event == "TRANSFER_PAID":
                transfer_id_status[transfer_id] = "PAID"
            elif final_event == "TRANSFER_FAILED":
                transfer_id_status[transfer_id] = "FAILED" 
            else:
                transfer_id_status[transfer_id] = "REVERSED"
        return transfer_id_status
   
    def get_final_balance(self, logs: str) -> dict:
        transfer_events, account_id_transfer_mappings = self.parse_events(logs)  
        balance_mapping = {}
        for account_id in account_id_transfer_mappings:
            balance = 0
            for transfer_id in account_id_transfer_mappings[account_id]:
                for event in transfer_events[transfer_id]:
                    amount = event["amount"]
                    event_type = event["event_type"]
                    if event_type == "TRANSFER_CREATED":
                        balance -= amount
                    elif event_type == "REVERSAL_CREATED":
                        balance += amount
            balance_mapping[account_id] = balance
        return balance_mapping
    
    def get_reversal_latency(self, logs: str) -> dict:
        transfer_events, account_id_transfer_mappings = self.parse_events(logs) 
        transfer_id_latency_mapping = {}
        for transaction_id in transfer_events.keys():
            creation_time_str = None
            reversal_time_str = None
            
            for event in transfer_events[transaction_id]:
                if event["event_type"] == "TRANSFER_CREATED":
                    creation_time_str = event["timestamp"]
                elif event["event_type"] == "REVERSAL_CREATED":
                    reversal_time_str = event["timestamp"]
            
            if creation_time_str and reversal_time_str:
                cretion_time = datetime.fromisoformat(creation_time_str.replace('Z', '+00:00'))
                reversal_time = datetime.fromisoformat(reversal_time_str.replace('Z', '+00:00'))
                
                latency_seconds = (reversal_time - cretion_time).total_seconds()  
                
                transfer_id_latency_mapping[transaction_id] = latency_seconds          
            
        return transfer_id_latency_mapping
    
    def get_risk_accounts(self, logs: str) -> list[str]:   
        transfer_events, account_id_transfer_mappings = self.parse_events(logs)
        risk_accounts = []
        
        for account_id in account_id_transfer_mappings:
            total_transfers = len(account_id_transfer_mappings[account_id])
            
            number_of_reversed = 0
            for transfer_id in account_id_transfer_mappings[account_id]:
                for event in transfer_events[transfer_id]:
                    event_type = event["event_type"]
                    if event_type == "REVERSAL_CREATED":
                        number_of_reversed += 1
            if ((number_of_reversed * 100) // total_transfers) > 20:
                risk_accounts.append(account_id)
                
                        
        return risk_accounts

if __name__ == "__main__":
    # --- Test Data ---
    # This log includes multiple accounts and transfer states to test all parts.
    transfer_log = (
        "2025-06-01T10:00:00Z;TRANSFER_CREATED;tr_1;acct_1;1000|"  # acct_1: Success
        "2025-06-02T10:00:00Z;TRANSFER_PAID;tr_1;acct_1;1000|"
        "2025-06-03T11:00:00Z;TRANSFER_CREATED;tr_2;acct_1;2000|"  # acct_1: Fail
        "2025-06-04T11:00:00Z;TRANSFER_FAILED;tr_2;acct_1;2000|"
        "2025-06-05T12:00:00Z;TRANSFER_CREATED;tr_5;acct_2;5000|"  # acct_2: Reversed
        "2025-06-05T12:00:30Z;REVERSAL_CREATED;tr_5;acct_2;5000|"
        "2025-06-06T13:00:00Z;TRANSFER_CREATED;tr_6;acct_2;6000|"  # acct_2: Success
        "2025-06-07T13:00:00Z;TRANSFER_PAID;tr_6;acct_2;6000|"
        "2025-06-08T14:00:00Z;TRANSFER_CREATED;tr_3;acct_1;3000|"  # acct_1: Success
        "2025-06-09T14:00:00Z;TRANSFER_PAID;tr_3;acct_1;3000|"
        "2025-06-10T15:00:00Z;TRANSFER_CREATED;tr_4;acct_1;4000|"  # acct_1: Success
        "2025-06-11T15:00:00Z;TRANSFER_PAID;tr_4;acct_1;4000"
    )

    # Instantiate your solution class
    tracker = TransferReversal() # Replace with your class name

    # --- Part 1 ---
    print("## Part 1: Final Transfer Status ##")
    # Expected: A map like {'tr_1': 'PAID', 'tr_2': 'FAILED', 'tr_5': 'REVERSED', ...}
    print(tracker.get_transfer_status(transfer_log))
    print("-" * 50)


    # --- Part 2 ---
    print("## Part 2: Balance Impact ##")
    # Expected: {'acct_1': -10000, 'acct_2': -6000}
    print(tracker.get_final_balance(transfer_log))
    print("-" * 50)


    # --- Part 3 ---
    print("## Part 3: Reversal Latency ##")
    # Expected: A map for reversed transfers. {'tr_5': 30.0} (latency in seconds)
    print(tracker.get_reversal_latency(transfer_log))
    print("-" * 50)


    # --- Part 4 ---
    print("## Part 4: Account Risk Report ##")
    # Expected: A list containing 'acct_2' (1 of 2 transfers reversed = 50% > 20%)
    # ['acct_2']
    print(tracker.get_risk_accounts(transfer_log))
    print("-" * 50)          
        
                                  
                     
        
                