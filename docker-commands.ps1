# ====================================================================
# COMANDOS DOCKER PARA ETLFutbol Pipeline
# Ejecutar desde la raíz del proyecto: d:\...\ETLFutbol\
# ====================================================================

Write-Host "🐳 === COMANDOS DOCKER PARA ETLFutbol ===" -ForegroundColor Green

Write-Host "`n📦 1. CONSTRUIR LA IMAGEN:" -ForegroundColor Yellow
Write-Host "docker build -t etlfutbol:latest -t etlfutbol:v1.0 ." -ForegroundColor Cyan

Write-Host "`n🚀 2. EJECUTAR ETL COMPLETO (recomendado):" -ForegroundColor Yellow
Write-Host "docker run --rm --name etlfutbol-run -v `"`$(pwd)/Files:/app/Files`" -v `"`$(pwd)/Graphics:/app/Graphics`" etlfutbol:latest" -ForegroundColor Cyan

Write-Host "`n🔍 3. EJECUTAR EN MODO INTERACTIVO (debug):" -ForegroundColor Yellow
Write-Host "docker run --rm -it --name etlfutbol-debug -v `"`$(pwd)/Files:/app/Files`" -v `"`$(pwd)/Graphics:/app/Graphics`" etlfutbol:latest bash" -ForegroundColor Cyan

Write-Host "`n⚡ 4. EJECUTAR EN SEGUNDO PLANO:" -ForegroundColor Yellow
Write-Host "docker run -d --name etlfutbol-daemon -v `"`$(pwd)/Files:/app/Files`" -v `"`$(pwd)/Graphics:/app/Graphics`" etlfutbol:latest" -ForegroundColor Cyan

Write-Host "`n📊 5. SOLO GENERAR GRÁFICAS (comando personalizado):" -ForegroundColor Yellow
Write-Host "docker run --rm -v `"`$(pwd)/Files:/app/Files`" -v `"`$(pwd)/Graphics:/app/Graphics`" etlfutbol:latest python -c `"from Extract.FutolGraphics import *; import pandas as pd; df=pd.read_csv('Files/Futbol.csv'); g=FutbolGraphics(df); g.generate_all_graphics()`"" -ForegroundColor Cyan

Write-Host "`n📋 6. VER LOGS DEL PROCESO:" -ForegroundColor Yellow
Write-Host "docker logs etlfutbol-daemon" -ForegroundColor Cyan
Write-Host "docker logs -f etlfutbol-daemon  # (seguir logs en tiempo real)" -ForegroundColor Gray

Write-Host "`n🔧 7. ACCEDER AL CONTENEDOR:" -ForegroundColor Yellow
Write-Host "docker exec -it etlfutbol-daemon bash" -ForegroundColor Cyan

Write-Host "`n⏹️  8. PARAR Y LIMPIAR CONTENEDORES:" -ForegroundColor Yellow
Write-Host "docker stop etlfutbol-daemon && docker rm etlfutbol-daemon" -ForegroundColor Cyan

Write-Host "`n🧹 9. LIMPIAR IMÁGENES Y CACHE:" -ForegroundColor Yellow
Write-Host "docker image prune -f" -ForegroundColor Cyan
Write-Host "docker system prune -f  # (limpiar todo el sistema)" -ForegroundColor Gray

Write-Host "`n📋 10. INFORMACIÓN Y ESTADO:" -ForegroundColor Yellow
Write-Host "docker images | findstr etlfutbol  # Ver imágenes" -ForegroundColor Cyan
Write-Host "docker ps -a | findstr etlfutbol   # Ver contenedores" -ForegroundColor Cyan
Write-Host "docker inspect etlfutbol:latest    # Detalles de la imagen" -ForegroundColor Cyan

Write-Host "`n💾 11. VERIFICAR ARCHIVOS GENERADOS:" -ForegroundColor Yellow
Write-Host "ls ./Graphics/  # Ver gráficas generadas" -ForegroundColor Cyan
Write-Host "ls ./Files/     # Ver archivos de datos y BD" -ForegroundColor Cyan

Write-Host "`n🏥 12. HEALTH CHECK:" -ForegroundColor Yellow
Write-Host "docker run --rm etlfutbol:latest python -c `"import pandas, matplotlib, sqlite3; print('✅ Todas las dependencias OK')`"" -ForegroundColor Cyan

Write-Host "`n" -ForegroundColor White
Write-Host "💡 TIPS:" -ForegroundColor Magenta
Write-Host "   • Los volúmenes (-v) mantienen los datos persistentes" -ForegroundColor White
Write-Host "   • Usa --rm para auto-eliminar contenedores al terminar" -ForegroundColor White
Write-Host "   • Las gráficas se guardan en ./Graphics/" -ForegroundColor White
Write-Host "   • La BD SQLite se guarda en ./Files/etl_data.db" -ForegroundColor White