"""
schemas.py - Modelos Pydantic para la API REST.
"""

from __future__ import annotations

from pydantic import BaseModel, Field


class TextInput(BaseModel):
    text: str = Field(
        ...,
        min_length=3,
        max_length=5000,
        description="Texto en espanol a clasificar.",
    )


class PredictionResponse(BaseModel):
    text: str
    sentiment: str
    confidence: float
    app_version: str


class MetricsResponse(BaseModel):
    accuracy: float
    f1_weighted: float
    confusion_matrix: list[list[int]]
    labels: list[str]
    tracked_predictions: int


class HealthResponse(BaseModel):
    status: str
    artifacts_loaded: bool
    database_ready: bool
    version: str


class HistoryItem(BaseModel):
    id: int
    text: str
    clean_text: str
    sentiment: str
    confidence: float
    created_at: str


class HistoryResponse(BaseModel):
    items: list[HistoryItem]
