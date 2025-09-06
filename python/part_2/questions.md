# Stripe Phone Screen Questions - Pair Programming Round

## Overview

These questions are based on actual Stripe phone screen experiences from 2024-2025. The round is 45 minutes, conducted on CoderPad, and focuses on practical coding rather than algorithmic puzzles. Expect iterative requirements to be added as you progress.

**Key Focus Areas:**

- JSON/Object manipulation
- String processing and parsing
- Data transformation and formatting
- Real-world payment processing scenarios
- Quick, clean implementation

---

## Question 1: Payment Transaction Processor

### Background

You're processing payment transaction logs in JSON format. Build a system to parse and analyze this data.

### Input Data

```json
[
  {
    "id": "txn_123",
    "amount": 2500,
    "currency": "USD",
    "status": "succeeded",
    "customer_id": "cus_abc",
    "created": "2024-01-15T10:30:00Z",
    "payment_method": "card"
  },
  {
    "id": "txn_124",
    "amount": 1000,
    "currency": "EUR",
    "status": "failed",
    "customer_id": "cus_xyz",
    "created": "2024-01-15T11:00:00Z",
    "payment_method": "bank_transfer",
    "failure_code": "insufficient_funds"
  }
]
```

### Part 1 (15 minutes)

Build a function that:

1. **Parses the JSON data**
2. **Returns total successful transaction amount in USD** (assume EUR to USD rate is 1.1)
3. **Lists all unique customer IDs**

### Part 2 (15 minutes)

Add functionality to:

1. **Group transactions by payment method**
2. **Calculate success rate for each payment method**
3. **Find the customer with the highest total transaction volume**

### Part 3 (15 minutes)

Handle these new requirements:

1. **Filter transactions by date range**
2. **Support new currency conversion rates** (passed as parameter)
3. **Generate a summary report** showing daily totals

---

## Question 2: Subscription Billing Calculator

### Background

Process subscription billing data to calculate prorated charges and generate invoices.

### Input Data

```json
{
  "customer": {
    "id": "cus_123",
    "email": "john@example.com"
  },
  "subscription": {
    "id": "sub_abc",
    "plan_amount": 2999,
    "billing_cycle": "monthly",
    "current_period_start": "2024-01-01",
    "current_period_end": "2024-01-31"
  },
  "events": [
    {
      "type": "plan_change",
      "date": "2024-01-15",
      "old_amount": 2999,
      "new_amount": 4999
    }
  ]
}
```

### Part 1 (15 minutes)

Create functions to:

1. **Calculate monthly charge** (no plan changes)
2. **Parse date strings** into usable format
3. **Validate input data** (check required fields)

### Part 2 (15 minutes)

Add proration logic:

1. **Calculate prorated refund** for unused time on old plan
2. **Calculate prorated charge** for new plan
3. **Return net amount to charge customer**

### Part 3 (15 minutes)

Handle edge cases:

1. **Multiple plan changes in one month**
2. **Subscription cancellation mid-cycle**
3. **Generate itemized invoice breakdown**

---

## Question 3: Webhook Event Processor

### Background

Build a system to process incoming webhook events from various payment providers.

### Input Data

```json
[
  {
    "id": "evt_001",
    "type": "payment.succeeded",
    "provider": "stripe",
    "timestamp": 1640995200,
    "data": {
      "payment_id": "pay_123",
      "amount": 5000,
      "customer": "cus_abc"
    }
  },
  {
    "id": "evt_002",
    "type": "payment_failed",
    "provider": "paypal",
    "timestamp": 1640995300,
    "data": {
      "transaction_id": "txn_456",
      "amount": 2500,
      "user_id": "user_xyz",
      "error": "card_declined"
    }
  }
]
```

### Part 1 (15 minutes)

Build a webhook processor that:

1. **Normalizes different provider formats** (stripe uses "customer", paypal uses "user_id")
2. **Converts timestamps to readable dates**
3. **Filters events by type**

### Part 2 (15 minutes)

Add event handling:

1. **Deduplicate events** (same id shouldn't be processed twice)
2. **Process events chronologically**
3. **Update customer payment status** based on events

### Part 3 (15 minutes)

Handle real-time requirements:

1. **Queue system simulation** (mark events as processing/completed)
2. **Retry failed events** with exponential backoff
3. **Generate event processing summary**

---

## Question 4: Credit Card Data Masker

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

1. **Mask card numbers** (show only last 4 digits: "\***\*-\*\***-\*\*\*\*-4242")
2. **Mask CVV completely** ("\*\*\*")
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

---

## Question 5: Currency Exchange Rate Calculator

### Background

Build a currency conversion system for international payments.

### Input Data

```json
{
  "rates": {
    "USD_EUR": 0.85,
    "USD_GBP": 0.73,
    "EUR_GBP": 0.86,
    "USD_JPY": 110.0
  },
  "transactions": [
    {
      "id": "tx_001",
      "amount": 1000,
      "from_currency": "USD",
      "to_currency": "EUR"
    },
    {
      "id": "tx_002",
      "amount": 500,
      "from_currency": "EUR",
      "to_currency": "GBP"
    }
  ]
}
```

### Part 1 (15 minutes)

Build conversion functions:

1. **Direct conversion** (USD to EUR using USD_EUR rate)
2. **Reverse conversion** (EUR to USD using 1/USD_EUR rate)
3. **Round to 2 decimal places**

### Part 2 (15 minutes)

Handle indirect conversions:

1. **Multi-hop conversion** (USD → EUR → GBP)
2. **Find shortest conversion path**
3. **Calculate conversion fees** (0.5% per hop)

### Part 3 (15 minutes)

Add advanced features:

1. **Historical rate lookup** (rates change over time)
2. **Batch conversion processing**
3. **Generate conversion audit trail**

---

## Question 6: Payment Method Validator

### Background

Validate different payment methods and extract relevant information.

### Input Data

```python
payment_methods = [
    {
        "type": "card",
        "number": "4242 4242 4242 4242",
        "expiry": "12/25",
        "name": "John Doe"
    },
    {
        "type": "bank_account",
        "routing": "110000000",
        "account": "1234567890",
        "account_type": "checking"
    },
    {
        "type": "email",
        "address": "john@example.com"
    }
]
```

### Part 1 (15 minutes)

Create validation functions:

1. **Validate card numbers** using Luhn algorithm
2. **Validate email format**
3. **Validate routing numbers** (9 digits)

### Part 2 (15 minutes)

Add processing logic:

1. **Normalize card numbers** (remove spaces/dashes)
2. **Extract card brand** (Visa, MasterCard, Amex)
3. **Format bank account** for display

### Part 3 (15 minutes)

Handle edge cases:

1. **International payment methods** (IBAN, SEPA)
2. **Expired card detection**
3. **Generate validation error messages**

---

## Question 7: Fraud Detection Data Processor

### Background

Process transaction data to identify potentially fraudulent patterns.

### Input Data

```json
{
  "transactions": [
    {
      "id": "tx_001",
      "customer_id": "cus_123",
      "amount": 100,
      "location": "US",
      "timestamp": "2024-01-15T10:00:00Z",
      "ip_address": "192.168.1.1"
    },
    {
      "id": "tx_002",
      "customer_id": "cus_123",
      "amount": 5000,
      "location": "RU",
      "timestamp": "2024-01-15T10:05:00Z",
      "ip_address": "10.0.0.1"
    }
  ]
}
```

### Part 1 (15 minutes)

Build detection functions:

1. **Calculate transaction velocity** (transactions per hour per customer)
2. **Detect location anomalies** (same customer, different countries)
3. **Flag high-amount transactions**

### Part 2 (15 minutes)

Add pattern analysis:

1. **Detect rapid-fire transactions** (multiple transactions in minutes)
2. **Check IP address changes**
3. **Calculate risk scores** (0-100 scale)

### Part 3 (15 minutes)

Generate reports:

1. **List high-risk transactions**
2. **Customer risk profiles**
3. **Real-time alerts system**

---

## Question 8: Refund Processing System

### Background

Process refund requests and update transaction states.

### Input Data

```json
{
  "original_transactions": [
    {
      "id": "pay_123",
      "amount": 10000,
      "currency": "USD",
      "status": "succeeded",
      "customer_id": "cus_abc"
    }
  ],
  "refund_requests": [
    {
      "id": "rfnd_001",
      "payment_id": "pay_123",
      "amount": 3000,
      "reason": "customer_request",
      "requested_at": "2024-01-16T10:00:00Z"
    }
  ]
}
```

### Part 1 (15 minutes)

Build refund processor:

1. **Validate refund amount** (can't exceed original payment)
2. **Check payment status** (can only refund successful payments)
3. **Calculate remaining refundable amount**

### Part 2 (15 minutes)

Handle partial refunds:

1. **Track multiple refunds** for same payment
2. **Update payment status** (fully_refunded vs partially_refunded)
3. **Generate refund confirmation**

### Part 3 (15 minutes)

Add business logic:

1. **Refund deadline enforcement** (30 days from payment)
2. **Fee calculations** (refund fees)
3. **Batch refund processing**

---

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

---

## Question 10: API Rate Limiting System

### Background

Implement a rate limiting system for API requests.

### Input Data

```json
{
  "requests": [
    {
      "api_key": "sk_test_123",
      "endpoint": "/v1/charges",
      "timestamp": 1640995200,
      "ip": "192.168.1.1"
    },
    {
      "api_key": "sk_test_123",
      "endpoint": "/v1/charges",
      "timestamp": 1640995201,
      "ip": "192.168.1.1"
    }
  ],
  "limits": {
    "sk_test_123": {
      "requests_per_minute": 100,
      "requests_per_hour": 1000
    }
  }
}
```

### Part 1 (15 minutes)

Build rate limiter:

1. **Track requests per API key**
2. **Check minute and hour limits**
3. **Return allow/deny decision**

### Part 2 (15 minutes)

Add sliding window:

1. **Implement sliding window counter**
2. **Clean up old request data**
3. **Handle burst traffic**

### Part 3 (15 minutes)

Advanced features:

1. **Different limits per endpoint**
2. **IP-based rate limiting**
3. **Rate limit headers** (X-RateLimit-Remaining, etc.)

---

## Tips for Success

1. **Start Simple**: Get basic functionality working first
2. **Ask Questions**: Clarify requirements as you go
3. **Think Out Loud**: Explain your approach
4. **Handle Edge Cases**: Consider null values, empty arrays, invalid input
5. **Test Your Code**: Use the provided examples to verify
6. **Iterate Quickly**: Implement fast, refine later
7. **Focus on Readability**: Clean, understandable code matters

## Common Patterns to Practice

- JSON parsing and manipulation
- String formatting and validation
- Date/time processing
- Dictionary/map operations
- List comprehensions and filtering
- Error handling and validation
- Data aggregation and grouping

Good luck with your Stripe interview!
