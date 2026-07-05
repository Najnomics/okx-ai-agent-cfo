# Agent CFO Specification

## 1. Summary

Agent CFO is the financial operating layer for OKX.AI ASP businesses. It tracks revenue, orders, calls, reviews, costs, refunds, disputes, wallet transactions, and traction. It generates dashboards, receipts, grant reports, and investor updates.

## 2. Goals

- Help builders prove hackathon traction.
- Organize ASP payment and usage records.
- Generate Revenue Rocket reports.
- Create receipts for paid calls/orders.
- Provide clear metrics without giving tax/legal advice.

## 3. Non-Goals

- Agent CFO is not tax filing software.
- Agent CFO does not provide legal, tax, or investment advice.
- MVP does not require direct OKX.AI private APIs if unavailable.

## 4. Users

| User | Need |
|---|---|
| ASP builder | Track revenue, orders, reviews, and costs. |
| Hackathon team | Prove traction and revenue. |
| Investor/grant reviewer | Read clean evidence-backed updates. |
| Multi-ASP operator | Compare services and margins. |

## 5. Service Modes

| Capability | Mode |
|---|---|
| `generate_revenue_report` | A2MCP |
| `classify_wallet_transactions` | A2MCP |
| `generate_receipt` | A2MCP |
| `analyze_asp_metrics` | A2MCP |
| custom investor/grant report | A2A |
| finance ops setup | A2A |

## 6. Public API

### 6.1 `generate_revenue_report`

```json
{
  "asp_id": "asp_456",
  "period_start": "2026-07-01",
  "period_end": "2026-07-17",
  "report_type": "hackathon_revenue_rocket",
  "include_evidence": true
}
```

### 6.2 `classify_wallet_transactions`

```json
{
  "wallet_address": "0xabc...",
  "chain_id": 196,
  "tx_hashes": ["0x1...", "0x2..."],
  "known_asp_ids": ["asp_456"]
}
```

### 6.3 `generate_receipt`

```json
{
  "payment_id": "pay_123",
  "buyer_wallet": "0xbuyer...",
  "seller_wallet": "0xseller...",
  "service_name": "WorkProof Lead Verification",
  "amount": "0.50",
  "currency": "USDT",
  "tx_hash": "0x..."
}
```

### 6.4 `analyze_asp_metrics`

```json
{
  "asp_id": "asp_456",
  "metrics": ["revenue", "orders", "reviews", "failed_calls", "repeat_users"],
  "period": "last_14_days"
}
```

## 7. Core Components

### 7.1 Data Ingestion

Sources:

- OKX.AI order/call records when available.
- OKX Payment SDK events.
- X Layer transaction logs.
- Wallet exports.
- Manual CSV imports.
- ASP endpoint usage logs.
- Reviews and ratings.
- Model/API/cloud costs.

### 7.2 Transaction Indexer

- Poll chain RPC or indexing provider.
- Track configured wallets.
- Decode payment events.
- Store raw events separately from classified ledger entries.

### 7.3 Entity Resolver

Maps:

```text
wallet address -> agent -> ASP -> service -> order -> customer
```

Uncertain mappings are marked as unresolved.

### 7.4 Transaction Classifier

Categories:

```text
revenue
refund
escrow_release
arbitration_deposit
service_cost
model_api_cost
cloud_cost
marketing_cost
withdrawal
internal_transfer
unknown
```

### 7.5 Internal Ledger

Maintains normalized records for business reporting.

### 7.6 Metrics Engine

Core metrics:

- gross revenue.
- net revenue.
- orders.
- paid calls.
- average revenue per order.
- repeat user rate.
- refund rate.
- dispute rate.
- gross margin estimate.
- review score.

### 7.7 Report Generator

Report types:

- Revenue Rocket Report.
- Grant Report.
- Investor Update.
- Receipt/Invoice.

## 8. Data Model

```sql
CREATE TABLE wallets (
  id UUID PRIMARY KEY,
  owner_agent_id TEXT,
  address TEXT,
  chain_id INT,
  label TEXT,
  created_at TIMESTAMP
);

CREATE TABLE raw_transactions (
  id UUID PRIMARY KEY,
  chain_id INT,
  tx_hash TEXT,
  log_index INT,
  wallet_address TEXT,
  raw_json JSONB,
  block_time TIMESTAMP,
  UNIQUE(chain_id, tx_hash, log_index)
);

CREATE TABLE ledger_entries (
  id UUID PRIMARY KEY,
  raw_transaction_id UUID REFERENCES raw_transactions(id),
  asp_id TEXT,
  service_id TEXT,
  category TEXT,
  amount NUMERIC,
  currency TEXT,
  usd_value NUMERIC,
  confidence NUMERIC,
  notes TEXT,
  created_at TIMESTAMP
);

CREATE TABLE reports (
  id UUID PRIMARY KEY,
  owner_agent_id TEXT,
  report_type TEXT,
  period_start DATE,
  period_end DATE,
  storage_uri TEXT,
  content_hash TEXT,
  created_at TIMESTAMP
);
```

## 9. MVP Scope

- Manual wallet/transaction import.
- Basic X Layer transaction polling if available.
- Revenue/cost/refund classification.
- Simple dashboard.
- Receipt generator.
- Hackathon traction report generator.

## 10. V1 Scope

- OKX.AI order/review integration.
- Full payment event ingestion.
- Investor update generator.
- Multi-ASP portfolio dashboard.
- Pricing recommendations.
- Team access.

## 11. Security Requirements

- Do not store private keys.
- Never request seed phrases.
- Store raw transactions separately.
- Mark uncertain classifications.
- Avoid tax/legal advice claims.
- Hash generated reports.

## 12. Hackathon Milestones

| Day | Target |
|---|---|
| 1 | Data model and sample imports. |
| 2 | Transaction classifier. |
| 3 | Metrics engine. |
| 4 | Dashboard. |
| 5 | Receipt generator. |
| 6 | Revenue Rocket report. |
| 7 | Demo and submission polish. |

