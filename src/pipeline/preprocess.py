"""
preprocess.py - Limpieza y normalizacion de texto en espanol.
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
from src.pipeline.text_utils import clean_text


PROCESSED_PATH = DATA_DIR / "processed" / "reviews_es.csv"
CLEAN_PATH = DATA_DIR / "processed" / "reviews_clean.csv"


def preprocess(df: pd.DataFrame) -> pd.DataFrame:
    prepared = df.copy()
    prepared["review_clean"] = prepared["review_body"].apply(clean_text)
    before = len(prepared)
    prepared = prepared[prepared["review_clean"].str.len() > 5].reset_index(drop=True)
    print(f"[preprocess] Registros eliminados por texto vacio: {before - len(prepared)}")
    print(f"[preprocess] Registros finales: {len(prepared)}")
    return prepared


def run() -> pd.DataFrame:
    dataframe = pd.read_csv(PROCESSED_PATH)
    cleaned = preprocess(dataframe)
    CLEAN_PATH.parent.mkdir(parents=True, exist_ok=True)
    cleaned.to_csv(CLEAN_PATH, index=False)
    print(f"[preprocess] Dataset limpio guardado en {CLEAN_PATH}")
    return cleaned


if __name__ == "__main__":
    run()
