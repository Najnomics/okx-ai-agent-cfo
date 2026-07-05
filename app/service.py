import hashlib
import json
import re
from typing import Any
from uuid import uuid4

from .schemas import (
    AnalyzeAspMetricsRequest,
    Category,
    ClassifyWalletTransactionsRequest,
    GenerateReceiptRequest,
    GenerateRevenueReportRequest,
    LedgerEntry,
    TransactionInput,
)


def stable_hash(payload: Any) -> str:
    return "0x" + hashlib.sha256(json.dumps(payload, sort_keys=True, default=str).encode()).hexdigest()


def classify_category(tx: TransactionInput) -> tuple[Category, float, str]:
    memo = tx.memo.lower()
    if tx.direction == "in" and any(term in memo for term in ["revenue", "payment", "paid call", "order", "escrow release"]):
        if "escrow" in memo:
            return "escrow_release", 0.93, "Inbound escrow release detected from memo."
        return "revenue", 0.92, "Inbound ASP payment/revenue detected from memo."
    if tx.direction == "out" and "refund" in memo:
        return "refund", 0.9, "Outbound refund detected from memo."
    if "arbitration" in memo:
        return "arbitration_deposit", 0.86, "Arbitration deposit detected from memo."
    if tx.direction == "out" and any(term in memo for term in ["model", "openai", "anthropic", "api"]):
        return "model_api_cost", 0.82, "Model/API service cost detected from memo."
    if tx.direction == "out" and any(term in memo for term in ["cloud", "server", "hosting", "render", "railway"]):
        return "cloud_cost", 0.82, "Cloud or hosting cost detected from memo."
    if tx.direction == "out" and "marketing" in memo:
        return "marketing_cost", 0.8, "Marketing cost detected from memo."
    if tx.direction == "out" and "withdraw" in memo:
        return "withdrawal", 0.75, "Withdrawal detected from memo."
    if tx.direction == "out":
        return "service_cost", 0.55, "Outbound transaction treated as possible service cost."
    return "unknown", 0.45, "Insufficient memo/context to classify confidently."


def classify_wallet_transactions(payload: ClassifyWalletTransactionsRequest) -> dict[str, Any]:
    transactions = payload.transactions or [
        TransactionInput(tx_hash=tx_hash, wallet_address=payload.wallet_address, amount=0, memo="unresolved", direction="in")
        for tx_hash in payload.tx_hashes
    ]
    entries: list[LedgerEntry] = []
    for tx in transactions:
        category, confidence, notes = classify_category(tx)
        usd_value = tx.amount if tx.currency.upper() in {"USDT", "USDC", "USD"} else tx.amount
        entries.append(
            LedgerEntry(
                entry_id=f"led_{uuid4().hex[:12]}",
                tx_hash=tx.tx_hash,
                asp_id=tx.asp_id or (payload.known_asp_ids[0] if payload.known_asp_ids else None),
                service_id=tx.service_id,
                category=category,
                amount=tx.amount,
                currency=tx.currency,
                usd_value=usd_value,
                confidence=confidence,
                notes=notes,
            )
        )
    return {
        "id": f"classification_{uuid4().hex[:12]}",
        "kind": "classification",
        "wallet_address": payload.wallet_address,
        "chain_id": payload.chain_id,
        "entries": [entry.model_dump() for entry in entries],
        "evidence_hash": stable_hash([entry.model_dump() for entry in entries]),
    }


def metrics_from_entries(entries: list[LedgerEntry]) -> dict[str, float]:
    gross_revenue = sum(entry.usd_value for entry in entries if entry.category in {"revenue", "escrow_release"})
    refunds = sum(entry.usd_value for entry in entries if entry.category == "refund")
    costs = sum(entry.usd_value for entry in entries if entry.category in {"service_cost", "model_api_cost", "cloud_cost", "marketing_cost"})
    paid_calls = sum(1 for entry in entries if entry.category in {"revenue", "escrow_release"})
    return {
        "gross_revenue": round(gross_revenue, 2),
        "net_revenue": round(gross_revenue - refunds, 2),
        "costs": round(costs, 2),
        "gross_margin_estimate": round(gross_revenue - refunds - costs, 2),
        "paid_calls": paid_calls,
        "refunds": round(refunds, 2),
    }


def generate_revenue_report(payload: GenerateRevenueReportRequest) -> dict[str, Any]:
    metrics = metrics_from_entries(payload.ledger_entries)
    evidence = [entry.tx_hash for entry in payload.ledger_entries] if payload.include_evidence else []
    return {
        "id": f"report_{uuid4().hex[:12]}",
        "kind": "revenue_report",
        "asp_id": payload.asp_id,
        "period_start": payload.period_start,
        "period_end": payload.period_end,
        "report_type": payload.report_type,
        "metrics": metrics,
        "summary": f"{payload.asp_id} generated {metrics['gross_revenue']} USD gross revenue and {metrics['paid_calls']} paid call(s) in the selected period.",
        "evidence": evidence,
        "content_hash": stable_hash({"metrics": metrics, "evidence": evidence}),
    }


def generate_receipt(payload: GenerateReceiptRequest) -> dict[str, Any]:
    receipt = {
        "id": f"receipt_{uuid4().hex[:12]}",
        "kind": "receipt",
        "payment_id": payload.payment_id,
        "buyer_wallet": payload.buyer_wallet,
        "seller_wallet": payload.seller_wallet,
        "service_name": payload.service_name,
        "amount": payload.amount,
        "currency": payload.currency,
        "tx_hash": payload.tx_hash,
        "timestamp": payload.timestamp,
    }
    receipt["content_hash"] = stable_hash(receipt)
    return receipt


def analyze_asp_metrics(payload: AnalyzeAspMetricsRequest) -> dict[str, Any]:
    metrics = metrics_from_entries(payload.ledger_entries)
    review_score = round(sum(payload.reviews) / len(payload.reviews), 2) if payload.reviews else None
    conversion_notes = []
    if payload.failed_calls > 0:
        conversion_notes.append(f"{payload.failed_calls} failed call(s) need inspection.")
    if payload.unique_users:
        repeat_rate = round(payload.repeat_users / payload.unique_users, 2)
    else:
        repeat_rate = 0
    return {
        "id": f"metrics_{uuid4().hex[:12]}",
        "kind": "metrics",
        "asp_id": payload.asp_id,
        "period": payload.period,
        "metrics": {**metrics, "review_score": review_score, "failed_calls": payload.failed_calls, "repeat_user_rate": repeat_rate},
        "recommendations": conversion_notes or ["Ask satisfied users for reviews after PASS results.", "Track model/API costs per service to improve margin accuracy."],
        "evidence_hash": stable_hash({"entries": [entry.model_dump() for entry in payload.ledger_entries], "reviews": payload.reviews}),
    }

