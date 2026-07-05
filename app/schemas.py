from typing import Literal

from pydantic import BaseModel, Field


Category = Literal[
    "revenue",
    "refund",
    "escrow_release",
    "arbitration_deposit",
    "service_cost",
    "model_api_cost",
    "cloud_cost",
    "marketing_cost",
    "withdrawal",
    "internal_transfer",
    "unknown",
]


class TransactionInput(BaseModel):
    tx_hash: str
    wallet_address: str | None = None
    counterparty: str | None = None
    direction: Literal["in", "out"] = "in"
    amount: float
    currency: str = "USDT"
    memo: str = ""
    service_id: str | None = None
    asp_id: str | None = None
    timestamp: str | None = None


class ClassifyWalletTransactionsRequest(BaseModel):
    wallet_address: str
    chain_id: int = 196
    tx_hashes: list[str] = Field(default_factory=list)
    known_asp_ids: list[str] = Field(default_factory=list)
    transactions: list[TransactionInput] = Field(default_factory=list)


class LedgerEntry(BaseModel):
    entry_id: str
    tx_hash: str
    asp_id: str | None = None
    service_id: str | None = None
    category: Category
    amount: float
    currency: str
    usd_value: float
    confidence: float
    notes: str


class GenerateRevenueReportRequest(BaseModel):
    asp_id: str
    period_start: str
    period_end: str
    report_type: str = "hackathon_revenue_rocket"
    include_evidence: bool = True
    ledger_entries: list[LedgerEntry] = Field(default_factory=list)


class GenerateReceiptRequest(BaseModel):
    payment_id: str
    buyer_wallet: str
    seller_wallet: str
    service_name: str
    amount: float
    currency: str = "USDT"
    tx_hash: str
    timestamp: str | None = None


class AnalyzeAspMetricsRequest(BaseModel):
    asp_id: str
    metrics: list[str] = Field(default_factory=lambda: ["revenue", "orders", "reviews", "failed_calls", "repeat_users"])
    period: str = "last_14_days"
    ledger_entries: list[LedgerEntry] = Field(default_factory=list)
    reviews: list[float] = Field(default_factory=list)
    failed_calls: int = 0
    repeat_users: int = 0
    unique_users: int = 0

