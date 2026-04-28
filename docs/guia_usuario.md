# Guia de usuario

## Objetivo

La aplicacion permite analizar rapidamente una resena en espanol y obtener:

- clase de sentimiento
- nivel de confianza
- acceso a metricas del modelo
- historial reciente de predicciones

## Pasos de uso

1. Arranca la aplicacion con `python src/main.py`.
2. Abre `http://127.0.0.1:8000`.
3. Escribe un texto en el cuadro principal.
4. Pulsa `Analizar sentimiento`.
5. Revisa el resultado, la confianza y el historial.
6. Si necesitas entregar resultados, usa `Exportar historial CSV`.

## Recomendaciones

- Introduce texto en espanol.
- Usa comentarios con contenido real para obtener una prediccion mas representativa.
- Si la API no responde, comprueba que el modelo entrenado exista en `models/`.
