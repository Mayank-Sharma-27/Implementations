"""
## Question 9: Invoice Generation System

### Background
Generate invoices from subscription and transaction data.

### Input Data
```json
{
  "customer": {
    "id": "cus_123",
    "name": "Acme Corp",
    "email": "billing@acme.com",
    "address": {
      "line1": "123 Main St",
      "city": "San Francisco",
      "state": "CA",
      "zip": "94105"
    }
  },
  "line_items": [
    {
      "description": "Pro Plan Subscription",
      "quantity": 1,
      "unit_price": 2999,
      "period": "2024-01-01 to 2024-01-31"
    },
    {
      "description": "API Calls",
      "quantity": 1500,
      "unit_price": 1,
      "period": "2024-01-01 to 2024-01-31"
    }
  ]
}
```

### Part 1 (15 minutes)
Build invoice calculator:
1. **Calculate line item totals**
2. **Apply tax rates** (8.5% for CA)
3. **Generate invoice number** (INV-YYYY-MM-XXXXX format)

### Part 2 (15 minutes)
Format invoice output:
1. **Generate human-readable invoice**
2. **Format currency amounts** ($29.99 format)
3. **Calculate due date** (30 days from issue)

### Part 3 (15 minutes)
Handle complex scenarios:
1. **Discounts and promotions**
2. **Multi-currency invoices**
3. **PDF generation metadata**

"""

from collections import Counter
from decimal import Decimal, ROUND_HALF_UP
class Invoice:
    
    def build_invoice(self, data: dict) -> dict:
        line_items = data["line_items"]
        customer = data["customer"]
        line_items_info = []
        TAX_RATE = Decimal("0.085")
        month_invoice_mapping = Counter()
        subtotal = Decimal("0.00")
        total_tax = Decimal("0.00")
        for line_item in line_items:
            unit_price = Decimal(str(line_item["unit_price"]))
            quantity = Decimal(str(line_item["quantity"]))
            amount = unit_price * quantity
            tax = (amount * TAX_RATE).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            line_item_total = (amount + tax).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            
            year,month = line_item["period"].split("-")[0:2]
            month_invoice_mapping[month] += 1
            seq_num = str(month_invoice_mapping[month]).zfill(5)
             
            line_items_info.append({
                "invoice_id": f"INV-{year}-{month}-{seq_num}",
                "description": line_item["description"],
                "unit_price": line_item["unit_price"],
                "tax": tax,
                "quantity": line_item["quantity"], 
                "line_item_total": line_item_total
            })
            subtotal += amount
            total_tax += tax
        invoice_total = (subtotal + total_tax).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)   
        return {
        "customer": {
            "id": customer["id"],
            "name": customer.get("name", ""),
            "email": customer.get("email", "")
        },
        "line_items": line_items_info,
        "summary": {
            "subtotal": float(subtotal),
            "total_tax": float(total_tax),
            "grand_total": float(invoice_total)
        }
    }
invoice = Invoice()

data = {
  "customer": {
    "id": "cus_123",
    "name": "Acme Corp",
    "email": "billing@acme.com",
    "address": {
      "line1": "123 Main St",
      "city": "San Francisco",
      "state": "CA",
      "zip": "94105"
    }
  },
  "line_items": [
    {
      "description": "Pro Plan Subscription",
      "quantity": 1,
      "unit_price": 2999,
      "period": "2024-01-01 to 2024-01-31"
    },
    {
      "description": "API Calls",
      "quantity": 1500,
      "unit_price": 1,
      "period": "2024-01-01 to 2024-01-31"
    }
  ]
}
print(invoice.build_invoice(data))
            
        
        
        
        
        