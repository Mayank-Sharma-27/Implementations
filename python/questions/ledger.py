"""
Stripe-Style Multi-Part Problem: The Unified Ledger Service

This problem simulates a unified ledger service that processes a raw stream of
transaction events. The goal is to maintain correct real-time balances for
merchant accounts and generate payout statements.

The input is a log of ledger events as a single string, with each event
separated by a `|`. The events are not guaranteed to be in chronological order
and must be processed by their `timestamp`.

The format for each event is:
`timestamp;transaction_id;account_id;type;amount;status;linked_id`

- type: CHARGE, REFUND, FEE, or PAYOUT
- status: SUCCEEDED, PENDING, or FAILED

---

Part 1: Final Account Balances
- Calculate the final balance for each account, considering only `SUCCEEDED`
  transactions.

Part 2: Available vs. Total Balance
- Calculate two balances for each account: `total_balance` (including SUCCEEDED
  and PENDING) and `available_balance` (only SUCCEEDED).

Part 3: Dynamic Payout Calculation
- A `PAYOUT` event is a trigger. The service must calculate the payout amount
  based on the account's available balance at that moment. The amount is only
  debited if the payout later succeeds.

Part 4: Generating a Payout Statement
- For a specific SUCCEEDED `payout_id`, generate a chronologically sorted list
  of all transaction IDs that were included in that payout. A transaction is
  included if it was SUCCEEDED and had not been part of a previous successful
  payout.
"""

from collections import defaultdict

class Ledger:
    
    def parse_events(self, logs: str) -> dict:
        log_tokens = logs.split("|")
        
        successful_account_transactions = defaultdict(list)
        pending_payout_transactions = defaultdict(int)
        pending_transactions = []
        account_balance =  defaultdict(lambda: {"available_balance":0, "total_balance": 0})
        events = []
        successful_account_transactions_to_amount = {}
        transaction_to_account_mappings = {}
        
        for log_token in log_tokens:
            timestamp,transaction_id,account_id,event_type,amount,status,linked_id = log_token.split(";")
            events.append({
                "timestamp": timestamp,
                "transaction_id": transaction_id,
                "account_id": account_id,
                "event_type": event_type,
                "amount" : int(amount),
                "status": status,
                "linked_id": linked_id
            })
            transaction_to_account_mappings[transaction_id] = account_id
        events = sorted(events, key=lambda p:p["timestamp"])
        
        for event in events:
            account_id = event["account_id"]
            event_type= event["event_type"]
            amount= event["amount"]
            status =  event["status"]
            linked_id = event["linked_id"]
            transaction_id = event["transaction_id"]
            if status == "PENDING":
                if event_type == "CHARGE":
                    account_balance[account_id]["total_balance"] += amount
                    pending_transactions.append(transaction_id)
                elif event_type == "REFUND":
                    account_balance[account_id]["total_balance"] += amount
                elif event_type == "FEE":
                    account_balance[account_id]["total_balance"] -= amount
                elif event_type == "PAYOUT":
                     pending_payout_transactions[transaction_id] = account_balance[account_id]["available_balance"]                     
            elif status == "SUCCEEDED":
                if event_type == "CHARGE":
                    if transaction_id not in pending_transactions:
                        account_balance[account_id]["total_balance"] += amount
                    else:
                        pending_transactions.remove(transaction_id)    
                    account_balance[account_id]["available_balance"] += amount
                    successful_account_transactions_to_amount[transaction_id] = amount
                elif event_type == "REFUND":
                    amount_to_refund = successful_account_transactions_to_amount[linked_id]
                    account_balance[account_id]["total_balance"] -= amount_to_refund
                    account_balance[account_id]["available_balance"] -= amount_to_refund
                elif event_type == "FEE":
                    account_balance[account_id]["total_balance"] -= amount
                    account_balance[account_id]["available_balance"] -= amount
                elif event_type == "PAYOUT":
                    if transaction_id in pending_payout_transactions:
                        amount_to_payout = pending_payout_transactions[transaction_id]
                        account_balance[account_id]["available_balance"] -= amount_to_payout
                        account_balance[account_id]["total_balance"] -= amount_to_payout
                        del pending_payout_transactions[transaction_id] 
                successful_account_transactions[account_id].append(transaction_id)        
            else:
                continue
            
        return  {
            "successful_account_transactions": successful_account_transactions,
            "account_balance": account_balance,
            "transaction_to_account_mappings": transaction_to_account_mappings
            
        }   
    
    def calculate_final_balances(self, log: str) -> dict:
        events = self.parse_events(log)
        account_balances = events["account_balance"]
        account_balance_mapping = defaultdict(int)
        for key, account_balance in account_balances.items():
            account_balance_mapping[key] = account_balance["available_balance"]
        return account_balance_mapping
    
    def get_all_balances(self, log: str) -> dict:
        events = self.parse_events(log)
        account_balances = events["account_balance"]
        return account_balances
    
    def generate_payout_statement(self, log: str, payout_id: str) -> dict:
        events = self.parse_events(log)
        transaction_to_account_mappings = events["transaction_to_account_mappings"]
        successful_account_transactions = events["successful_account_transactions"]
        successful_transactions_before_payout = []
        account_id = transaction_to_account_mappings[payout_id]
        for transaction in successful_account_transactions[account_id]:
            if transaction == payout_id:
                return successful_transactions_before_payout
            successful_transactions_before_payout.append(transaction)
            
        return successful_transactions_before_payout
                    

if __name__ == "__main__":
 
    log = (
        "2025-01-02T10:05:00Z;tx_A2;acct_A;FEE;50;SUCCEEDED;tx_A1|"          # 2. acct_A: Fee for charge
        "2025-01-02T10:00:00Z;tx_A1;acct_A;CHARGE;1000;SUCCEEDED;|"          # 1. acct_A: Initial charge
        "2025-01-03T11:00:00Z;po_B1;acct_B;PAYOUT;0;PENDING;|"               # 9. acct_B: Payout is triggered (Available: -20)
        "2025-01-02T10:15:00Z;tx_B2;acct_B;CHARGE;500;PENDING;|"             # 4. acct_B: A charge that will eventually fail
        "2025-01-02T10:10:00Z;tx_B1;acct_B;CHARGE;2000;SUCCEEDED;|"          # 3. acct_B: Initial charge
        "2025-01-03T14:00:00Z;tx_B2;acct_B;CHARGE;500;FAILED;|"              # 10. acct_B: The pending charge fails
        "2025-01-02T10:30:00Z;tx_A3;acct_A;CHARGE;300;PENDING;|"             # 5. acct_A: A charge that will eventually succeed
        "2025-01-04T10:00:00Z;po_B1;acct_B;PAYOUT;0;FAILED;|"                # 13. acct_B: The payout fails, so no money is moved
        "2025-01-03T10:00:00Z;tx_B3;acct_B;REFUND;2000;SUCCEEDED;tx_B1|"      # 7. acct_B: Refund for the initial charge
        "2025-01-02T10:45:00Z;po_A1;acct_A;PAYOUT;0;PENDING;|"               # 6. acct_A: Payout is triggered (Available: 1000-50=950)
        "2025-01-03T15:00:00Z;tx_A3;acct_A;CHARGE;300;SUCCEEDED;|"           # 11. acct_A: The pending charge succeeds
        "2025-01-03T10:01:00Z;tx_B4;acct_B;FEE;20;SUCCEEDED;tx_B3|"          # 8. acct_B: Fee for the refund
        "2025-01-05T10:00:00Z;tx_A4;acct_A;CHARGE;500;SUCCEEDED;|"           # 14. acct_A: A final charge after the payout
        "2025-01-03T16:00:00Z;po_A1;acct_A;PAYOUT;950;SUCCEEDED;"           # 12. acct_A: The payout succeeds for the calculated amount
    )
    
    print("--- Part 1 Results ---")
    ledger = Ledger()
    print(dict(ledger.calculate_final_balances(log)))  
    print("--- Part 2")
    print(dict(ledger.get_all_balances(log)))
    print("--- Part 3")
    print(ledger.generate_payout_statement(log, 'po_A1'))      