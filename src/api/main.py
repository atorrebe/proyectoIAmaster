"""
main.py — Punto de entrada de la aplicación FastAPI. Levanta la API REST del sistema de análisis de sentimiento.
Uso:
uvicorn src.api.main:app --reload --port 8000

Documentación interactiva disponible en: http://localhost:8000/docs
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware from src.api.router import router

app = FastAPI(
title="SentimentAPI — Análisis de Sentimiento en Español", description=(
"API REST para clasificar el sentimiento de textos en español " "como positivo, neutro o negativo. "
"Desarrollada como proyecto del Máster en IA y Big Data."
),
version="1.0.0", contact={
"name": "Andrés Torres Berraquero",
"url": "https://github.com/atorrebe/proyectoIAmaster",
},
)

# CORS: permite peticiones desde el frontend en local app.add_middleware(
CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"],
)

# Registrar rutas bajo el prefijo /api/v1 app.include_router(router, prefix="/api/v1")


@app.get("/", tags=["Raíz"]) def root():
"""Endpoint raíz — comprueba que el servidor responde.""" return {
"status": "ok",
"message": "SentimentAPI activa. Visita /docs para la documentación.",
}
