"""
schemas.py — Modelos Pydantic para la API REST.
"""

from pydantic import BaseModel, Field
from typing import Optional


class TextInput(BaseModel):
    text: str = Field(
        ...,
        min_length=3,
        max_length=5000,
        description="Texto en español a clasificar.",
    )


class PredictionResponse(BaseModel):
    text: str
    sentiment: str
    confidence: float


class MetricsResponse(BaseModel):
    accuracy: float
    f1_weighted: float
    confusion_matrix: list
    labels: list


class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
    version: str = "1.0.0"