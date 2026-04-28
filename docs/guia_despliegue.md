# Guia de despliegue

## Opcion 1. Ejecucion local

```bash
python -m venv venv
venv\Scripts\activate
pip install -r environment/requirements.txt
python src/main.py
```

## Opcion 2. Docker Compose

```bash
docker compose -f environment/docker-compose.yml up --build
```

## Coste estimado

Para esta entrega no se ha realizado despliegue cloud permanente. El coste estimado es `0 EUR` al ejecutarse localmente.

## Limitaciones

- No hay balanceo ni alta disponibilidad.
- SQLite no esta pensado para carga multiusuario real.
- El despliegue se orienta a demo academica y validacion funcional.
