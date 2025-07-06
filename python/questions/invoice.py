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
    
    def parse_input(self, payment: str, invoices: list[str]) -> str:
        result = ""
        if not payment or not invoices:
            return ValueError("Invalid input")
        
        payment_tokens = payment.split(",")
        payment_id = payment_tokens[0].strip()
        invoice_id = payment_tokens[2].split(":")[1].strip()
        
        for invoice in invoices:
            invoice_tokens = invoice.split(",")
            if invoice_tokens[0].strip() == invoice_id:
                invoice_date = invoice_tokens[1]
                invoice_amount = invoice_tokens[2]
                result = f"{payment_id} pays of {invoice_amount} due on {invoice_date}"
                break
        return result 
    
    def parse_with_multi_format(self, payment: str, invoices: list[str]) -> str:
        result = ""
        if not payment or not invoices:
            return ValueError("Invalid Input")
        
        payment_tokens = payment.split(",")
        payment_id = payment_tokens[0].strip()
        payment_amount = payment_tokens[1].strip()
        
        
        for invoice in invoices:
            invoice_tokens = invoice.split(",")
            if len(invoice_tokens) !=3:
                continue
            invoice_amount = invoice_tokens[2].strip()
            
            if payment_amount == invoice_amount:
                invoice_date = invoice_tokens[1]
                invoice_id = invoice_tokens[0]
                result = f"{payment_id} pays of {invoice_amount} for {invoice_id} due on {invoice_date}"
                break
        return result
    
    
    def parse_with_forgiveness(self, payment: str, invoices: list[str], forgiveness: str) -> str:
        result = ""
        if not payment or not invoices or not forgiveness:
            return ValueError("Invalid Input")
        
        payment_tokens = payment.split(",")
        payment_id = payment_tokens[0].strip()
        payment_amount = int(payment_tokens[1].strip())
        forgiveness = int(forgiveness)
        low_range = payment_amount - forgiveness
        high_range = payment_amount + forgiveness
        
        for invoice in invoices:
            invoice_tokens = invoice.split(",")
            if len(invoice_tokens) != 3:
                continue
            
            invoice_amount = int(invoice_tokens[2].strip()) 
            invoice_date = invoice_tokens[1]
            invoice_id = invoice_tokens[0]
            
            if payment_amount == invoice_amount:
                result  = f"{payment_id} pays off {payment_amount} for {invoice_id} due on {invoice_date}"
            elif payment_amount >= low_range and payment_amount <= high_range:
                forgiven = abs(payment_amount - invoice_amount)
                result  = f"{payment_id} pays off {payment_amount} for {invoice_id} due on {invoice_date} ({forgiven} forgiven)"
                
        return result
    
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
    forgiveness = "300"
    print(invoice.parse_with_forgiveness(payment1, invoices1, forgiveness))         
            
         