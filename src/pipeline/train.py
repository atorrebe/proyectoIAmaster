Entrena el modelo Logistic Regression con TF-IDF, evalúa y persiste los artefactos en models/.
"""

train.py — Entrenamiento del modelo de análisis de sentimiento.

Entrena un clasificador Logistic Regression sobre representaciones TF-IDF del texto limpio. Guarda el modelo y el vectorizador en models/.

Flujo:
Carga data/processed/reviews_clean.csv
División train/test (80/20, estratificada)
Vectorización TF-IDF
Entrenamiento Logistic Regression
Evaluación con accuracy, F1 y matriz de confusión
Persistencia del modelo con joblib """

import os import json import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer from sklearn.linear_model import LogisticRegression
from sklearn.metrics import ( accuracy_score,
f1_score, classification_report, confusion_matrix,
)

CLEAN_PATH = os.path.join("data", "processed", "reviews_clean.csv") MODELS_DIR = "models"
MODEL_PATH = os.path.join(MODELS_DIR, "sentiment_model.joblib") VECTORIZER_PATH = os.path.join(MODELS_DIR, "tfidf_vectorizer.joblib") METRICS_PATH = os.path.join(MODELS_DIR, "metrics.json")

LABEL_ORDER = ["negativo", "neutro", "positivo"] RANDOM_STATE = 42
TEST_SIZE = 0.2
MAX_FEATURES = 30000
C_VALUE = 1.0


def load_data(path: str = CLEAN_PATH) -> pd.DataFrame: """Carga el dataset limpio."""
if not os.path.exists(path): raise FileNotFoundError(
f"Dataset limpio no encontrado en {path}.\n" "Ejecuta primero: python src/pipeline/preprocess.py"
)
df = pd.read_csv(path)
df = df.dropna(subset=["review_clean", "sentiment"]) print(f"[train] Registros disponibles: {len(df)}") print(f"[train] Distribución:\n{df['sentiment'].value_counts()}") return df


def split_data(df: pd.DataFrame): """División estratificada train/test."""
X = df["review_clean"].values y = df["sentiment"].values
X_train, X_test, y_train, y_test = train_test_split(
X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y
)

print(f"[train] Train: {len(X_train)} | Test: {len(X_test)}") return X_train, X_test, y_train, y_test


def build_vectorizer() -> TfidfVectorizer: """Crea el vectorizador TF-IDF.""" return TfidfVectorizer(
max_features=MAX_FEATURES, ngram_range=(1, 2), sublinear_tf=True, min_df=2,
)


def train_model(X_train_vec, y_train) -> LogisticRegression: """Entrena el clasificador Logistic Regression."""
model = LogisticRegression( C=C_VALUE,
max_iter=1000, multi_class="multinomial", solver="lbfgs", random_state=RANDOM_STATE, class_weight="balanced",
)
model.fit(X_train_vec, y_train) return model


def evaluate(model, X_test_vec, y_test) -> dict: """Calcula métricas de evaluación."""
y_pred = model.predict(X_test_vec) acc = accuracy_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred, average="weighted")
report = classification_report(y_test, y_pred, labels=LABEL_ORDER, output_dict=True) cm = confusion_matrix(y_test, y_pred, labels=LABEL_ORDER).tolist()

metrics = {
"accuracy": round(acc, 4),
"f1_weighted": round(f1, 4), "classification_report": report, "confusion_matrix": cm, "labels": LABEL_ORDER,
}

print(f"\n[train] Accuracy: {acc:.4f}") print(f"[train] F1 (weighted): {f1:.4f}") print(f"\n[train] Informe de clasificación:\n")
print(classification_report(y_test, y_pred, labels=LABEL_ORDER)) return metrics


def save_artifacts(model, vectorizer, metrics):
"""Persiste el modelo, vectorizador y métricas en disco.""" os.makedirs(MODELS_DIR, exist_ok=True)
joblib.dump(model, MODEL_PATH) joblib.dump(vectorizer, VECTORIZER_PATH)
with open(METRICS_PATH, "w", encoding="utf-8") as f: json.dump(metrics, f, indent=2, ensure_ascii=False)
print(f"\n[train] Modelo guardado en {MODEL_PATH}") print(f"[train] Vectorizador guardado en {VECTORIZER_PATH}") print(f"[train] Métricas guardadas en {METRICS_PATH}")
def run():

df = load_data()
X_train, X_test, y_train, y_test = split_data(df)

vectorizer = build_vectorizer()
X_train_vec = vectorizer.fit_transform(X_train) X_test_vec = vectorizer.transform(X_test)

model = train_model(X_train_vec, y_train) metrics = evaluate(model, X_test_vec, y_test) save_artifacts(model, vectorizer, metrics) return model, vectorizer, metrics


if  name == " main ": run()
