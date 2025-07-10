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
    
    def parse_events(self, deposits: str, invoices : list[str]) -> dict:
        partially_paid_invoices = []
        overpaid_invoices = []
        fully_paid_invoices = []
        unpaid_invoices = []
       
        invoices_infomation = {} 
        deposit_tokens = deposits.split("|")
        deposit_id =  deposit_tokens[0]
        customer_balance = defaultdict(lambda: {"balance_due":0})
        customer_credit = defaultdict(int)
        customer_invoice_mapping = defaultdict(list)
        for token in deposit_tokens[1:]:
           t = token.split(":") 
           
           customer_id = t[0]
           amount_paid = int(t[1])
           invoice_id = t[2]
           invoices_infomation[invoice_id] = {
               "customer_id": customer_id,
               "amount_paid": amount_paid
           }
           customer_invoice_mapping[customer_id].append(invoice_id)
        
        
        for invoice in invoices:
            invoice_tokens = invoice.split(",")
            invoice_id = invoice_tokens[0]
            customer_id = invoice_tokens[1]
            amount_due = int(invoice_tokens[2])
            
            if invoices_infomation.get(invoice_id) is not None:
               invoice_info = invoices_infomation[invoice_id]
               if invoice_info["amount_paid"] == amount_due:
                  fully_paid_invoices.append(invoice_id)
               elif invoice_info["amount_paid"] > amount_due:
                   over_paid_amount = invoice_info["amount_paid"] - amount_due
                   overpaid_invoices.append({
                       "invoice_id": invoice_id,
                       "overpaid_amount" : over_paid_amount,
                       "customer_id": customer_id
                   })
                   customer_credit[customer_id] += over_paid_amount
               else:
                   balance_due = amount_due - invoice_info["amount_paid"]
                   partially_paid_invoices.append({
                       "invoice_id": invoice_id,
                       "balance_due" : balance_due
                   })
                   customer_balance[customer_id]["balance_due"] += balance_due
            else:
                balance_due = amount_due
                unpaid_invoices.append({
                       "invoice_id": invoice_id,
                       "balance_due" : balance_due,
                       "customer_id": customer_id
                   }) 
                customer_balance[customer_id]["balance_due"] += balance_due
        
            updated_unpaid = []
        for unpaid in unpaid_invoices:
                invoice_id = unpaid["invoice_id"]
                customer_id = unpaid["customer_id"]
                balance_due = unpaid["balance_due"]
                credit = customer_credit[customer_id]

                if credit >= balance_due:
                    customer_credit[customer_id] -= balance_due
                    updated_unpaid.append({"invoice_id": invoice_id, "balance_due": 0, "status": "PAID"})
                elif credit > 0:
                    unpaid_balance = balance_due - credit
                    customer_credit[customer_id] = 0
                    updated_unpaid.append({"invoice_id": invoice_id, "balance_due": unpaid_balance, "status": "PARTIALLY_PAID"})
                    customer_balance[customer_id]["balance_due"] = unpaid_balance
                else:
                    updated_unpaid.append({"invoice_id": invoice_id, "balance_due": balance_due, "status": "UNPAID"})
        
               
        
        return {"customer_balance" : customer_balance, "overpaid_invoices": overpaid_invoices, "partially_paid_invoices": partially_paid_invoices,
                "fully_paid_invoices": fully_paid_invoices, "unpaid_invoices": updated_unpaid}
    
    def get_fully_paid_info(self, deposits: str, invoices : list[str]) -> dict:
        invoice_info = self.parse_events(deposits, invoices)
        fully_paid_invoices = invoice_info["fully_paid_invoices"]
        ans = {}
        for invoice_id in fully_paid_invoices:
            ans[invoice_id] = "PAID"
        
        return ans
    
    def get_payments(self, deposits: str, invoices : list[str]) -> dict:
        invoice_info = self.parse_events(deposits, invoices)
        partially_paid_invoices = invoice_info["partially_paid_invoices"]
        return partially_paid_invoices
    
    def get_over_payments_and_others(self, deposits: str, invoices : list[str]) -> dict:
        invoice_info = self.parse_events(deposits, invoices)
        overpaid_invoices = invoice_info["overpaid_invoices"]
       
        return overpaid_invoices  
                          
    def get_invoices_status(self, deposits: str, invoices: list[str]) -> dict:
        invoice_info = self.parse_events(deposits, invoices)
        status_map = {}

        for key in invoice_info["partially_paid_invoices"]:
            status_map[key["invoice_id"]] = "PARTIALLY_PAID"
        for key in invoice_info["overpaid_invoices"]:
            status_map[key["invoice_id"]] = "PAID"
        for key in invoice_info["fully_paid_invoices"]:
            status_map[key] = "PAID"
        for key in invoice_info["unpaid_invoices"]:
            status_map[key["invoice_id"]] = key["status"]

        return {
            "invoices": status_map,
            "customer_balance": invoice_info["customer_balance"]
        }          
                                 
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
    print(service.get_invoices_status(deposit_p4, invoices_p4))
    print("-" * 50)        