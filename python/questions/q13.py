from collections import defaultdict
from datetime import datetime

class TransferReversal:
    
    def parse_events(self, log: str) -> dict:
        log_tokens = log.split("|")
        
        transfers = defaultdict(list)
        accounts_transfers_mapping = defaultdict(list)
        
        for log_token in log_tokens:
            timestamp ,event_type, transfer_id, account_id, amount = log_token.split(";")
            transfers[transfer_id].append({
                "event_type": event_type,
                "account_id": account_id,
                "amount" : int(amount),
                "timestamp": timestamp
            })
            transfers_in_account = accounts_transfers_mapping.get(account_id, [])
            if transfer_id not in transfers_in_account:
               transfers_in_account.append(transfer_id)
               accounts_transfers_mapping[account_id] = transfers_in_account
            
        for id in transfers.keys():
                transfers[id] = sorted(transfers[id], key=lambda p:p["timestamp"])
                
        return {"transfers": transfers, "accounts_transfers_mapping": accounts_transfers_mapping}
        
    def get_transfer_status(self, log: str) -> dict:
        events = self.parse_events(log)
        transfers = events["transfers"]
        ans = {}
        for id, transfer in transfers.items():
            length = len(transfer)
            ans[id] = transfer[length - 1]["event_type"]
        return ans
    
    def get_final_balance(self, log: str) -> dict:
        events = self.parse_events(log)
        transfers_mapping = events["transfers"]
        #print(transfers_mapping)
        accounts_transfers_mapping =  events["accounts_transfers_mapping"]
        transfer_final_status = self.get_transfer_status(log)
        ans = {}
        for account_id in accounts_transfers_mapping:
            balance = 0
            for transfer_id in accounts_transfers_mapping[account_id]:
                for event in transfers_mapping[transfer_id]:
                    amount = int(event["amount"])
                    event_type = event["event_type"]
                    if event_type == "TRANSFER_CREATED":
                        balance -= amount
                    elif event_type == "REVERSAL_CREATED":
                        balance += amount
            ans[account_id] = balance
        return ans      
                
    def get_reversal_latency(self, logs: str) -> dict:
        events = self.parse_events(logs)
        transfers = events["transfers"]
        transfer_id_reversal_mapping = {}
        for transfer_id, transfer in transfers.items():
            creation_time = None
            reversal_time = None
            
            for event in transfers[transfer_id]:
                if event["event_type"] == "TRANSFER_CREATED":
                   creation_time = event["timestamp"]
                if event["event_type"] == "REVERSAL_CREATED":
                   reversal_time = event["timestamp"]
            
            if creation_time and reversal_time:
                cretion_time = datetime.fromisoformat(creation_time.replace('Z', '+00:00'))
                reversal_time = datetime.fromisoformat(reversal_time.replace('Z', '+00:00'))
                
                latency_seconds = (reversal_time - cretion_time).total_seconds()  
                
                transfer_id_reversal_mapping[transfer_id] = latency_seconds
        return transfer_id_reversal_mapping
    
    def get_risk_accounts(self, logs: str) -> list[str]:   
        events = self.parse_events(logs)
        transfers = events["transfers"]
        accounts_transfers_mapping =  events["accounts_transfers_mapping"]
        risk_accounts = []
        
        for account_id in accounts_transfers_mapping:
            total_transfers = len(accounts_transfers_mapping[account_id])
            
            number_of_reversed = 0
            for transfer_id in accounts_transfers_mapping[account_id]:
                for event in transfers[transfer_id]:
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
        
                                  
                     
        
                