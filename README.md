# proyectoIAmaster

Proyecto final de analisis de sentimiento en espanol para el Curso de Especializacion en Inteligencia Artificial y Big Data.

## Resumen

La aplicacion analiza resenas en espanol a partir de un modelo `Logistic Regression + TF-IDF`, expone una API REST con FastAPI y ofrece una interfaz web integrada para:

- lanzar predicciones
- consultar metricas del modelo
- guardar historial en SQLite
- exportar resultados a CSV

Esta version corresponde al cierre de Fase 3 y prioriza una ejecucion local sencilla, trazabilidad de predicciones y documentacion final coherente con el codigo.

## Mejoras de Fase 3

- Arranque con un solo comando usando `python src/main.py`
- Frontend servido por la propia API para evitar problemas de `file://`
- Persistencia local de predicciones en `SQLite`
- Exportacion del historial a `CSV`
- Dashboard ligero con metricas, matriz de confusion e historial reciente
- Validaciones y gestion de errores mas claras
- Seguridad basica con `TrustedHostMiddleware`, `CORS` restringido y cabeceras defensivas
- Tests de API para `health`, `predict`, `metrics` y `export`
- Dockerfile y `docker-compose.yml` corregidos

## Arquitectura final

```text
Dataset -> Pipeline (ingest / preprocess / train)
       -> Artifacts del modelo (.joblib + metrics.json)
       -> API FastAPI
       -> Frontend web servido por la API
       -> SQLite (historial de predicciones)
       -> Export CSV
```

## Estructura del proyecto

```text
proyectoIAmaster/
|-- data/
|-- docs/
|-- environment/
|-- models/
|-- src/
|   |-- api/
|   |-- core/
|   |-- frontend/
|   |-- pipeline/
|   `-- services/
|-- tests/
|-- pytest.ini
`-- README.md
```

## Requisitos

- Python 3.10 o superior
- `pip`
- Modelos entrenados dentro de `models/`

## Ejecucion local

### 1. Crear entorno e instalar dependencias

```bash
python -m venv venv
venv\Scripts\activate
pip install -r environment/requirements.txt
```

### 2. Arrancar la aplicacion

```bash
python src/main.py
```

### 3. Abrir la interfaz

Visita [http://127.0.0.1:8000](http://127.0.0.1:8000)

### 4. Endpoints principales

- `GET /api/v1/health`
- `POST /api/v1/predict`
- `GET /api/v1/metrics`
- `GET /api/v1/history`
- `GET /api/v1/export`

## Automatizacion

- Ejecucion local: `python src/main.py`
- Contenedores: `docker compose -f environment/docker-compose.yml up --build`

## Tests

```bash
pytest
```

## Limitaciones actuales

- No se ha desplegado en cloud para evitar coste y complejidad extra en un entorno academico local.
- El modelo final sigue siendo clasico; la comparativa con transformers se mantiene como mejora futura.
- No se ha automatizado retraining ni monitorizacion avanzada de MLOps.
- La base de datos SQLite esta pensada para demo local, no para concurrencia alta.

## Documentacion adicional

- [Guia de usuario](docs/guia_usuario.md)
- [Guia tecnica](docs/guia_tecnica.md)
- [Guia de despliegue](docs/guia_despliegue.md)
