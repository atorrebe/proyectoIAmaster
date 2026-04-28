# Guia tecnica

## Componentes

- `src/pipeline/`: ingesta, limpieza y entrenamiento
- `src/api/`: endpoints FastAPI
- `src/services/storage.py`: persistencia SQLite y export CSV
- `src/frontend/index.html`: interfaz de usuario
- `models/`: artefactos del modelo y metricas

## Flujo de prediccion

1. El frontend envia el texto a `POST /api/v1/predict`.
2. La API limpia el texto con la misma logica usada en entrenamiento.
3. Se cargan modelo y vectorizador desde `models/`.
4. Se devuelve la clase predicha y la confianza.
5. La prediccion se guarda en SQLite.
6. El dashboard refresca metricas e historial.

## Seguridad basica aplicada

- `TrustedHostMiddleware`
- CORS restringido por variable de entorno
- Cabeceras `nosniff`, `DENY`, `no-store`

## Tests cubiertos

- Salud del sistema
- Prediccion y persistencia
- Lectura de metricas
- Exportacion CSV
