import os
import zipfile

DATASET = "mexwell/amazon-reviews-multi"

# Descargar dataset
os.system(f"kaggle datasets download -d {DATASET}")

# Nombre del zip
zip_file = "amazon-reviews-multi.zip"

# Crear carpeta data
os.makedirs("data", exist_ok=True)

# Extraer
with zipfile.ZipFile(zip_file, 'r') as zip_ref:
    zip_ref.extractall("data/")

# Borrar zip
os.remove(zip_file)

print("Dataset descargado correctamente en /data")
