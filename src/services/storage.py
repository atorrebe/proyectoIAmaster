from __future__ import annotations

import csv
import io
import sqlite3
from pathlib import Path

from src.core.config import DATABASE_PATH


def _connect() -> sqlite3.Connection:
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_db() -> None:
    with _connect() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS predictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT NOT NULL,
                clean_text TEXT NOT NULL,
                sentiment TEXT NOT NULL,
                confidence REAL NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )


def save_prediction(text: str, clean_text: str, sentiment: str, confidence: float) -> None:
    with _connect() as connection:
        connection.execute(
            """
            INSERT INTO predictions (text, clean_text, sentiment, confidence)
            VALUES (?, ?, ?, ?)
            """,
            (text, clean_text, sentiment, confidence),
        )


def fetch_recent_predictions(limit: int) -> list[dict[str, object]]:
    with _connect() as connection:
        rows = connection.execute(
            """
            SELECT id, text, clean_text, sentiment, confidence, created_at
            FROM predictions
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()
    return [dict(row) for row in rows]


def count_predictions() -> int:
    with _connect() as connection:
        row = connection.execute("SELECT COUNT(*) AS total FROM predictions").fetchone()
    return int(row["total"]) if row else 0


def export_predictions_csv() -> str:
    rows = fetch_recent_predictions(limit=10000)
    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow(["id", "text", "clean_text", "sentiment", "confidence", "created_at"])
    for row in rows:
        writer.writerow(
            [
                row["id"],
                row["text"],
                row["clean_text"],
                row["sentiment"],
                row["confidence"],
                row["created_at"],
            ]
        )
    return buffer.getvalue()


def database_ready() -> bool:
    return Path(DATABASE_PATH).exists()
