"""
predict.py — Servicio de predicción de sentimiento.

Carga el modelo y el vectorizador entrenados y expone la función predict() para uso interno por la API.
"""

import os import re import joblib
from typing import Tuple

MODELS_DIR = "models"
MODEL_PATH = os.path.join(MODELS_DIR, "sentiment_model.joblib") VECTORIZER_PATH = os.path.join(MODELS_DIR, "tfidf_vectorizer.joblib")

STOPWORDS_ES = {
"de", "la", "que", "el", "en", "y", "a", "los", "del", "se",
"las", "por", "un", "para", "con", "no", "una", "su", "al",
"lo", "como", "más", "pero", "sus", "le", "ya", "o", "este",
"si", "porque", "esta", "entre", "cuando", "muy", "sin", "sobre",
"ser", "tiene", "también", "me", "hasta", "hay", "donde", "quien",
"desde", "todo", "nos", "durante", "todos", "uno", "les", "ni",
"contra", "otros", "ese", "eso", "ante", "ellos", "e", "esto",
}

# Carga lazy: el modelo se carga solo cuando se necesita por primera vez
_model = None
_vectorizer = None


def _load_artifacts():
"""Carga el modelo y el vectorizador desde disco.""" global _model, _vectorizer
if _model is None or _vectorizer is None: if not os.path.exists(MODEL_PATH):
raise FileNotFoundError(
f"Modelo no encontrado en {MODEL_PATH}.\n" "Ejecuta primero: python src/pipeline/train.py"
)
_model = joblib.load(MODEL_PATH)
_vectorizer = joblib.load(VECTORIZER_PATH)

def _clean(text: str) -> str:
"""Aplica la misma limpieza que preprocess.py.""" if not isinstance(text, str):
return ""
text = text.lower()
text = re.sub(r"http\S+|www\.\S+", "", text) text = re.sub(r"[^a-záéíóúüñ\s]", " ", text)
text = re.sub(r"\s+", " ", text).strip()
tokens = [w for w in text.split() if w not in STOPWORDS_ES and len(w) > 2] return " ".join(tokens)


def predict(text: str) -> Tuple[str, float]: """
Recibe un texto en español y devuelve:
sentiment (str): 'positivo', 'neutro' o 'negativo'
confidence (float): probabilidad máxima del modelo

Args:
text: texto de la reseña en español.

Returns:
Tupla (sentiment, confidence).

Raises:
FileNotFoundError: si el modelo no está entrenado. ValueError: si el texto está vacío tras la limpieza.
"""
_load_artifacts() clean = _clean(text) if not clean:
raise ValueError("El texto proporcionado no contiene contenido válido.") vec = _vectorizer.transform([clean])
sentiment = _model.predict(vec)[0] proba = _model.predict_proba(vec)[0] confidence = float(max(proba))
return sentiment, round(confidence, 4)
