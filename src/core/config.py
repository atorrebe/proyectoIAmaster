from __future__ import annotations

import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]
SRC_DIR = BASE_DIR / "src"
FRONTEND_DIR = SRC_DIR / "frontend"
MODELS_DIR = BASE_DIR / "models"
DATA_DIR = BASE_DIR / "data"
DOCS_DIR = BASE_DIR / "docs"

APP_NAME = "SentimentAI"
APP_VERSION = "1.1.0"
API_PREFIX = "/api/v1"


def _split_env(name: str, default: list[str]) -> list[str]:
    raw_value = os.getenv(name, "")
    if not raw_value.strip():
        return default
    return [item.strip() for item in raw_value.split(",") if item.strip()]


ALLOWED_ORIGINS = _split_env(
    "ALLOW_ORIGINS",
    [
        "http://127.0.0.1:8000",
        "http://localhost:8000",
    ],
)
ALLOWED_HOSTS = _split_env(
    "ALLOW_HOSTS",
    [
        "127.0.0.1",
        "localhost",
        "testserver",
    ],
)

DATABASE_PATH = Path(os.getenv("PREDICTIONS_DB_PATH", DATA_DIR / "predictions.db"))
MODEL_PATH = MODELS_DIR / "sentiment_model.joblib"
VECTORIZER_PATH = MODELS_DIR / "tfidf_vectorizer.joblib"
METRICS_PATH = MODELS_DIR / "metrics.json"
EXPORT_FILENAME = "predictions_export.csv"

MAX_HISTORY_ITEMS = int(os.getenv("MAX_HISTORY_ITEMS", "100"))
