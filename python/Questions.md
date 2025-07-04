Of course. My apologies for omitting the sample inputs. You are right, having a concrete example to test against is crucial.

Here are the 14 problems again, rewritten in Markdown format, with a `Sample Input` section added to each one. This format will be perfect for your GitHub repository.

-----

## Problem 1: Subscription Proration Calculator

### Story

You are building the proration engine for Stripe Billing. When a user changes their subscription plan mid-month (e.g., from 'basic' to 'pro'), your service must calculate the credit for unused time on the old plan and the charge for the remaining time on the new plan. Assume all months have 30 days.

### Input Format

  - A log of subscription events separated by `&`. Format: `timestamp;customer_id;event_type;plan_id`
  - A second input provides plan costs: `plan_id:cost_per_month_in_cents`.

### The Task

1.  **Final Subscription Status:** Process the log to determine the final active plan for each customer. A `CANCEL` event means the customer has no active plan.
2.  **Simple Monthly Cost:** Calculate the total monthly bill for each customer assuming they were on their final plan for the entire 30-day month.
3.  **Poration Calculation:** Calculate the prorated cost for the month. When a plan change occurs, the customer is credited for the unused portion of their old plan and charged for the remaining portion of the new plan.
4.  **Final Invoice Generation:** Generate a summary invoice for each customer, listing each billing event (initial subscription, credits, new charges) and the final total amount due.

### Sample Input

```python
event_log = "2025-01-01T00:00:00Z;cust_A;SUBSCRIBE;basic&2025-01-15T00:00:00Z;cust_A;UPGRADE;pro&2025-01-01T00:00:00Z;cust_B;SUBSCRIBE;pro"
plan_costs = "basic:1000,pro:5000"
```

-----

## Problem 2: Stripe Capital Repayment Ledger

### Story

Stripe Capital offers loans to businesses. These loans are repaid automatically by holding back a percentage of the merchant's daily sales revenue until the loan is fully repaid. You are building the service that tracks these repayments.

### Input Format

  - A list of loans, format: `loan_id;merchant_id;principal_cents;repayment_percentage`.
  - A log of daily sales, format: `date;merchant_id;sales_amount_cents`. The log is a single string with entries separated by `|`.

### The Task

1.  **Daily Repayment Calculation:** For each entry in the daily sales log, calculate the amount that should be withheld for loan repayment.
2.  **Remaining Loan Balance:** Process the entire sales log chronologically. For each merchant, calculate the remaining balance on their loan.
3.  **Handling Zero-Sales Days:** Ensure your logic correctly handles days with zero sales (no repayment).
4.  **Loan Status Report:** Generate a final report for all merchants with loans, including their original principal, total amount repaid, remaining balance, and a status of `REPAID` or `OUTSTANDING`.

### Sample Input

```python
loans = ["loan_1;m_A;500000;10", "loan_2;m_B;1000000;15"]
sales_log = "2025-03-01;m_A;10000|2025-03-01;m_B;25000|2025-03-02;m_A;0|2025-03-02;m_B;30000"
```

-----

## Problem 3: API Rate Limiter (Leaky Bucket)

### Story

You are implementing a "leaky bucket" rate limiter to protect a critical API endpoint. Requests of different "sizes" add "water" to a bucket. The bucket leaks at a constant rate. A request is rejected if adding its size would cause the bucket to overflow.

### Input Format

  - A log of API requests separated by `~`. Format: `timestamp;api_key;request_id;request_size`.
  - Initial parameters: `bucket_capacity`, `leak_rate_per_second`.

### The Task

1.  **Simple Request Counter:** Implement a basic rate limiter that only counts the number of requests in the last 60 seconds per `api_key`.
2.  **Leaky Bucket Implementation:** Implement the core leaky bucket logic. At the time of each request, calculate how much has leaked, then determine if the new request fits.
3.  **Request Outcomes:** Process the log chronologically and return a map of each `request_id` to its outcome: `ACCEPTED` or `REJECTED`.
4.  **Per-Key Summary:** Generate a summary report for each `api_key`, including total requests received, accepted, and rejected.

### Sample Input

```python
requests_log = "2025-01-01T10:00:00Z;key_A;req_1;10~2025-01-01T10:00:00Z;key_A;req_2;15~2025-01-01T10:00:01Z;key_A;req_3;20"
bucket_capacity = 30
leak_rate_per_second = 10
```

-----

## Problem 4: Service Dependency Latency (Critical Path)

### Story

A single API request at Stripe triggers a cascade of internal service calls. You are building a monitoring tool to identify performance bottlenecks by finding the "critical path"—the slowest chain of dependent calls.

### Input Format

  - A string representing a directed acyclic graph (DAG) of service calls, separated by `,`. Format: `caller_service:callee_service:latency_ms`.

### The Task

1.  **Direct Dependency Latency:** Write a function that takes a `caller_service` and `callee_service` and returns the latency if a direct link exists.
2.  **Total Latency for a Simple Chain:** Given a specific path of services (e.g., `A -> B -> C`), calculate the total latency.
3.  **Finding the Critical Path:** Given a `start_service` and `end_service`, find the path between them with the highest total latency.
4.  **Handling Parallel Calls:** A service can make multiple calls that execute in parallel. The time it takes is determined by the *slowest* of its parallel calls. Update your critical path logic to handle this.

### Sample Input

```python
dependency_graph = "A:B:50,A:C:100,B:D:40,C:D:30"
```

-----

## Problem 5: Stripe Atlas Document Verification

### Story

Stripe Atlas helps founders start a company. The process involves submitting several documents, which go through a verification workflow. You are building a service to track the status of each company's application.

### Input Format

  - A log of document events, separated by `&`. Format: `timestamp;company_id;doc_id;event_type;details`.
  - A second input defines the required documents: a list of strings.

### The Task

1.  **Document Status:** Determine the final status of each individual document (`UPLOADED`, `VERIFIED`, `FAILED`).
2.  **Company Application Status:** Determine the overall status of each company's application (`COMPLETE`, `ACTION_REQUIRED`, `PENDING`).
3.  **Missing Documents:** For any company that is not `COMPLETE`, provide a list of required documents that are still missing or not verified.
4.  **Full Company Report:** Generate a report for each company including its overall status and a detailed breakdown of each required document's status.

### Sample Input

```python
required_docs = ["articles_of_incorporation", "founder_agreement"]
event_log = "2025-02-01T10:00:00Z;comp_A;doc_1;DOC_UPLOADED;doc_type=articles_of_incorporation&2025-02-02T11:00:00Z;comp_A;doc_1;VERIFICATION_PASSED;doc_type=articles_of_incorporation"
```

-----

## Problem 6: Checkout Session Itemization

### Story

You are building the backend for Stripe Checkout. A customer creates a session, adds/removes items, applies a coupon, and confirms the purchase. You need to calculate the final amount.

### Input Format

  - A log of events for a single checkout session, separated by `|`. Format: `timestamp;event_type;data`.

### The Task

1.  **Shopping Cart Contents:** Before the `PURCHASE_CONFIRMED` event, return a list of items in the cart and their final quantities.
2.  **Subtotal Calculation:** Calculate the subtotal of the cart (sum of `price * quantity`).
3.  **Applying a Discount:** Handle a `COUPON_APPLIED` event (`PERCENT` or `FIXED`) and calculate the final total.
4.  **Final Order Summary:** Generate a summary object including items, subtotal, discount applied, and final total.

### Sample Input

```python
session_log = "2025-03-10T10:00:00Z;ITEM_ADDED;item_id=prod_A;price=1000;quantity=2|2025-03-10T10:01:00Z;ITEM_ADDED;item_id=prod_B;price=500;quantity=1|2025-03-10T10:02:00Z;ITEM_REMOVED;item_id=prod_A;quantity=1|2025-03-10T10:03:00Z;COUPON_APPLIED;coupon_id=SAVE10;type=PERCENT;value=10|2025-03-10T10:04:00Z;PURCHASE_CONFIRMED;"
```

-----

## Problem 7: Multi-Factor Authentication (MFA) Policy Engine

### Story

You are building a policy engine to determine if a login attempt requires Multi-Factor Authentication (MFA) based on rules and login history.

### Input Format

  - A set of rules, format: `risk_level:mfa_required`.
  - A log of login attempts, separated by `~`. Format: `timestamp;user_id;ip_address;device_id;outcome`.

### The Task

1.  **Login History:** For each user, compile a list of their unique `ip_address`es and `device_id`s from successful past logins.
2.  **Risk Assessment:** For a new login, determine its risk level (`LOW`, `MEDIUM`, `HIGH`) based on whether the IP and device are new.
3.  **MFA Decision:** Using the rules and risk level, decide if MFA is required for a new login attempt.
4.  **Lockout Policy:** Add a lockout rule: 3 consecutive `FAILURE`s lock the account. Deny any login attempt for a locked account.

### Sample Input

```python
rules = "LOW:FALSE,MEDIUM:TRUE,HIGH:TRUE"
login_log = "2025-04-01T10:00:00Z;user_1;1.1.1.1;device_A;SUCCESS~2025-04-02T11:00:00Z;user_1;2.2.2.2;device_A;SUCCESS"
new_login_attempt = "2025-04-03T12:00:00Z;user_1;2.2.2.2;device_B;ATTEMPT"
```

-----

## Problem 8: Stripe Terminal Connection Status

### Story

Stripe Terminal card readers must maintain a connection to the Stripe backend. You are writing a service to monitor their connection status.

### Input Format

  - A log of connection events, separated by `&`. Format: `timestamp;reader_id;event_type`.
  - `event_type`: `CONNECT`, `DISCONNECT`, `HEARTBEAT`.

### The Task

1.  **Last Seen Timestamp:** For each reader, determine the timestamp of its very last communication.
2.  **Current Connection Status:** Determine if each reader is `ONLINE` or `OFFLINE`.
3.  **Uptime Calculation:** Given a start and end timestamp, calculate the total time in seconds each reader was `ONLINE`.
4.  **Unreliable Readers Report:** An "unreliable" reader is one with more than 5 `DISCONNECT` events. Generate a list of all unreliable readers.

### Sample Input

```python
connection_log = "2025-05-01T09:00:00Z;rd_A;CONNECT&2025-05-01T09:05:00Z;rd_B;CONNECT&2025-05-01T09:10:00Z;rd_A;HEARTBEAT&2025-05-01T09:12:00Z;rd_B;DISCONNECT"
```

-----

## Problem 9: Transfer Reversal Tracking

### Story

When Stripe sends money to a user's bank account (a "transfer"), it can sometimes fail and be reversed. You need to track these reversals and update account balances.

### Input Format

  - A log of transfer and reversal events, separated by `|`. Format: `timestamp;event_type;transfer_id;account_id;amount`.
  - `event_type`: `TRANSFER_CREATED`, `TRANSFER_PAID`, `TRANSFER_FAILED`, `REVERSAL_CREATED`.

### The Task

1.  **Final Transfer Status:** For each `transfer_id`, determine its final status: `PAID`, `FAILED`, or `REVERSED`.
2.  **Balance Impact:** Calculate the final balance impact for each `account_id`. `TRANSFER_CREATED` debits the balance; `REVERSAL_CREATED` credits it back.
3.  **Reversal Latency:** For every reversed transfer, calculate the time in seconds between creation and reversal.
4.  **Account Risk Report:** A "high-risk" account is one where \>20% of its transfers were reversed. Generate a list of high-risk accounts.

### Sample Input

```python
transfer_log = "2025-06-01T10:00:00Z;TRANSFER_CREATED;tr_A;acct_1;5000|2025-06-02T10:00:00Z;TRANSFER_PAID;tr_A;acct_1;5000|2025-06-03T11:00:00Z;TRANSFER_CREATED;tr_B;acct_2;2000|2025-06-05T14:00:00Z;REVERSAL_CREATED;tr_B;acct_2;2000"
```

-----

## Problem 10: Inventory Management for a Merchant

### Story

A merchant using Stripe needs a simple inventory management system. You are building a service that processes orders and tracks product stock levels.

### Input Format

  - An initial inventory list, separated by `,`. Format: `product_id:initial_stock_level`.
  - A log of order events, separated by `~`. Format: `timestamp;order_id;product_id;quantity;event_type`.
  - `event_type`: `SALE`, `RETURN`.

### The Task

1.  **Items Sold:** Process only `SALE` events. For each product, calculate the total quantity sold.
2.  **Final Stock Levels:** Process all events chronologically. `SALE` decreases stock, `RETURN` increases it. Calculate final stock levels.
3.  **Out of Stock Check:** A `SALE` can only be fulfilled if there is sufficient stock at that moment. Re-calculate final stock levels with this new rule.
4.  **Fulfillment Report:** Generate a report mapping each `order_id` for a `SALE` to a status: `FULFILLED` or `INSUFFICIENT_STOCK`.

### Sample Input

```python
initial_inventory = "prod_A:100,prod_B:50"
order_log = "2025-07-10T10:00:00Z;ord_1;prod_A;10;SALE~2025-07-10T10:05:00Z;ord_2;prod_B;60;SALE~2025-07-11T11:00:00Z;ord_1;prod_A;2;RETURN"
```

-----

## Problem 11: Webhook Delivery Attempt Simulator

### Story

When an event occurs, Stripe sends a "webhook" notification to a user's server. If the server fails to respond, Stripe retries with an exponential backoff delay. You are building a simulator for this logic.

### Input Format

  - A list of webhook events to be sent, format: `event_id;url`.
  - Retry policy parameters: `initial_delay_seconds`, `max_retries`.
  - A log of server responses, separated by `&`. Format: `timestamp;event_id;http_status`. `200` is a success.

### The Task

1.  **Initial Delivery Status:** Determine if each event's *first* delivery attempt was a success or failure.
2.  **Retry Schedule:** For every event that initially failed, generate a schedule of when subsequent retries should have occurred.
3.  **Final Event Status:** Determine the final status for each event: `DELIVERED` or `FAILED`.
4.  **Unreliable Endpoints:** An "unreliable" `url` is one that failed to accept an event more than 3 times in a row for any single event. Identify all unreliable URLs.

### Sample Input

```python
events_to_send = ["evt_A;http://endpoint.com/a", "evt_B;http://endpoint.com/b"]
policy = {"initial_delay_seconds": 60, "max_retries": 3}
response_log = "2025-08-01T12:00:00Z;evt_A;503&2025-08-01T12:01:00Z;evt_A;503&2025-08-01T12:02:00Z;evt_B;200&2025-08-01T12:03:00Z;evt_A;200"
```

-----

## Problem 12: Stripe Sigma Query Planner

### Story

Stripe Sigma allows users to run SQL queries against their data. You are building a simplified query planner that determines which tables need to be joined to answer a query.

### Input Format

  - A dictionary of table schemas.
  - A query string, format: `SELECT field1,field2 FROM primary_table`.

### The Task

1.  **Field Existence Check:** Check if all selected fields exist in the `FROM` table.
2.  **Single Join Identification:** If a field is missing, find another table that contains it and can be joined (shares a common field).
3.  **Multi-Join Path:** Find the full set of all tables that must be included to fulfill the query.
4.  **Join Path Visualization:** Return the path of joins, e.g., `charges -> customers` (on `customer_id`).

### Sample Input

```python
schemas = {"charges": ["charge_id", "customer_id", "amount"], "customers": ["customer_id", "email"], "refunds": ["refund_id", "charge_id"]}
query = "SELECT email, refund_id FROM charges"
```

-----

## Problem 13: Top-Up Balance and Threshold Alerts

### Story

Some Stripe products require a user to maintain a "top-up" balance from which fees are deducted. You are building a monitoring service to send alerts when a balance drops below a threshold.

### Input Format

  - A log of balance-affecting events, separated by `|`. Format: `timestamp;account_id;type;amount`.
  - `type`: `TOP_UP` (adds), `FEE` (subtracts).
  - An `alert_threshold` value.

### The Task

1.  **Final Balances:** Process all events and calculate the final balance for each account.
2.  **Balance History:** For a specific account, return its entire balance history (timestamp and balance after each event).
3.  **Threshold Alert Generation:** Identify every time an account's balance **crosses** the threshold from above to below. Return a list of all alerts.
4.  **"At Risk" Report:** An account is "at risk" if it has dropped below the threshold more than twice. Generate a list of all "at risk" accounts.

### Sample Input

```python
balance_log = "2025-09-01T10:00:00Z;acct_A;TOP_UP;10000|2025-09-02T11:00:00Z;acct_A;FEE;3000|2025-09-03T12:00:00Z;acct_A;FEE;3000"
alert_threshold = 5000
```

-----

## Problem 14: Automated Subscription Tier Assignment

### Story

You are building a service for a SaaS company that automatically assigns users to subscription tiers ('Bronze', 'Silver', 'Gold') based on their monthly usage.

### Input Format

  - A definition of tier boundaries, format: `Bronze:0,Silver:1000,Gold:5000`.
  - A log of daily usage events, separated by `&`. Format: `date;customer_id;usage_amount`.

### The Task

1.  **Total Monthly Usage:** For a given month, calculate the total `usage_amount` for each customer.
2.  **Tier Assignment:** Determine the correct subscription tier for each customer for that month.
3.  **Tier Change Notifications:** Compare the assigned tier for the current month to the previous month. Generate a notification for any customer whose tier has changed.
4.  **Projected Tier Calculation:** Halfway through the current month, calculate each customer's *projected* total monthly usage (assume usage rate is constant) and determine their "projected tier".

### Sample Input

```python
tier_boundaries = "Bronze:0,Silver:1000,Gold:5000"
usage_log = "2025-01-10;cust_A;600&2025-01-12;cust_B;30&2025-01-15;cust_A;100"
```