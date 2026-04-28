"""
ingest.py - Carga y filtrado del dataset Amazon Reviews Multi.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
project_root_str = str(PROJECT_ROOT)
if project_root_str not in sys.path:
    sys.path.insert(0, project_root_str)

from src.core.config import DATA_DIR


RAW_PATH = DATA_DIR / "raw" / "amazon_reviews_multi.csv"
PROCESSED_PATH = DATA_DIR / "processed" / "reviews_es.csv"
MAX_RECORDS = 1200000


def load_raw(path: Path = RAW_PATH) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Dataset no encontrado en {path}.")
    dataframe = pd.read_csv(path, nrows=MAX_RECORDS)
    print(f"[ingest] Registros cargados: {len(dataframe)}")
    return dataframe


def filter_spanish(dataframe: pd.DataFrame) -> pd.DataFrame:
    filtered = dataframe[dataframe["language"] == "es"].copy()
    print(f"[ingest] Resenas en espanol: {len(filtered)}")
    return filtered


def assign_sentiment(dataframe: pd.DataFrame) -> pd.DataFrame:
    def label(stars):
        if stars <= 2:
            return "negativo"
        if stars == 3:
            return "neutro"
        return "positivo"

    dataframe["sentiment"] = dataframe["stars"].apply(label)
    print(f"[ingest] Distribucion:\n{dataframe['sentiment'].value_counts()}")
    return dataframe


def save_processed(dataframe: pd.DataFrame, path: Path = PROCESSED_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    dataframe.to_csv(path, index=False)
    print(f"[ingest] Dataset guardado en {path}")


def run() -> pd.DataFrame:
    dataframe = load_raw()
    dataframe = filter_spanish(dataframe)
    dataframe = assign_sentiment(dataframe)
    save_processed(dataframe)
    return dataframe


if __name__ == "__main__":
    run()
