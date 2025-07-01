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
    
    def parse_events(self, log: str) -> dict :
        parsed_events = []
        for line in log.strip().split("|"):
            if not line.strip():
                continue
            
            timestamp, t_id, a_id, event, amount, status, linked_id = line.split(";")
            parsed_events.append({
                "timestamp": timestamp,
                "transaction_id": t_id,
                "account": a_id,
                "event": event,
                "amount": int(amount),
                "status": status,
                "linked_id": linked_id
            })
        return sorted(parsed_events, key=lambda p : p["timestamp"])
    
    def _get_final_ledger_state(self, log: str) -> dict:
        sorted_events = self.parse_events(log)
        
        balances = defaultdict(lambda : {"total_balance": 0, "available_balance" : 0})
        
        pending_payouts = {}
        cleared_transactions = defaultdict(set)
        payout_statements = defaultdict(list)
        
        for event in sorted_events:
            acct_id = event["account"]
            tx_id = event["transaction_id"]
            status = event["status"]
            tx_type = event["event"]
            amount = event["amount"]
            
            if tx_type == "PAYOUT":
                if status == "PENDING":
                    pending_payouts[tx_id] = balances[acct_id]["available_balance"]
                elif status == "SUCCEEDED":
                    payout_amount =  pending_payouts.get(tx_id, amount)
                    if payout_amount > 0:
                        balances[acct_id]["total_balance"] -= payout_amount
                        balances[acct_id]["available_balance"] -= payout_amount
                        statement_txs = []
                        for prev_event in sorted_events:
                            if prev_event["timestamp"] >= event["timestamp"]:
                                break
                            if (prev_event["account"] == acct_id and
                                prev_event["status"] == "SUCCEEDED" and
                                prev_event["event"] != "PAYOUT" and
                                prev_event["transaction_id"] not in cleared_transactions[acct_id]):
                                
                                statement_txs.append(prev_event["transaction_id"])
                                cleared_transactions[acct_id].add(prev_event["transaction_id"])
                        payout_statements[tx_id] = statement_txs
                continue#
            
            if status == "FAILED":
                continue
            
            effect = 1 if tx_type == "CHARGE" else -1
            
            if status == "SUCCEEDED":
                balances[acct_id]["total_balance"] += amount * effect
                balances[acct_id]["available_balance"] += amount * effect
            elif status == "PENDING":
                balances[acct_id]["total_balance"] += amount * effect

        return {"balances": balances, "statements": payout_statements}        
        
    def calculate_final_balances(self, log: str) -> dict:
        """Solves Part 1."""
        # This part can be solved by running the full ledger and extracting one piece of it.
        # In a real system, you might optimize this, but for the interview, it demonstrates cohesion.
        final_state = self._get_final_ledger_state(log)
        final_balances = {
            acct_id: data["available_balance"]
            for acct_id, data in final_state["balances"].items()
        }
        return final_balances

    def get_all_balances(self, log: str) -> dict:
        """Solves Parts 2 & 3."""
        final_state = self._get_final_ledger_state(log)
        # Convert defaultdict to a regular dict for clean output
        return {acct_id: data for acct_id, data in final_state["balances"].items()}

    def generate_payout_statement(self, log: str, payout_id: str) -> list:
        """Solves Part 4."""
        final_state = self._get_final_ledger_state(log)
        return final_state["statements"].get(payout_id, [])        
    
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
    print(ledger.calculate_final_balances(log))  
    print("--- Part 2")
    print(dict(ledger.get_all_balances(log)))
    print("--- Part 3")
    print(ledger.generate_payout_statement(log, 'po_A1'))      