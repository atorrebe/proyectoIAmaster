# Uso de IA en el proyecto

La IA se utiliza para clasificar el sentimiento de textos en espanol en tres categorias: `positivo`, `neutro` y `negativo`.

## En esta entrega

- Modelo principal: `Logistic Regression`
- Representacion del texto: `TF-IDF` con unigramas y bigramas
- Uso en produccion: inferencia local mediante FastAPI

## Alcance real

- El modelo no genera texto ni toma decisiones autonomas.
- La IA se limita a predecir la clase de sentimiento y una confianza asociada.
- Las predicciones quedan registradas en SQLite para trazabilidad y exportacion.
