"""
preprocess.py — Limpieza y normalización de texto en español.
"""

import os
import re
import pandas as pd

PROCESSED_PATH = os.path.join("data", "processed", "reviews_es.csv")
CLEAN_PATH = os.path.join("data", "processed", "reviews_clean.csv")

STOPWORDS_ES = {
    "de", "la", "que", "el", "en", "y", "a", "los", "del", "se",
    "las", "por", "un", "para", "con", "no", "una", "su", "al",
    "lo", "como", "mas", "pero", "sus", "le", "ya", "o", "este",
    "si", "porque", "esta", "entre", "cuando", "muy", "sin", "sobre",
    "ser", "tiene", "tambien", "me", "hasta", "hay", "donde", "quien",
    "desde", "todo", "nos", "durante", "todos", "uno", "les", "ni",
    "contra", "otros", "ese", "eso", "ante", "ellos", "e", "esto",
    "mi", "antes", "algunos", "que", "unos", "yo", "otro", "otras",
    "el", "tanto", "esa", "estos", "mucho", "quienes", "nada", "muchos",
    "cual", "poco", "ella", "estar", "estas", "algunas", "algo", "nosotros",
    "ha", "he", "han", "has", "habia", "fue", "son", "era", "estan", "esta", "es"
}


def clean_text(text):
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r"http\S+|www\.\S+", "", text)
    text = re.sub(r"[^a-zA-Z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    tokens = [w for w in text.split() if w not in STOPWORDS_ES and len(w) > 2]
    return " ".join(tokens)


def preprocess(df):
    df = df.copy()
    df["review_clean"] = df["review_body"].apply(clean_text)
    before = len(df)
    df = df[df["review_clean"].str.len() > 5].reset_index(drop=True)
    print(f"[preprocess] Registros eliminados por texto vacío: {before - len(df)}")
    print(f"[preprocess] Registros finales: {len(df)}")
    return df


def run():
    df = pd.read_csv(PROCESSED_PATH)
    df = preprocess(df)
    os.makedirs(os.path.dirname(CLEAN_PATH), exist_ok=True)
    df.to_csv(CLEAN_PATH, index=False)
    print(f"[preprocess] Dataset limpio guardado en {CLEAN_PATH}")
    return df


if __name__ == "__main__":
    run()