"""
Stripe-Style Multi-Part Problem: Bank Deposit Reconciliation

This problem simulates the reconciliation of a single, consolidated bank
deposit against a list of outstanding customer invoices. The goal is to
correctly apply payments and manage balances for partial or overpayments.

Inputs:
- `deposit_data`: A single string representing the deposit, formatted as:
  `deposit_id|customer_id:amount_paid:invoice_id|...`
- `outstanding_invoices`: A list of strings for open invoices, formatted as:
  `invoice_id,customer_id,amount_due`

---

Part 1: Exact Reconciliation
- Process payments that exactly match the invoice's amount due.

Part 2: Handling Partial Payments
- Add logic to handle underpayments, leaving an invoice as "PARTIALLY_PAID"
  with a remaining balance.

Part 3: Handling Overpayments and Customer Credits
- Add logic to handle overpayments, where the excess amount is added to a
  customer's credit balance.

Part 4: Automatic Credit Application
- After processing the deposit, automatically apply any generated customer
  credits to their other outstanding invoices, starting with the oldest.
"""


from collections import defaultdict

class Bank:
    
    def parse_events(self, deposit_data: str, invoices: str) -> dict:
        parsed_data = {}
        
        deposit_data_events = []
        main_parts = deposit_data.split('|')
        id = main_parts[0]
        for data in main_parts[1:]:
            if not data:
                continue
            
            c_id, amount, invoice_id = data.split(":")
            deposit_data_events.append({
                "id": id,
                "c_id": c_id,
                "amount": int(amount),
                "invoice_id": invoice_id
            })
        invoices_events = []
        
        for data in invoices:
            invoice_id, c_id, amount = data.split(",")
            invoices_events.append({
               "invoice_id": invoice_id,
               "c_id": c_id,
               "amount": int(amount)
            })
        parsed_data["deposit_data_events"] = deposit_data_events
        parsed_data["invoices"] = invoices_events 
        return parsed_data
    
    def get_invoice_info_amounts(self, deposit_data: str, invoices: str) -> list:
        parsed_data = self.parse_events(deposit_data, invoices)
        paid_invoices = []
        for invoice in parsed_data["invoices"]:
            id =  invoice["invoice_id"]
            c_id = invoice["c_id"]
            invoice_amount = invoice["amount"]
            
            for deposit_data_event in parsed_data["deposit_data_events"]:
                deposit_id  = deposit_data_event["id"]
                amount = deposit_data_event["amount"]
                invoice_id = deposit_data_event["invoice_id"]
                if amount == invoice_amount and invoice_id == id: 
                    paid_invoices.append({
                        "deposit_id": deposit_id,
                        "c_id": c_id,
                        "amount": int(amount),
                        "invoice_id": invoice_id,
                        "status": "PAID"
                    })
                elif amount < invoice_amount and invoice_id == id:
                    amount_remaining = invoice_amount - amount 
                    paid_invoices.append({
                        "deposit_id": deposit_id,
                        "c_id": c_id,
                        "amount": int(amount),
                        "invoice_id": invoice_id,
                        "status": "PARTIALLY_PAID",
                        "amount_remaining": amount_remaining 
                    })
                elif amount > invoice_amount and invoice_id == id:
                    over_paid_amount = amount - invoice_amount 
                    paid_invoices.append({
                        "deposit_id": deposit_id,
                        "c_id": c_id,
                        "amount": int(amount),
                        "invoice_id": invoice_id,
                        "status": "PAID",
                        "over_paid_amount": over_paid_amount 
                    })
                                          
        
        return paid_invoices
        
    def get_fully_paid_info(self, deposit_data: str, invoices: str) -> list[str]:
        invoice_info = self.get_invoice_info_amounts(deposit_data, invoices)
        lines = []
        for invoice in invoice_info:
            status = invoice["status"]
            deposit_id = invoice["deposit_id"]
            invoice_id = invoice["invoice_id"]
            amount = invoice["amount"]
            c_id = invoice["c_id"]
            
            if status == "PAID":
                lines.append(f"Applied payment from deposit {deposit_id}, to fully pay invoice {invoice_id}, for customer {c_id} ({amount})")
            
        return "\n".join(lines) 
    
    def get_payments(self, deposit_data: str, invoices: str) -> dict:
        invoice_info = self.get_invoice_info_amounts(deposit_data, invoices)
    
        ans = {}
        for payment in invoice_info:
            invoice_id = payment["invoice_id"]
            
            status = payment["status"]
            if status == "PARTIALLY_PAID": 
                amount_remaining = payment["amount_remaining"]
                ans[invoice_id] = {"status": "PARTIALLY_PAID", "amount_remaining": amount_remaining}
            else:
                ans[invoice_id] = {"status": "PAID"}          
        all_invoices = self.parse_events(deposit_data, invoices)["invoices"]
        for invoice in all_invoices:
            invoice_id = invoice["invoice_id"]
            amount = int(invoice["amount"])
            if ans.get(invoice_id) is None:
                ans[invoice_id] = {"status": "UNPAID", "amount_remaining":amount}
            
                
        return ans
    
    def get_over_payments_and_others(self, deposit_data: str, invoices: str) -> list:
        ans = []
        
        
        payments = self.get_payments(deposit_data, invoices)
        invoice_info = self.get_invoice_info_amounts(deposit_data, invoices)
        ans.append(payments)
        credit_informations = {}
        
        for payment in invoice_info:
            c_id = payment["c_id"]
            status = payment["status"] 
            
            if payment.get("over_paid_amount") is not None:
               over_paid_amount = payment["over_paid_amount"]
               credit_informations[c_id] = {"credit_balance": over_paid_amount} 
        
        ans.append(credit_informations)
        
        return ans           
    
    def _get_auto_matic_credit_application(self, deposit_data: str, invoices: str) -> list:
        credit_informations = self.get_over_payments_and_others(deposit_data, invoices)
        all_invoices = self.parse_events(deposit_data, invoices)["invoices"]
        
        for invoice in all_invoices:
            
            invoice_id = invoice_id = invoice["invoice_id"]
            c_id = invoice["c_id"]
            if c_id not in credit_informations[1].keys(): 
                continue
            
            pending_invoice = credit_informations[0][invoice_id]
            if pending_invoice["status"] == "PAID":
                continue
            
            
            if pending_invoice["status"] == "UNPAID" or pending_invoice["status"] == "PARTIALLY_PAID":
                customer_credit = credit_informations[1][c_id]["credit_balance"]
                
               
                if pending_invoice["amount_remaining"] <= customer_credit:
                   pending_invoice["status"] = "PAID"
                  
                   customer_credit = customer_credit - pending_invoice["amount_remaining"]
                   del pending_invoice["amount_remaining"]
                   credit_informations[1][c_id]["credit_balance"] = customer_credit
                else:
                   pending_invoice["amount_remaining"] = pending_invoice["amount_remaining"] - customer_credit
                   customer_credit = 0     
                   credit_informations[1][c_id]["credit_balance"] = 0
                   pending_invoice["status"] = "PARTIALLY_PAID"
        
        return credit_informations           
        
        
        
        
if __name__ == "__main__":
    # --- Part 1 Test Data ---
    deposit_p1 = "dep_01|cust_A:1000:inv_101|cust_B:2500:inv_102|cust_C:500:inv_103"
    invoices_p1 = ["inv_101,cust_A,1000", "inv_102,cust_B,2550", "inv_103,cust_C,500"]

    # --- Part 2 Test Data ---
    # Uses the same data as Part 1
    deposit_p2 = deposit_p1
    invoices_p2 = invoices_p1

    # --- Part 3 Test Data ---
    deposit_p3 = "dep_02|cust_X:1500:inv_201|cust_Y:2000:inv_202|cust_X:800:inv_203"
    invoices_p3 = ["inv_201,cust_X,1200", "inv_202,cust_Y,2100", "inv_203,cust_X,800"]

    # --- Part 4 Test Data ---
    deposit_p4 = "dep_03|cust_M:3000:inv_301"
    invoices_p4 = ["inv_301,cust_M,2500", "inv_302,cust_M,400", "inv_303,cust_M,500"]

    # Instantiate your solution class
    service = Bank() # Replace with your class name

    print("## Part 1: Exact Matches ##")
    print(service.get_fully_paid_info(deposit_p1, invoices_p1))
    print("-" * 50)

    print("## Part 2: Handling Partial Payments ##")
    print(service.get_payments(deposit_p2, invoices_p2))
    print("-" * 50)

    print("## Part 3: Handling Overpayments and Credits ##")
    print(service.get_over_payments_and_others(deposit_p3, invoices_p3))
    print("-" * 50)

    print("## Part 4: Automatic Credit Application ##")
    print(service._get_auto_matic_credit_application(deposit_p4, invoices_p4))
    print("-" * 50)        