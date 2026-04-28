from __future__ import annotations

import json
import os
from pathlib import Path

from fastapi.testclient import TestClient


def build_client(tmp_path: Path):
    os.environ["PREDICTIONS_DB_PATH"] = str(tmp_path / "predictions.db")

    from src.core import config
    from src.api.main import app
    from src.services import storage

    config.DATABASE_PATH = tmp_path / "predictions.db"
    storage.DATABASE_PATH = config.DATABASE_PATH
    storage.initialize_db()
    return TestClient(app)


def write_metrics_file(base_dir: Path) -> None:
    metrics_path = base_dir / "models" / "metrics.json"
    metrics_path.parent.mkdir(parents=True, exist_ok=True)
    metrics_path.write_text(
        json.dumps(
            {
                "accuracy": 0.81,
                "f1_weighted": 0.8,
                "confusion_matrix": [[3, 0, 0], [0, 2, 1], [0, 1, 4]],
                "labels": ["negativo", "neutro", "positivo"],
            }
        ),
        encoding="utf-8",
    )


def test_health_endpoint_reports_status(tmp_path: Path):
    client = build_client(tmp_path)
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"
    assert payload["database_ready"] is True
    assert "artifacts_loaded" in payload


def test_predict_endpoint_persists_prediction(tmp_path: Path, monkeypatch):
    client = build_client(tmp_path)

    def fake_predict(_: str):
        return "positivo", 0.97, "producto genial"

    monkeypatch.setattr("src.api.router.predict", fake_predict)
    response = client.post("/api/v1/predict", json={"text": "Producto genial"})

    assert response.status_code == 200
    payload = response.json()
    assert payload["sentiment"] == "positivo"
    assert payload["confidence"] == 0.97

    history = client.get("/api/v1/history?limit=5")
    history_payload = history.json()
    assert len(history_payload["items"]) == 1
    assert history_payload["items"][0]["clean_text"] == "producto genial"


def test_metrics_endpoint_returns_saved_metrics(tmp_path: Path):
    write_metrics_file(Path(__file__).resolve().parents[1])
    client = build_client(tmp_path)
    response = client.get("/api/v1/metrics")
    assert response.status_code == 200
    payload = response.json()
    assert payload["accuracy"] == 0.81
    assert payload["labels"] == ["negativo", "neutro", "positivo"]


def test_export_endpoint_returns_csv(tmp_path: Path, monkeypatch):
    client = build_client(tmp_path)

    def fake_predict(_: str):
        return "neutro", 0.55, "texto normalizado"

    monkeypatch.setattr("src.api.router.predict", fake_predict)
    client.post("/api/v1/predict", json={"text": "Texto para exportar"})

    response = client.get("/api/v1/export")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/csv")
    assert "texto normalizado" in response.text
