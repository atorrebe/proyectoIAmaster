"""
train.py — Entrenamiento del modelo de análisis de sentimiento.
"""

import os
import json
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, classification_report, confusion_matrix

CLEAN_PATH = os.path.join("data", "processed", "reviews_clean.csv")
MODELS_DIR = "models"
MODEL_PATH = os.path.join(MODELS_DIR, "sentiment_model.joblib")
VECTORIZER_PATH = os.path.join(MODELS_DIR, "tfidf_vectorizer.joblib")
METRICS_PATH = os.path.join(MODELS_DIR, "metrics.json")

LABEL_ORDER = ["negativo", "neutro", "positivo"]
RANDOM_STATE = 42
TEST_SIZE = 0.2
MAX_FEATURES = 30000


def run():
    # Cargar datos
    df = pd.read_csv(CLEAN_PATH)
    df = df.dropna(subset=["review_clean", "sentiment"])
    print(f"[train] Registros disponibles: {len(df)}")
    print(f"[train] Distribución:\n{df['sentiment'].value_counts()}")

    # División train/test
    X = df["review_clean"].values
    y = df["sentiment"].values
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y
    )
    print(f"[train] Train: {len(X_train)} | Test: {len(X_test)}")

    # Vectorización TF-IDF
    vectorizer = TfidfVectorizer(
        max_features=MAX_FEATURES,
        ngram_range=(1, 2),
        sublinear_tf=True,
        min_df=2,
    )
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)

    # Entrenamiento
    print("[train] Entrenando modelo...")
    model = LogisticRegression(
        C=1.0,
        max_iter=1000,
        solver="lbfgs",
        random_state=RANDOM_STATE,
        class_weight="balanced",
    )
    model.fit(X_train_vec, y_train)

    # Evaluación
    y_pred = model.predict(X_test_vec)
    acc = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred, average="weighted")
    print(f"\n[train] Accuracy: {acc:.4f}")
    print(f"[train] F1 (weighted): {f1:.4f}")
    print(f"\n[train] Informe de clasificación:\n")
    print(classification_report(y_test, y_pred, labels=LABEL_ORDER))

    # Guardar artefactos
    os.makedirs(MODELS_DIR, exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    joblib.dump(vectorizer, VECTORIZER_PATH)

    metrics = {
        "accuracy": round(acc, 4),
        "f1_weighted": round(f1, 4),
        "confusion_matrix": confusion_matrix(y_test, y_pred, labels=LABEL_ORDER).tolist(),
        "labels": LABEL_ORDER,
    }
    with open(METRICS_PATH, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2, ensure_ascii=False)

    print(f"\n[train] Modelo guardado en {MODEL_PATH}")
    print(f"[train] Métricas guardadas en {METRICS_PATH}")


if __name__ == "__main__":
    run()