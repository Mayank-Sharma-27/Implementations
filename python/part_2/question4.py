"""
### Background
Build a system to safely log credit card transactions while masking sensitive data.

### Input Data
```json
{
  "transactions": [
    {
      "id": "txn_001",
      "card_number": "4242424242424242",
      "expiry": "12/25",
      "cvv": "123",
      "amount": 10000,
      "merchant": "Store ABC"
    },
    {
      "id": "txn_002", 
      "card_number": "5555555555554444",
      "expiry": "08/26",
      "cvv": "456",
      "amount": 5000,
      "merchant": "Shop XYZ"
    }
  ]
}
```

### Part 1 (15 minutes)
Create masking functions:
1. **Mask card numbers** (show only last 4 digits: "****-****-****-4242")
2. **Mask CVV completely** ("***")
3. **Keep expiry dates** but validate format

### Part 2 (15 minutes)
Add validation and formatting:
1. **Detect card type** (Visa starts with 4, MasterCard starts with 5)
2. **Validate card number length** (Visa: 16 digits, Amex: 15 digits)
3. **Generate masked transaction logs**

### Part 3 (15 minutes)
Handle compliance requirements:
1. **Support different masking levels** (internal vs external logs)
2. **Log access tracking** (who viewed what when)
3. **Export sanitized data** for analytics team
"""
import re
class Transactions:
    
    def mask_card_number(self, card_number:str, level: str = "external") -> str:
        if level == "internal":
            return card_number[0:6] + "*" * (len(card_number) -10) + card_number[-4:] 
        masking_character = "*"
        masked = masking_character * (len(card_number) - 4) + card_number[-4:]
        grouped = [masked[i:i+4] for i in range(0, len(masked), 4)]
        return "-".join(grouped)
    
    def mask_cvv(self, cvv: str) -> str:
        return "*" * len(cvv)    
        
    
    def get_masked_transactions(self, data: dict) -> dict:
        transactions = data["transactions"]
        
        masked_values: list[dict] = []
        for transaction in transactions:
            masked_values.append({
                "id": transaction["id"],
                "card_number": self.mask_card_number(transaction["card_number"]),
                "expiry" : transaction["expiry"],
                "cvv": self.mask_cvv(transaction["cvv"]),
                "amount": transaction["amount"],
                "merchant": transaction["merchant"]
            })
        return {"transactions": masked_values}
    
    def _get_card_type(self, card_number: str) -> str | None:
        
        if card_number.startswith("4"):
            return "Visa"
        elif card_number.startswith(("34", "37")):
            return "Amex"
        elif card_number.startswith(("51","52","53","54","55")):
            return "MasterCard"
        return None
    
    def _validate_card_type(self, card_number: str) -> bool:
        digits = re.sub(r"\D", "", card_number)
        card_type = self._get_card_type(digits)
        if card_type == "Visa":
            return len(digits) in {13, 16, 19}
        elif card_type == "Amex":
            return len(digits) == 15
        elif card_type == "MasterCard":
            return len(digits) == 16
        return False
                          
    def generate_masked_transaction_logs(self, data: dict) -> list[dict]:
        transaction_logs = []
        transactions = data["transactions"]
        
        for transaction in transactions:
            transaction_logs.append({
                "id": transaction["id"],
                "card_number": self.mask_card_number(transaction["card_number"]),
                "expiry" : transaction["expiry"],
                "cvv": self.mask_cvv(transaction["cvv"]),
                "amount": transaction["amount"],
                "merchant": transaction["merchant"],
                "card_type": self._get_card_type(transaction["card_number"]),
                "valid_card": self._validate_card_type(transaction["card_number"])
            })
        return {"transactions": transaction_logs}
    
    def export_for_analytics(self, data: dict) -> list[dict] :
        sanitized = []
        
        for transaction in data["transactions"]:
            sanitized.append({
                "id": transaction["id"],
                "amount" : transaction["amount"],
                "merchant": transaction["merchant"],
                "card_type": self._get_card_type(transaction["card_number"])
            })
        return sanitized           
        

transactions = Transactions()
data = {
  "transactions": [
    {"id": "txn_001","card_number": "4242424242424242","expiry": "12/25","cvv": "123","amount": 10000,"merchant": "Store ABC"},
    {"id": "txn_002","card_number": "5555-5555-5555-4444","expiry": "08/26","cvv": "456","amount": 5000,"merchant": "Shop XYZ"},
    {"id": "txn_003","card_number": "378282246310005","expiry": "11/26","cvv": "999","amount": 7000,"merchant": "AmEx Store"}
  ]
}
print(transactions.get_masked_transactions(data))            
print(transactions.generate_masked_transaction_logs(data)) 
print(transactions.export_for_analytics(data))
