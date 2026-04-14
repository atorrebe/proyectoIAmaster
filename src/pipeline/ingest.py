import os
import pandas as pd

RAW_PATH = os.path.join("data", "raw", "amazon_reviews_multi.csv") PROCESSED_PATH = os.path.join("data", "processed", "reviews_es.csv")
MAX_RECORDS = 50000


def load_raw(path: str = RAW_PATH) -> pd.DataFrame: """Carga el CSV original en un DataFrame."""
if not os.path.exists(path): raise FileNotFoundError(
f"Dataset no encontrado en {path}.\n"
"Descárgalo desde Kaggle: https://www.kaggle.com/datasets/\n" "y colócalo en data/raw/amazon_reviews_multi.csv"
)
df = pd.read_csv(path, nrows=MAX_RECORDS) print(f"[ingest] Registros cargados: {len(df)}") return df


def filter_spanish(df: pd.DataFrame) -> pd.DataFrame: """Filtra únicamente las reseñas en español.""" if "language" not in df.columns:
raise ValueError("El dataset no contiene la columna 'language'.") df_es = df[df["language"] == "es"].copy()
print(f"[ingest] Reseñas en español: {len(df_es)}") return df_es


def assign_sentiment(df: pd.DataFrame) -> pd.DataFrame: """
Genera la columna 'sentiment' a partir de 'stars': 1-2 → negativo
3	→ neutro
4-5 → positivo
"""
def label(stars): if stars <= 2:
return "negativo" elif stars == 3:

return "neutro" else:
return "positivo"

df["sentiment"] = df["stars"].apply(label)
print(f"[ingest] Distribución de sentimientos:\n{df['sentiment'].value_counts()}") return df


def save_processed(df: pd.DataFrame, path: str = PROCESSED_PATH) -> None: """Guarda el DataFrame procesado en disco.""" os.makedirs(os.path.dirname(path), exist_ok=True)
df.to_csv(path, index=False)
print(f"[ingest] Dataset guardado en {path}")


def run():
df = load_raw()
df = filter_spanish(df) df = assign_sentiment(df) save_processed(df)
return df


if  name == " main ": run()
