# Agent CFO

Agent CFO is the revenue intelligence and traction-reporting layer for OKX.AI Agent Service Provider businesses.

It tracks revenue, orders, paid calls, reviews, costs, refunds, disputes, wallet transactions, and campaign metrics.

## OKX.AI Genesis Hackathon Fit

- Category: Finance Copilot / Revenue Rocket support
- Service mode: A2MCP for reports and receipts, A2A for custom investor/grant reporting
- Core value: helps ASP builders prove traction and understand their business
- Demo target: import sample X Layer/OKX.AI payments and generate a Revenue Rocket report

Hackathon notes:

- Campaign: OKX.AI Genesis, part of the X Layer Build X series.
- Build goal: create an Agent Service Provider that solves a clear real-world use case.
- Submission flow: list the ASP on OKX.AI, post a short X walkthrough with `#OKXAI`, then submit the project form before the deadline.
- Official context: https://www.okx.com/xlayer/build-x-hackathon

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
- `app/` - FastAPI service implementation
- `tests/` - API tests
- `Dockerfile` - production container
- `okx-ai-listing.md` - marketplace listing draft
- `DEMO_SCRIPT.md` - 90-second walkthrough script

## Run Locally

```bash
uv run uvicorn app.main:app --reload
```

Then open:

- API docs: `http://127.0.0.1:8000/docs`
- MCP-style manifest: `http://127.0.0.1:8000/mcp`
- Demo payloads: `http://127.0.0.1:8000/demo`

## Test

```bash
uv run --extra dev pytest
```

## Production Notes

- Set `AGENT_CFO_API_KEY` before exposing paid endpoints.
- Deploy behind HTTPS before OKX.AI registration.
- Use `AGENT_CFO_DATA_DIR` for persistent SQLite report storage.
- Agent CFO organizes records and reports; it does not provide legal, tax, or investment advice.

## Contributor

- eosadolor382@gmail.com

## Status

Production-shaped MVP: transaction classifier, metrics engine, receipt generator, report generator, persistence, tests, Dockerfile, listing copy, and demo script are implemented.
