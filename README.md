# ETLFutbol 🏈⚽

Un proyecto de **ETL (Extract, Transform, Load)** para el análisis de datos de partidos de fútbol. Este sistema automatiza la extracción, limpieza, transformación y carga de datos futbolísticos, así como la generación de visualizaciones analíticas.

## 📋 Descripción

ETLFutbol es un pipeline completo de procesamiento de datos diseñado para analizar información de partidos de fútbol. El sistema procesa archivos CSV con resultados de partidos, realiza limpieza y transformación de datos, y genera visualizaciones estadísticas para análisis deportivo.

## 📊 Dataset

Este proyecto utiliza el dataset **"Resultados de Fútbol entre 1872 y 2017"** disponible en Kaggle:

🔗 **[Dataset: Resultados de Fútbol (1872-2017)](https://www.kaggle.com/datasets/ramnquintana/resultados-de-futbol-entre-1872-y-2017)**

### Características del Dataset:
- **Período temporal**: 1872 - 2017 (145 años de historia futbolística)
- **Cobertura global**: Partidos de múltiples países y competiciones
- **Formato**: CSV con información estructurada de resultados
- **Campos principales**: Fecha, equipos, marcadores, torneos y países

Para usar este proyecto, descarga el dataset desde Kaggle y colócalo en la carpeta `Files/` con el nombre `Futbol.csv`.

## 🏗️ Arquitectura del Proyecto

```
ETLFutbol/
├── main.py                    # Punto de entrada principal
├── requirements.txt           # Dependencias del proyecto
├── Config/                    # Configuraciones
│   ├── __init__.py
│   └── Config.py             # Parámetros de configuración
├── Extract/                   # Módulo de extracción
│   ├── __init__.py
│   ├── FutbolExtract.py      # Extracción de datos CSV
│   └── FutolGraphics.py      # Generación de gráficas
├── Transform/                 # Módulo de transformación
│   ├── __init__.py
│   └── FutbolClean.py        # Limpieza y transformación
├── Load/                      # Módulo de carga
│   ├── __init__.py
│   └── FutbolLoad.py         # Carga a SQLite y CSV
├── Files/                     # Archivos de datos
│   ├── Futbol.csv            # Dataset original
│   └── etl_data.db           # Base de datos SQLite
└── Graphics/                  # Visualizaciones generadas
    ├── analisis_temporal.png
    ├── distribucion_goles.png
    └── top_equipos.png
```

## 🚀 Características Principales

### ✅ **Extract (Extracción)**
- Lectura de archivos CSV con datos de partidos
- Análisis inicial de la estructura de datos
- Validación de formato y contenido

### 🧹 **Transform (Transformación)**
- **Limpieza de datos**: Eliminación de valores nulos y duplicados
- **Validación de datos**: Verificación de tipos y rangos
- **Estandarización**: Normalización de nombres de equipos y fechas
- **Cálculo de métricas**: Estadísticas derivadas de los partidos

### 💾 **Load (Carga)**
- Exportación a **SQLite** para consultas eficientes
- Generación de archivos **CSV** limpios
- Almacenamiento estructurado para análisis posterior

### 📊 **Visualizaciones**
- **Distribución de goles**: Análisis estadístico de marcadores
- **Análisis temporal**: Tendencias a lo largo del tiempo
- **Top equipos**: Rankings y rendimiento de equipos
- **Gráficas personalizables** con matplotlib y seaborn

## 🛠️ Tecnologías Utilizadas

- **Python 3.x**
- **Pandas**: Manipulación y análisis de datos
- **NumPy**: Operaciones numéricas
- **Matplotlib**: Visualización de datos
- **Seaborn**: Gráficas estadísticas avanzadas
- **SQLite**: Base de datos embebida
- **Requests**: Manejo de peticiones HTTP (futuras extensiones)

## 📦 Instalación

### Prerrequisitos
- Python 3.7 o superior
- pip (gestor de paquetes de Python)

### Pasos de instalación

1. **Clonar el repositorio**:
```bash
git clone https://github.com/JavierMPlata/ETLFutbol.git
cd ETLFutbol
```

2. **Crear entorno virtual** (recomendado):
```bash
python -m venv venv
venv\Scripts\activate  # En Windows
# source venv/bin/activate  # En Linux/Mac
```

3. **Instalar dependencias**:
```bash
pip install -r requirements.txt
```

## 🎮 Uso

### Ejecución básica
```bash
python main.py
```

### Proceso completo
El script principal ejecuta automáticamente:

1. **Extracción** de datos desde `Files/Futbol.csv`
2. **Limpieza** y transformación de datos
3. **Generación** de visualizaciones en `Graphics/`
4. **Carga** de datos limpios a SQLite

### Configuración personalizada

Edita `Config/Config.py` para ajustar rutas y parámetros:

```python
class Config:
    INPUT_PATH = r'Files\Futbol.csv'           # Archivo de entrada
    SQLITE_DB_PATH = r'Files\etl_data.db'     # Base de datos SQLite
    SQLITE_TABLE = 'futbol_data_clean'        # Tabla de destino
```

## 📈 Análisis Generados

### 1. Distribución de Goles
- Histogramas de goles locales y visitantes
- Análisis estadístico de marcadores
- Identificación de patrones de puntuación

### 2. Análisis Temporal
- Tendencias de goles a lo largo del tiempo
- Estacionalidad en el rendimiento
- Evolución de equipos por temporadas

### 3. Rankings de Equipos
- Top equipos por victorias
- Análisis de rendimiento local vs visitante
- Métricas de efectividad ofensiva y defensiva

## 🔧 Estructura de Datos

### Formato de entrada esperado (CSV):
```
date,home_team,away_team,home_score,away_score,tournament,country
2023-01-15,Barcelona,Real Madrid,2,1,La Liga,Spain
```

### Campos procesados:
- **date**: Fecha del partido (formato YYYY-MM-DD)
- **home_team**: Equipo local
- **away_team**: Equipo visitante  
- **home_score**: Goles del equipo local
- **away_score**: Goles del equipo visitante
- **tournament**: Competición
- **country**: País


## 📊 Ejemplos de Salida

```
EXTRAYENDO DATOS...
==================================================
Primeras 5 filas de los datos extraídos:
        date   home_team    away_team  home_score  away_score
0  2023-01-15   Barcelona  Real Madrid           2           1

==================================================
PROCESO DE LIMPIEZA DE DATOS
==================================================
✅ Datos duplicados removidos: 15
✅ Valores nulos procesados: 8
✅ Formato de fechas estandarizado
✅ Nombres de equipos normalizados

==================================================
GENERANDO GRÁFICAS DE ANÁLISIS
==================================================
📊 Gráfica guardada: Graphics/distribucion_goles.png
📊 Gráfica guardada: Graphics/analisis_temporal.png
📊 Gráfica guardada: Graphics/top_equipos.png
```

## 📞 Contacto

**Javier M. Plata** - [@JavierMPlata](https://github.com/JavierMPlata)

Proyecto: [https://github.com/JavierMPlata/ETLFutbol](https://github.com/JavierMPlata/ETLFutbol)

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

---

⭐ **¡Dale una estrella al proyecto si te ha sido útil!** ⭐