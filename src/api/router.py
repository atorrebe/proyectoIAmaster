"""
router.py - Endpoints REST de la API de analisis de sentimiento.
"""

from __future__ import annotations

import json
from io import StringIO

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import StreamingResponse

from src.api.schemas import HealthResponse, HistoryResponse, MetricsResponse, PredictionResponse, TextInput
from src.core.config import APP_VERSION, EXPORT_FILENAME, MAX_HISTORY_ITEMS, METRICS_PATH, MODEL_PATH
from src.pipeline.predict import predict
from src.services.storage import (
    count_predictions,
    database_ready,
    export_predictions_csv,
    fetch_recent_predictions,
    save_prediction,
)


router = APIRouter()


@router.get("/health", response_model=HealthResponse, tags=["Sistema"])
def health() -> HealthResponse:
    return HealthResponse(
        status="ok",
        artifacts_loaded=MODEL_PATH.exists(),
        database_ready=database_ready(),
        version=APP_VERSION,
    )


@router.post("/predict", response_model=PredictionResponse, tags=["Prediccion"])
def predict_sentiment(body: TextInput) -> PredictionResponse:
    try:
        sentiment, confidence, cleaned_text = predict(body.text)
        save_prediction(body.text, cleaned_text, sentiment, confidence)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Error interno: {exc}") from exc

    return PredictionResponse(
        text=body.text,
        sentiment=sentiment,
        confidence=confidence,
        app_version=APP_VERSION,
    )


@router.get("/metrics", response_model=MetricsResponse, tags=["Evaluacion"])
def get_metrics() -> MetricsResponse:
    if not METRICS_PATH.exists():
        raise HTTPException(
            status_code=404,
            detail="Metricas no disponibles. Entrena el modelo primero con train.py.",
        )

    with METRICS_PATH.open("r", encoding="utf-8") as file_handle:
        data = json.load(file_handle)

    return MetricsResponse(
        accuracy=data["accuracy"],
        f1_weighted=data["f1_weighted"],
        confusion_matrix=data["confusion_matrix"],
        labels=data["labels"],
        tracked_predictions=count_predictions(),
    )


@router.get("/history", response_model=HistoryResponse, tags=["Monitorizacion"])
def get_history(
    limit: int = Query(default=10, ge=1, le=MAX_HISTORY_ITEMS, description="Numero maximo de filas.")
) -> HistoryResponse:
    return HistoryResponse(items=fetch_recent_predictions(limit))


@router.get("/export", tags=["Monitorizacion"])
def export_predictions() -> StreamingResponse:
    csv_payload = export_predictions_csv()
    return StreamingResponse(
        StringIO(csv_payload),
        media_type="text/csv",
        headers={"Content-Disposition": f'attachment; filename="{EXPORT_FILENAME}"'},
    )
