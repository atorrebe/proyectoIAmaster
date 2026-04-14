"""
schemas.py — Modelos de datos (esquemas Pydantic) para la API REST.

Define las estructuras de entrada y salida de los endpoints. """

from pydantic import BaseModel, Field from typing import Optional


class TextInput(BaseModel):
"""Cuerpo de la petición POST /predict.""" text: str = Field(
...,
min_length=3, max_length=5000,
description="Texto en español a clasificar.",
example="El producto llegó en perfecto estado y supera mis expectativas.",
)


class PredictionResponse(BaseModel): """Respuesta del endpoint POST /predict."""
text: str = Field(..., description="Texto original recibido.") sentiment: str = Field(
...,
description="Categoría predicha: 'positivo', 'neutro' o 'negativo'.",
)
confidence: float = Field(
..., ge=0.0,

le=1.0,
description="Probabilidad asociada a la predicción (0.0 – 1.0).",
)


class MetricsResponse(BaseModel):
"""Respuesta del endpoint GET /metrics.""" accuracy: float
f1_weighted: float confusion_matrix: list labels: list


class HealthResponse(BaseModel):
"""Respuesta del endpoint GET /health.""" status: str
model_loaded: bool version: str = "1.0.0"
