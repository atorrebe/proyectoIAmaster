"""
preprocess.py — Limpieza y normalización de texto en español.

Aplica las siguientes transformaciones al campo 'review_body':
Conversión a minúsculas
Eliminación de URLs
Eliminación de caracteres no alfanuméricos (conserva tildes y ñ)
Eliminación de espacios múltiples
Eliminación de stopwords en español """

import os import re
import pandas as pd

PROCESSED_PATH = os.path.join("data", "processed", "reviews_es.csv") CLEAN_PATH = os.path.join("data", "processed", "reviews_clean.csv")

# Stopwords básicas en español (sin dependencia de NLTK) STOPWORDS_ES = {
"de", "la", "que", "el", "en", "y", "a", "los", "del", "se",
"las", "por", "un", "para", "con", "no", "una", "su", "al",
"lo", "como", "más", "pero", "sus", "le", "ya", "o", "este",
"si", "porque", "esta", "entre", "cuando", "muy", "sin", "sobre",
"ser", "tiene", "también", "me", "hasta", "hay", "donde", "quien",
"desde", "todo", "nos", "durante", "todos", "uno", "les", "ni",
"contra", "otros", "ese", "eso", "ante", "ellos", "e", "esto",
"mí", "antes", "algunos", "qué", "unos", "yo", "otro", "otras",
"él", "tanto", "esa", "estos", "mucho", "quienes", "nada", "muchos",

"cual", "poco", "ella", "estar", "estas", "algunas", "algo", "nosotros",
"mi", "mis", "tú", "te", "ti", "tu", "tus", "vosotros", "vosotras",
"os", "mío", "mía", "míos", "mías", "tuyo", "tuya", "tuyos", "tuyas",
"suyo", "suya", "suyos", "suyas", "nuestro", "nuestra", "nuestros",
"nuestras", "vuestro", "vuestra", "vuestros", "vuestras", "ha", "he",
"han", "has", "había", "fue", "son", "era", "son", "están", "está", "es", "am", "are", "been"
}


def clean_text(text: str) -> str:
"""Aplica limpieza estándar a un texto en español.""" if not isinstance(text, str):
return "" # Minúsculas
text = text.lower() # Eliminar URLs
text = re.sub(r"http\S+|www\.\S+", "", text)
# Eliminar caracteres no alfanuméricos excepto letras con tilde y ñ text = re.sub(r"[^a-záéíóúüñ\s]", " ", text)
# Eliminar espacios múltiples
text = re.sub(r"\s+", " ", text).strip() # Eliminar stopwords
tokens = [w for w in text.split() if w not in STOPWORDS_ES and len(w) > 2] return " ".join(tokens)


def preprocess(df: pd.DataFrame) -> pd.DataFrame: """Aplica la limpieza al DataFrame."""
if "review_body" not in df.columns:
raise ValueError("El DataFrame no contiene la columna 'review_body'.") df = df.copy()
df["review_clean"] = df["review_body"].apply(clean_text) # Eliminar textos vacíos tras la limpieza
before = len(df)
df = df[df["review_clean"].str.len() > 5].reset_index(drop=True) print(f"[preprocess] Registros eliminados por texto vacío: {before - len(df)}") print(f"[preprocess] Registros finales: {len(df)}")
return df


def run():
if not os.path.exists(PROCESSED_PATH): raise FileNotFoundError(
f"Ejecuta primero src/pipeline/ingest.py para generar {PROCESSED_PATH}"
)
df = pd.read_csv(PROCESSED_PATH) df = preprocess(df)
os.makedirs(os.path.dirname(CLEAN_PATH), exist_ok=True) df.to_csv(CLEAN_PATH, index=False)
print(f"[preprocess] Dataset limpio guardado en {CLEAN_PATH}") return df


if  name == " main ": run()

