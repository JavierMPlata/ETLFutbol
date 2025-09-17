from Extract.FutbolExtract import futbolExtract
from Transform.FutbolClean import futbolClean
from Load.FutbolLoad import Loader
from Config.Config import Config

# Extracción de datos
print("EXTRAYENDO DATOS...")
print("=" * 50)
response1 = futbolExtract(Config.INPUT_PATH)
response1.queries()

print("Primeras 5 filas de los datos extraídos:")
print(response1.response())

# Limpieza de datos
print("\n" + "=" * 50)
print("PROCESO DE LIMPIEZA DE DATOS")
print("=" * 50)

# Crear instancia de limpieza con los datos extraídos
cleaner = futbolClean(response1.data)

# Ejecutar proceso completo de limpieza
cleaned_data = cleaner.full_cleaning_process()

print("\n" + "=" * 50)
print("DATOS LIMPIOS - PRIMERAS 15 FILAS:")
print("=" * 50)
print(cleaned_data.head(15))

print("\n" + "=" * 50)
print("INFORMACIÓN FINAL DEL DATASET LIMPIO:")
print("=" * 50)
print(f"Shape: {cleaned_data.shape}")
print(f"Tipos de datos:")
print(cleaned_data.dtypes)
print(f"\nValores nulos finales:")
print(cleaned_data.isnull().sum())

# Carga de datos
loader = Loader(cleaned_data)
loader.to_sqlite()