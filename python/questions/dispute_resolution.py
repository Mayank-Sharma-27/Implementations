"""
Stripe-Style Multi-Part Problem: Dispute Resolution Ledger

This problem involves processing a log of payment dispute events to track the
status and financial impact on merchants. The input is a single string where
events are separated by '&'. The event format is:
`dispute_id/merchant_id/transaction_id/timestamp/event_type/amount_minor/metadata`

Part 1: Dispute State Tracking
- Determine the final status of each dispute (`WON`, `LOST`, or `UNDER_REVIEW`)
  based on its most recent event by timestamp.

Part 2: Initial Financial Impact
- Calculate the net financial impact on each merchant. An `OPEN` event debits
  the amount from the merchant, and a `WON` event credits it back.

Part 3: Non-Refundable Dispute Fees
- Modify the calculation to include a fixed, non-refundable fee that is
  debited from the merchant when a dispute is opened.

Part 4: Merchant Reconciliation Report
- Generate a formatted report for a specified merchant, detailing each dispute's
  status, reason, individual impact, and the total net impact for the merchant.
"""
from collections import defaultdict
class DisputeResolution:
   
    def create_dispute_tracking(self, events: str) -> dict:
        disputes = defaultdict(list)
        
        events_tokens = events.split("&")
        
        for events_token in events_tokens:
            logs = events_token.split("/")
            dispute_id = logs[0].strip()
            merchant_id = logs[1].strip()
            transaction_id = logs[2].strip()
            timestamp = logs[3].strip()
            event_type = logs[4].strip()
            amount = logs[5].strip()
            meta_data = logs[6].strip()
            disputes[dispute_id].append({
                  "merchant_id": merchant_id,
                  "transaction_id": transaction_id,
                  "timestamp": timestamp,
                  "event_type": event_type,
                  "amount": int(amount),
                  "meta_data": meta_data
                   
               })  
            
        for dispute_id in disputes.keys():
            disputes[dispute_id] = sorted(disputes[dispute_id], key=lambda p : p["timestamp"])    
        return disputes
    
    def get_dispute_status(self, events: str) -> dict:
        disputes = self.create_dispute_tracking(events)
        
        ans = {}
        for dispute_id, dispute in disputes.items():
            ans[dispute_id] = dispute[-1]["event_type"]
        return ans
    
    def get_merchant_info(self, events: str, dispute_fee: int) -> dict:
        disputes = self.create_dispute_tracking(events)
        merchant_info = defaultdict(int)
        merchant_dispute_mapping = defaultdict(set)
        for dispute_id, dispute in disputes.items():
            for dis in dispute:
                status = dis["event_type"]
                mechant_id = dis["merchant_id"]
                merchant_dispute_mapping[mechant_id].add(dispute_id)
                amount = dis["amount"]
                
                if status == "OPEN":
                    merchant_info[mechant_id] -= amount 
                elif status =="WON":
                    merchant_info[mechant_id] += amount
        
        for merchant_id in merchant_info.keys():
            merchant_info[merchant_id] -= (dispute_fee * len(merchant_dispute_mapping.get(merchant_id)))
              
        return merchant_info
    
    def get_report(self, events: str, dispute_fee: int) -> str:
        disputes = self.create_dispute_tracking(events)
        merchant_info = defaultdict(list)
        for dispute_id, dispute in disputes.items():
            merchant_amount =0
            impact =0
            for dis in dispute:
                status = dis["event_type"]
                amount = dis["amount"]
                if status == "OPEN":
                    merchant_amount -= amount 
                elif status =="WON":
                    merchant_amount += amount
            last_status = dispute[-1]["event_type"]
            transaction_id = dispute[-1]["transaction_id"]
            impact += merchant_amount
            mechant_id = dispute[-1]["merchant_id"]
            merchant_amount -= dispute_fee
            merchant_info[mechant_id].append({
                "dispute_id" : dispute_id,
                "status" : last_status,
                "Reason": "",
                "Impact": merchant_amount,
                "transaction_id": transaction_id
            })   
            
        lines = []
        
        for merchant_id, data in merchant_info.items():
            lines.append(f"Dispute report for :{merchant_id}")
            for d in data:
                status = d["status"]
                reason = d["Reason"]
                impact = d["Impact"]
                id = d["dispute_id"]
                transaction_id = d["transaction_id"]
                lines.append(f"- Dispute {id} (Transaction {transaction_id})")
                lines.append("\n")
                lines.append(f"Status: {status}")
                lines.append("\n")
                lines.append(f"Reason : {reason}")
                lines.append("\n")
                lines.append(f"Impact: {impact}")
            lines.append(f"Total Net impact {self.get_merchant_info(events, dispute_fee)[mechant_id]}")        
                
        return "\n".join(lines)           
            
if __name__ =="__main__":
    log = "d_1/m_A/tr_1/2025-06-15T10:00:00Z/OPEN/5000/reason=product_not_received&d_2/m_B/tr_2/2025-06-16T11:00:00Z/OPEN/2500/reason=fraudulent&d_1/m_A/tr_1/2025-06-20T14:00:00Z/WON/5000/&d_3/m_A/tr_3/2025-06-18T09:00:00Z/OPEN/10000/reason=duplicate_charge&d_2/m_B/tr_2/2025-06-19T12:00:00Z/EVIDENCE_SUBMITTED/2500/evidence_id=evi_abc"
    dispute_resoulution = DisputeResolution()
    #print(dispute_resoulution.get_dispute_status(log))
    print("\n")
    print(dict(dispute_resoulution.get_merchant_info(log, 0)))
    print("\n")
    print(dict(dispute_resoulution.get_merchant_info(log, 1500)))
    print("\n")
    print(dispute_resoulution.get_report(log, 1500))
    print("\n")