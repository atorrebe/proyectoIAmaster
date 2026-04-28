"""
predict.py - Servicio de prediccion de sentimiento.
"""

from __future__ import annotations

import joblib

from src.core.config import MODEL_PATH, VECTORIZER_PATH
from src.pipeline.text_utils import clean_text


_model = None
_vectorizer = None


def _load_artifacts() -> None:
    global _model, _vectorizer
    if _model is None or _vectorizer is None:
        if not MODEL_PATH.exists() or not VECTORIZER_PATH.exists():
            raise FileNotFoundError(
                f"Modelo no encontrado en {MODEL_PATH}. "
                "Ejecuta primero: python src/pipeline/train.py"
            )
        _model = joblib.load(MODEL_PATH)
        _vectorizer = joblib.load(VECTORIZER_PATH)


def predict(text: str) -> tuple[str, float, str]:
    _load_artifacts()
    cleaned_text = clean_text(text)
    if not cleaned_text:
        raise ValueError("El texto no contiene contenido valido.")
    vector = _vectorizer.transform([cleaned_text])
    sentiment = _model.predict(vector)[0]
    probabilities = _model.predict_proba(vector)[0]
    confidence = float(max(probabilities))
    return sentiment, round(confidence, 4), cleaned_text
