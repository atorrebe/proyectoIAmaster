"""
router.py — Endpoints REST de la API de análisis de sentimiento.
"""

import json
import os
from fastapi import APIRouter, HTTPException
from src.api.schemas import TextInput, PredictionResponse, MetricsResponse, HealthResponse
from src.pipeline.predict import predict

router = APIRouter()

METRICS_PATH = os.path.join("models", "metrics.json")


@router.get("/health", response_model=HealthResponse, tags=["Sistema"])
def health():
    model_path = os.path.join("models", "sentiment_model.joblib")
    model_loaded = os.path.exists(model_path)
    return HealthResponse(
        status="ok",
        model_loaded=model_loaded,
        version="1.0.0",
    )


@router.post("/predict", response_model=PredictionResponse, tags=["Predicción"])
def predict_sentiment(body: TextInput):
    try:
        sentiment, confidence = predict(body.text)
    except FileNotFoundError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")
    return PredictionResponse(
        text=body.text,
        sentiment=sentiment,
        confidence=confidence,
    )


@router.get("/metrics", response_model=MetricsResponse, tags=["Evaluación"])
def get_metrics():
    if not os.path.exists(METRICS_PATH):
        raise HTTPException(
            status_code=404,
            detail="Métricas no disponibles. Entrena el modelo primero con train.py.",
        )
    with open(METRICS_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    return MetricsResponse(
        accuracy=data["accuracy"],
        f1_weighted=data["f1_weighted"],
        confusion_matrix=data["confusion_matrix"],
        labels=data["labels"],
    )