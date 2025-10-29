# Usar la imagen oficial de Python 3.12 (última versión estable)
FROM python:3.12-slim

# Información del mantenedor
LABEL maintainer="JavierMPlata" \
      description="ETL Pipeline para análisis de datos de fútbol" \
      version="1.0" \
      python.version="3.12"

# Establecer variables de entorno optimizadas para el proyecto
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    MPLBACKEND=Agg \
    MPLCONFIGDIR=/tmp/matplotlib \
    DEBIAN_FRONTEND=noninteractive

# Instalar dependencias del sistema necesarias para matplotlib, pandas y SQLite
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    pkg-config \
    libfreetype6-dev \
    libpng-dev \
    libjpeg-dev \
    libffi-dev \
    libssl-dev \
    sqlite3 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /tmp/* \
    && rm -rf /var/tmp/*

# Crear usuario no-root para seguridad
RUN groupadd -r etluser && useradd -r -g etluser -s /bin/bash etluser

# Establecer directorio de trabajo
WORKDIR /app

# Copiar archivos de dependencias primero (para aprovechar cache de Docker)
COPY requirements.txt .

# Actualizar pip e instalar dependencias de Python
RUN python -m pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt && \
    pip cache purge

# Crear directorios necesarios con permisos correctos
RUN mkdir -p Files Graphics /tmp/matplotlib && \
    chown -R etluser:etluser /app && \
    chmod 777 /tmp/matplotlib

# Cambiar al usuario no-root antes de copiar archivos
USER etluser

# Copiar el código fuente del proyecto con estructura completa
COPY --chown=etluser:etluser Config/ ./Config/
COPY --chown=etluser:etluser Extract/ ./Extract/
COPY --chown=etluser:etluser Transform/ ./Transform/
COPY --chown=etluser:etluser Load/ ./Load/
COPY --chown=etluser:etluser main.py .

# Copiar archivos de datos (CSV y cualquier base de datos existente)
COPY --chown=etluser:etluser Files/ ./Files/

# Crear volúmenes para persistir datos y gráficas generadas
VOLUME ["/app/Files", "/app/Graphics"]

# Comando de salud específico para verificar dependencias del ETL
HEALTHCHECK --interval=30s --timeout=15s --start-period=10s --retries=3 \
    CMD python -c "import pandas, matplotlib, sqlite3, requests, numpy, seaborn; print('ETL dependencies OK')" || exit 1

# Comando por defecto para ejecutar el pipeline ETL completo
CMD ["python", "main.py"]