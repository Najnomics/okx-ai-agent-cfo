# Agent CFO

Agent CFO is the revenue intelligence and traction-reporting layer for OKX.AI Agent Service Provider businesses.

It tracks revenue, orders, paid calls, reviews, costs, refunds, disputes, wallet transactions, and campaign metrics.

## OKX.AI Genesis Hackathon Fit

- Category: Finance Copilot / Revenue Rocket support
- Service mode: A2MCP for reports and receipts, A2A for custom investor/grant reporting
- Core value: helps ASP builders prove traction and understand their business
- Demo target: import sample X Layer/OKX.AI payments and generate a Revenue Rocket report

## Problem

Hackathon builders need to prove usage, revenue, and reviews quickly. ASP businesses also need organized records, receipts, and simple financial visibility without pretending to be full accounting software.

## MVP Tools

### `generate_revenue_report`

Creates a hackathon traction report for a selected period.

### `classify_wallet_transactions`

Classifies wallet events as revenue, refund, escrow release, cost, internal transfer, or unknown.

### `generate_receipt`

Creates a receipt with buyer wallet, seller wallet, service, amount, timestamp, and transaction hash.

### `analyze_asp_metrics`

Summarizes revenue, orders, reviews, failed calls, repeat users, and conversion.

## Architecture

```text
ASP Builder
  -> Agent CFO API / Dashboard
  -> Wallet / Payment Import
  -> Transaction Classifier
  -> Internal Ledger
  -> Metrics Engine
  -> Report Generator
  -> Receipts / Revenue Rocket Report
```

## Hackathon Demo

1. Show ASP receiving paid calls.
2. Agent CFO imports sample transactions.
3. Dashboard shows revenue, orders, reviews, and failed calls.
4. Generate Revenue Rocket report.
5. Export receipt and investor-style update.

## Repository Contents

- `spec.md` - full product and technical specification
- `README.md` - project overview and hackathon framing

## Contributor

- eosadolor382@gmail.com

## Status

Hackathon planning repository. Implementation scaffold will add importers, classifier, dashboard, receipt generation, and reports.

