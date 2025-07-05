Design a global payment-processing system that ensures low latency (≤100 ms) and high availability across regions.

Design a subscription billing system supporting proration, mid-cycle plan changes, and invoicing.

Design a real-time fraud-detection system for transactions (extract features, ML scoring, <100 ms response).

Design a rate limiter for Stripe’s API using distributed token-bucket/leaky-bucket pattern.

Design a multi-tenant architecture for Stripe Billing, covering data isolation, scalability, and security.

Build a notification/webhook system for payment events—ensure reliable scheduling, retries, idempotency, and dead letter handling.

Design retry mechanisms for transient payment failures, e.g. payment gateway timeouts.

Explain eventual consistency in a billing system and where it can/cannot be used.

Design a system to handle refunds and chargebacks, ensuring state consistency and merchants’ notifications.

Design a ledger or accounting system to track charges, credits, and balance updates for vendors.

Obscure or blur credit-card data in logs while preserving enough context for debugging.

Design a usage-based billing system that efficiently collects and bills per-unit usage metrics.

Design a webhook subscription platform where merchants can register endpoints and receive events reliably.

Design an identity/access-management system (IAM) for internal Stripe tools and APIs (RBAC, token lifecycles, audit logs).

Design a secure data pipeline for fraud feature data, covering ingestion, transformation, storage, and analytics.

Design a dashboard metrics system aggregating real-time payment and subscription data.

Design a disaster recovery plan for Stripe’s billing system across multiple regions.

Design a billing retry system for failed recurring charges (e.g., retry logic, notifications, dunning).

Design dynamic API throttling per merchant/customer to prevent abuse.

Explain and design idempotent payment APIs, covering how you achieve safe retries and consistency.