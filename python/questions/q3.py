""" Stripe’s Invoicing product allows businesses to create and send invoices to their customers. While many invoices can be paid directly, there are cases where standalone payments need to be reconciled with open invoices for a customer.

Your task is to write a program that matches incoming payments to their corresponding invoices based on the payment’s memo line.

You are given:
• A payment string
• A list of invoice strings

The payment string is a comma-separated string containing:

The payment ID (e.g., “payment123”)
The payment amount in USD minor units (e.g., $1.00 = 100)
The memo line, which always follows the format “Paying off: {INVOICE_ID}”
Each invoice string is also comma-separated and contains:

The invoice ID
The due date of the invoice (e.g., “2024-01-01”)
The amount due in USD minor units
You need to:
• Parse the payment and invoices.
• Find the invoice mentioned in the memo line.
• Output a formatted string describing the reconciliation.

Input Example:
payment = "payment5,1000,Paying off: invoiceC"
invoices = [
"invoiceA,2024-01-01,100",
"invoiceB,2024-02-01,200",
"invoiceC,2023-01-30,1000"
]

Expected Output:
payment5 pays off 1000 for invoiceC due on 2023-01-30 """

class Invoice:
    
    def parse_input(self, payment: str, invoices: list) -> str:
        payment_tokens = payment.split(",")
        payment_id = payment_tokens[0].strip()
        amount = payment_tokens[1].strip()
        
        payment_invoice_id = payment_tokens[2].split(":")[1].strip()
        
        for invoice in invoices:
            invoice_tokens = invoice.split(",")
            invoice_id = invoice_tokens[0]
            date = invoice_tokens[1]
            if payment_invoice_id == invoice_id:
                return f"{payment_id} pays off {amount}for {invoice_id} due to {date}"
            
        return ""    
        
    def parse_with_multi_format(self, payment: str, invoices: list) -> str:
        payment_tokens = payment.split(",")
        payment_id = payment_tokens[0].strip()
        amount = payment_tokens[1].strip()
        payment_type = payment_tokens[2].strip()
        
        for invoice in invoices:
            invoice_tokens = invoice.split(",")
            invoice_id = invoice_tokens[0]
            invoice_amount = invoice_tokens[2]
            date = invoice_tokens[1]
            
            if invoice_amount == amount:
                return f"{payment_id} pays off {amount} for {invoice_id} due to {date} by {payment_type}"
        
        return ""
    
    def parse_with_forgiveness(self, payment: str, invoices: list, forgiveness: int) -> str:
        payment_tokens = payment.split(",")
        payment_id = payment_tokens[0].strip()
        amount = int(payment_tokens[1].strip())
        payment_type = payment_tokens[2].strip()  
        low_range = amount - forgiveness
        high_range = amount + forgiveness
        
        for invoice in invoices:
            invoice_tokens = invoice.split(",") 
            invoice_id = invoice_tokens[0]
            invoice_amount = invoice_tokens[2]
            date = invoice_tokens[1]
            
            if invoice_amount == amount:
                return f"{payment_id} pays off {amount} for {invoice_id} due to {date} by {payment_type}" 
            elif amount >= low_range and amount <= high_range:
                forgiven = abs(amount - int(invoice_amount))
                return f"{payment_id} pays off {amount} for {invoice_id} due to {date} by {payment_type} with forgiveness {forgiven}" 
        
        return ""    
            
        
    
if __name__ == "__main__":
                    
    invoice = Invoice()
    
    payment = "payment5,1000,Paying off: invoiceC"
    invoices = ["invoiceA,2024-01-01,100", "invoiceB,2024-02-01,200", "invoiceC,2023-01-30,5000"]
    
    print(invoice.parse_input(payment, invoices))
    
    print("part2")
    payment1 = "payment5,200,Bank transfer" 
    invoices1 = ["invoiceA,2024-01-01,100", "invoiceB,2024-02-01,200", "invoiceC,2023-01-30,5000"]
    print(invoice.parse_with_multi_format(payment, invoices))
    print(invoice.parse_with_multi_format(payment1, invoices1)) 
    
    print (" part 3")
    payment1 = "payment5,700,Bank transfer" 
    invoices1 = ["invoiceA,2024-01-01,900", "invoiceB,2024-02-01,1000", "invoiceC,2023-01-30,1000"]
    forgiveness = 300
    print(invoice.parse_with_forgiveness(payment1, invoices1, forgiveness))         
            
         