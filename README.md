# proyectoIAmaster

> Proyecto de análisis de sentimiento mediante IA y Big Data

---

## Descripción del proyecto

Este proyecto tiene como objetivo desarrollar un sistema capaz de analizar textos y detectar automáticamente el sentimiento expresado en ellos (positivo, negativo o neutro). Se combinarán técnicas de **Big Data** para el procesamiento de grandes volúmenes de datos con modelos de **Inteligencia Artificial** para la clasificación de sentimientos.

El sistema se aplicará sobre datasets de comentarios y opiniones reales, permitiendo obtener insights a escala sobre la percepción de usuarios en distintos contextos (reseñas, redes sociales, foros, etc.).

---

## Integrantes

| Nombre                   |
| ------------------------ |
| Andrés Torres Berraquero |
| Angel Alegre I Mena      |
| Edgar Sarria Serrano     |
| Rodrigo Serrano Jiménez  |

---

## Arquitectura resumida

```
┌─────────────────┐     ┌──────────────────┐      ┌───────────────────┐
│   Fuente de     │────▶│  Procesamiento   │────▶│    Modelo de IA   │
│     datos       │     │   (Big Data)     │      │  (Sentimiento)    │
│  (dataset raw)  │     │  Spark / Pandas  │      │  Hugging Face /   │
└─────────────────┘     └──────────────────┘      │  Transformers     │
                                                  └────────┬──────────┘
                                                           │
                                                  ┌────────▼──────────┐
                                                  │    Resultados     │
                                                  │  y visualización  │
                                                  └───────────────────┘
```

**Fases del pipeline:**

1. **Ingesta** — Carga del dataset de comentarios/opiniones desde `data/raw/`
2. **Preprocesado** — Limpieza, tokenización y normalización del texto
3. **Modelado** — Entrenamiento o fine-tuning de un modelo de análisis de sentimiento
4. **Evaluación** — Métricas de precisión, recall y F1-score
5. **Visualización** — Exploración de resultados en notebooks Jupyter

---

## Cómo ejecutar

> ⚠️ _El proyecto está en fase inicial. Las instrucciones se irán completando en próximas fases._

### 1. Clonar el repositorio

```bash
git clone https://github.com/usuario/proyectoIAmaster.git
cd proyectoIAmaster
```

### 2. Crear entorno virtual e instalar dependencias

```bash
python -m venv venv
source venv/bin/activate      # En Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Ejecutar el pipeline (próximamente)

```bash
# Preprocesado
python src/preprocess.py

# Entrenamiento
python src/train.py

# Evaluación
python src/evaluate.py
```

### 4. Explorar los notebooks

```bash
jupyter notebook notebooks/
```

---

## Tecnologías

| Categoría              | Tecnología                |
| ---------------------- | ------------------------- |
| Lenguaje principal     | Python 3.10+              |
| Big Data               | Apache Spark / PySpark    |
| NLP y modelos          | Hugging Face Transformers |
| Análisis y exploración | Jupyter Notebook, Pandas  |
| Visualización          | Matplotlib, Seaborn       |
| Control de versiones   | Git / GitHub              |

---

## Estado actual

- [x] Definición de la idea y objetivos del proyecto
- [x] Organización del repositorio
- [ ] Selección definitiva del dataset
- [ ] Preprocesado de datos
- [ ] Entrenamiento del modelo
- [ ] Evaluación y resultados

---

## Estructura del proyecto

```
proyectoIAmaster/
├── data/
│   ├── raw/          # Datos originales sin modificar
│   └── processed/    # Datos limpios y preparados
├── docs/             # Documentación del proyecto
├── notebooks/        # Pruebas y análisis con Jupyter
├── src/              # Código principal
└── README.md
```
