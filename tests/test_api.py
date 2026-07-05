from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_classifies_revenue() -> None:
    response = client.post(
        "/tools/classify_wallet_transactions",
        json={
            "wallet_address": "0xseller",
            "known_asp_ids": ["asp_demo"],
            "transactions": [{"tx_hash": "0x1", "direction": "in", "amount": 2.5, "memo": "paid call revenue", "currency": "USDT"}],
        },
    )
    assert response.status_code == 200
    entry = response.json()["entries"][0]
    assert entry["category"] == "revenue"
    assert entry["confidence"] >= 0.9


def test_generates_receipt() -> None:
    response = client.post(
        "/tools/generate_receipt",
        json={
            "payment_id": "pay_1",
            "buyer_wallet": "0xbuyer",
            "seller_wallet": "0xseller",
            "service_name": "WorkProof",
            "amount": 0.5,
            "currency": "USDT",
            "tx_hash": "0xtx",
        },
    )
    assert response.status_code == 200
    assert response.json()["content_hash"].startswith("0x")


def test_analyzes_metrics() -> None:
    entry = {
        "entry_id": "led_1",
        "tx_hash": "0x1",
        "asp_id": "asp_demo",
        "category": "revenue",
        "amount": 2,
        "currency": "USDT",
        "usd_value": 2,
        "confidence": 0.9,
        "notes": "demo",
    }
    response = client.post("/tools/analyze_asp_metrics", json={"asp_id": "asp_demo", "ledger_entries": [entry], "reviews": [5, 4]})
    assert response.status_code == 200
    body = response.json()
    assert body["metrics"]["gross_revenue"] == 2
    assert body["metrics"]["review_score"] == 4.5

