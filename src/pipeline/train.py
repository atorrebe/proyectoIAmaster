"""
train.py - Entrenamiento del modelo de analisis de sentimiento.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, f1_score
from sklearn.model_selection import train_test_split

PROJECT_ROOT = Path(__file__).resolve().parents[2]
project_root_str = str(PROJECT_ROOT)
if project_root_str not in sys.path:
    sys.path.insert(0, project_root_str)

from src.core.config import DATA_DIR, METRICS_PATH, MODEL_PATH, MODELS_DIR, VECTORIZER_PATH


LABEL_ORDER = ["negativo", "neutro", "positivo"]
RANDOM_STATE = 42
TEST_SIZE = 0.2
MAX_FEATURES = 30000


def run() -> None:
    clean_path = DATA_DIR / "processed" / "reviews_clean.csv"
    dataframe = pd.read_csv(clean_path)
    dataframe = dataframe.dropna(subset=["review_clean", "sentiment"])
    print(f"[train] Registros disponibles: {len(dataframe)}")
    print(f"[train] Distribucion:\n{dataframe['sentiment'].value_counts()}")

    texts = dataframe["review_clean"].values
    labels = dataframe["sentiment"].values
    x_train, x_test, y_train, y_test = train_test_split(
        texts,
        labels,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
        stratify=labels,
    )
    print(f"[train] Train: {len(x_train)} | Test: {len(x_test)}")

    vectorizer = TfidfVectorizer(
        max_features=MAX_FEATURES,
        ngram_range=(1, 2),
        sublinear_tf=True,
        min_df=2,
    )
    x_train_vec = vectorizer.fit_transform(x_train)
    x_test_vec = vectorizer.transform(x_test)

    print("[train] Entrenando modelo...")
    model = LogisticRegression(
        C=1.0,
        max_iter=1000,
        solver="lbfgs",
        random_state=RANDOM_STATE,
        class_weight="balanced",
    )
    model.fit(x_train_vec, y_train)

    predictions = model.predict(x_test_vec)
    accuracy = accuracy_score(y_test, predictions)
    f1_weighted = f1_score(y_test, predictions, average="weighted")
    print(f"\n[train] Accuracy: {accuracy:.4f}")
    print(f"[train] F1 (weighted): {f1_weighted:.4f}")
    print("\n[train] Informe de clasificacion:\n")
    print(classification_report(y_test, predictions, labels=LABEL_ORDER))

    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    joblib.dump(vectorizer, VECTORIZER_PATH)

    metrics = {
        "accuracy": round(accuracy, 4),
        "f1_weighted": round(f1_weighted, 4),
        "confusion_matrix": confusion_matrix(y_test, predictions, labels=LABEL_ORDER).tolist(),
        "labels": LABEL_ORDER,
    }
    with METRICS_PATH.open("w", encoding="utf-8") as file_handle:
        json.dump(metrics, file_handle, indent=2, ensure_ascii=False)

    print(f"\n[train] Modelo guardado en {MODEL_PATH}")
    print(f"[train] Metricas guardadas en {METRICS_PATH}")


if __name__ == "__main__":
    run()
