from src.pipeline.ingest import run as run_ingest
from src.pipeline.preprocess import run as run_preprocess
from src.pipeline.train import run as run_train


def main() -> None:
    print("[main] Iniciando pipeline de análisis de sentimiento...")
    run_ingest()
    run_preprocess()
    run_train()
    print("[main] Pipeline completado correctamente.")


if __name__ == "__main__":
    main()
