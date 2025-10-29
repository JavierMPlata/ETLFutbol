# 🐳 ETLFutbol - Guía Docker

## 📋 Descripción
Pipeline ETL para análisis de datos de fútbol containerizado con Docker. Este proyecto procesa datos de partidos de fútbol realizando extracción, transformación, carga y generación de gráficas analíticas.

## 🏗️ Arquitectura del Contenedor
- **Base**: Python 3.12-slim
- **Usuario**: etluser (no-root para seguridad)
- **Dependencias**: pandas, matplotlib, seaborn, numpy, requests, sqlite3
- **Volúmenes**: `/app/Files` (datos) y `/app/Graphics` (gráficas)

## 🚀 Inicio Rápido

### 1. Construir la Imagen
```powershell
# Desde el directorio raíz del proyecto
docker build -t etlfutbol:latest .
```

### 2. Ejecutar ETL Completo
```powershell
# Ejecución básica (recomendada)
docker run --rm --name etlfutbol-run `
  -v "$(pwd)/Files:/app/Files" `
  -v "$(pwd)/Graphics:/app/Graphics" `
  etlfutbol:latest
```

### 3. Usando Docker Compose (Más Fácil)
```powershell
# Ejecutar una vez
docker-compose up etl-futbol

# Ejecutar en segundo plano
docker-compose up -d etl-futbol
```

## 📖 Instrucciones Detalladas

### 🔨 Construir la Imagen

#### Construcción Básica
```powershell
docker build -t etlfutbol:latest .
```

#### Construcción con Tags Múltiples
```powershell
docker build -t etlfutbol:latest -t etlfutbol:v1.0 .
```

#### Construcción Forzada (sin cache)
```powershell
docker build --no-cache -t etlfutbol:latest .
```

#### Verificar la Imagen Creada
```powershell
docker images | findstr etlfutbol
```

### 🏃 Ejecutar el Contenedor

#### Ejecución Estándar (Recomendada)
```powershell
docker run --rm --name etlfutbol-run `
  -v "$(pwd)/Files:/app/Files" `
  -v "$(pwd)/Graphics:/app/Graphics" `
  etlfutbol:latest
```

#### Ejecución en Segundo Plano
```powershell
docker run -d --name etlfutbol-daemon `
  -v "$(pwd)/Files:/app/Files" `
  -v "$(pwd)/Graphics:/app/Graphics" `
  etlfutbol:latest
```

#### Ejecución Sin Volúmenes (Datos Temporales)
```powershell
docker run --rm --name etlfutbol-temp etlfutbol:latest
```

### 🔍 Debug y Desarrollo

#### 1. Modo Interactivo (Shell)
```powershell
# Acceder al contenedor con bash
docker run --rm -it --name etlfutbol-debug `
  -v "$(pwd)/Files:/app/Files" `
  -v "$(pwd)/Graphics:/app/Graphics" `
  etlfutbol:latest bash
```

#### 2. Ejecutar Comandos Específicos
```powershell
# Verificar dependencias
docker run --rm etlfutbol:latest python -c "import pandas, matplotlib, sqlite3; print('✅ OK')"

# Ver estructura de archivos
docker run --rm -v "$(pwd)/Files:/app/Files" etlfutbol:latest ls -la Files/

# Ejecutar solo limpieza de datos
docker run --rm -v "$(pwd)/Files:/app/Files" etlfutbol:latest `
  python -c "from Transform.FutbolClean import *; print('Limpieza OK')"
```

#### 3. Debug con Docker Compose
```powershell
# Levantar contenedor para desarrollo
docker-compose --profile dev up -d etl-futbol-dev

# Acceder al contenedor de desarrollo
docker exec -it etlfutbol-dev bash
```

#### 4. Inspeccionar Contenedor en Ejecución
```powershell
# Ver procesos dentro del contenedor
docker exec etlfutbol-daemon ps aux

# Ver logs en tiempo real
docker logs -f etlfutbol-daemon

# Ver estadísticas de recursos
docker stats etlfutbol-daemon
```

### 📊 Comandos Específicos del ETL

#### Solo Generar Gráficas
```powershell
docker run --rm `
  -v "$(pwd)/Files:/app/Files" `
  -v "$(pwd)/Graphics:/app/Graphics" `
  etlfutbol:latest python -c "
from Extract.FutolGraphics import FutbolGraphics
import pandas as pd
df = pd.read_csv('Files/Futbol.csv')
graphics = FutbolGraphics(df)
graphics.generate_all_graphics()
print('✅ Gráficas generadas')
"
```

#### Solo Limpieza de Datos
```powershell
docker run --rm `
  -v "$(pwd)/Files:/app/Files" `
  etlfutbol:latest python -c "
from Extract.FutbolExtract import futbolExtract
from Transform.FutbolClean import futbolClean
from Config.Config import Config

# Extraer y limpiar
extractor = futbolExtract(Config.INPUT_PATH)
extractor.queries()
cleaner = futbolClean(extractor.data)
clean_data = cleaner.full_cleaning_process()
print(f'✅ Datos limpios: {clean_data.shape}')
"
```

#### Solo Carga a SQLite
```powershell
docker run --rm `
  -v "$(pwd)/Files:/app/Files" `
  etlfutbol:latest python -c "
import pandas as pd
from Load.FutbolLoad import Loader

df = pd.read_csv('Files/Futbol.csv')
loader = Loader(df)
loader.to_sqlite()
print('✅ Datos cargados a SQLite')
"
```

## 🔧 Solución de Problemas

### Problema: Error de Permisos
```powershell
# Si hay problemas de permisos con los volúmenes
docker run --rm --user root -v "$(pwd):/app/project" etlfutbol:latest chown -R 1000:1000 /app/project
```

### Problema: Contenedor No Se Detiene
```powershell
# Forzar parada
docker kill etlfutbol-daemon
docker rm etlfutbol-daemon
```

### Problema: Imagen Muy Grande
```powershell
# Ver tamaño de las imágenes
docker images etlfutbol

# Limpiar imágenes no utilizadas
docker image prune -f
```

### Problema: Error en Dependencias
```powershell
# Reconstruir sin cache
docker build --no-cache -t etlfutbol:latest .

# Verificar dependencias específicas
docker run --rm etlfutbol:latest pip list
```

### Problema: Archivos No Se Guardan
```powershell
# Verificar que los directorios existen localmente
mkdir -p Files Graphics

# Verificar permisos de los volúmenes
docker run --rm -v "$(pwd):/test" etlfutbol:latest ls -la /test/
```

## 📁 Estructura de Archivos

### Archivos de Entrada (Files/)
- `Futbol.csv` - Datos de partidos de fútbol
- `etl_data.db` - Base de datos SQLite (generada)

### Archivos de Salida (Graphics/)
- Gráficas PNG generadas por el análisis
- Nombres automáticos basados en el tipo de gráfica

## 🔄 Flujo del ETL

1. **Extract** (`Extract/FutbolExtract.py`) - Lee datos CSV
2. **Transform** (`Transform/FutbolClean.py`) - Limpia y procesa datos
3. **Load** (`Load/FutbolLoad.py`) - Guarda en SQLite
4. **Graphics** (`Extract/FutolGraphics.py`) - Genera visualizaciones

## 📊 Monitoreo y Logs

### Ver Logs
```powershell
# Logs básicos
docker logs etlfutbol-daemon

# Logs con timestamps
docker logs -t etlfutbol-daemon

# Seguir logs en tiempo real
docker logs -f etlfutbol-daemon

# Últimas 50 líneas
docker logs --tail 50 etlfutbol-daemon
```

### Health Check
```powershell
# Verificar estado del contenedor
docker inspect etlfutbol-daemon | findstr Health

# Health check manual
docker run --rm etlfutbol:latest python -c "
import pandas, matplotlib, sqlite3, requests, numpy, seaborn
print('✅ Todas las dependencias funcionan correctamente')
"
```

## 🧹 Limpieza

### Limpiar Contenedores
```powershell
# Parar todos los contenedores de etlfutbol
docker ps -q --filter "name=etlfutbol" | ForEach-Object { docker stop $_ }

# Eliminar contenedores parados
docker container prune -f
```

### Limpiar Imágenes
```powershell
# Eliminar imágenes no utilizadas
docker image prune -f

# Eliminar imagen específica
docker rmi etlfutbol:latest
```

### Limpieza Completa
```powershell
# Limpieza completa del sistema Docker
docker system prune -af --volumes
```

## 🎯 Tips y Mejores Prácticas

1. **Siempre usar volúmenes** para persistir datos importantes
2. **Usar `--rm`** para contenedores de una sola ejecución
3. **Revisar logs** antes de reportar problemas
4. **Verificar permisos** si hay problemas con archivos
5. **Usar tags específicos** en producción (`v1.0` en lugar de `latest`)

## 📞 Soporte

Si encuentras problemas:
1. Revisa los logs: `docker logs <container-name>`
2. Verifica que los archivos de entrada existen
3. Comprueba que los directorios tienen permisos correctos
4. Ejecuta el health check manual

---
*Creado por: JavierMPlata*  
*Versión: 1.0*  
*Fecha: Octubre 2025*