from fastapi import Depends, FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .config import Settings, get_settings
from .schemas import AnalyzeAspMetricsRequest, ClassifyWalletTransactionsRequest, GenerateReceiptRequest, GenerateRevenueReportRequest
from .service import analyze_asp_metrics, classify_wallet_transactions, generate_receipt, generate_revenue_report
from .storage import LedgerStore

app = FastAPI(title="Agent CFO", version="0.1.0", description="Revenue intelligence and traction reports for OKX.AI ASPs.")

settings = get_settings()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if settings.cors_origins == "*" else [item.strip() for item in settings.cors_origins.split(",")],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
store = LedgerStore(settings.data_dir)


def require_api_key(x_api_key: str | None = Header(default=None), config: Settings = Depends(get_settings)) -> None:
    if config.api_key and x_api_key != config.api_key:
        raise HTTPException(status_code=401, detail="Invalid or missing API key.")


def persist(record: dict) -> dict:
    store.insert(record["id"], record.get("kind", "record"), record)
    return record


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "service": "agent-cfo", "mode": "A2MCP"}


@app.get("/mcp")
def mcp_manifest() -> dict:
    return {
        "name": "Agent CFO",
        "version": "0.1.0",
        "service_mode": "A2MCP",
        "tools": [
            {"name": "generate_revenue_report", "endpoint": "/tools/generate_revenue_report"},
            {"name": "classify_wallet_transactions", "endpoint": "/tools/classify_wallet_transactions"},
            {"name": "generate_receipt", "endpoint": "/tools/generate_receipt"},
            {"name": "analyze_asp_metrics", "endpoint": "/tools/analyze_asp_metrics"},
        ],
    }


@app.post("/tools/classify_wallet_transactions", dependencies=[Depends(require_api_key)])
def tool_classify_wallet_transactions(payload: ClassifyWalletTransactionsRequest) -> dict:
    return persist(classify_wallet_transactions(payload))


@app.post("/tools/generate_revenue_report", dependencies=[Depends(require_api_key)])
def tool_generate_revenue_report(payload: GenerateRevenueReportRequest) -> dict:
    return persist(generate_revenue_report(payload))


@app.post("/tools/generate_receipt", dependencies=[Depends(require_api_key)])
def tool_generate_receipt(payload: GenerateReceiptRequest) -> dict:
    return persist(generate_receipt(payload))


@app.post("/tools/analyze_asp_metrics", dependencies=[Depends(require_api_key)])
def tool_analyze_asp_metrics(payload: AnalyzeAspMetricsRequest) -> dict:
    return persist(analyze_asp_metrics(payload))


@app.get("/history", dependencies=[Depends(require_api_key)])
def history(limit: int = 50) -> dict:
    return {"items": store.list_recent(limit=limit)}


@app.get("/demo")
def demo() -> dict:
    return {
        "classification": {
            "endpoint": "/tools/classify_wallet_transactions",
            "payload": {
                "wallet_address": "0xseller",
                "chain_id": 196,
                "known_asp_ids": ["asp_workproof"],
                "transactions": [
                    {"tx_hash": "0xrev1", "direction": "in", "amount": 1.25, "memo": "paid call revenue", "currency": "USDT"},
                    {"tx_hash": "0xcost1", "direction": "out", "amount": 0.2, "memo": "model api cost", "currency": "USDT"},
                    {"tx_hash": "0xref1", "direction": "out", "amount": 0.1, "memo": "refund", "currency": "USDT"},
                ],
            },
        }
    }

