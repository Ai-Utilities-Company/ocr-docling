#!/bin/bash

# Skrypt do uruchamiania aplikacji OCR Docling API

echo "🚀 Uruchamianie OCR Docling API..."

# Sprawdź czy Docker jest zainstalowany
if ! command -v docker &> /dev/null; then
    echo "❌ Docker nie jest zainstalowany. Zainstaluj Docker i spróbuj ponownie."
    exit 1
fi

# Sprawdź czy docker-compose jest zainstalowany
if ! command -v docker-compose &> /dev/null; then
    echo "❌ docker-compose nie jest zainstalowany. Zainstaluj docker-compose i spróbuj ponownie."
    exit 1
fi

# Sprawdź czy plik .env istnieje, jeśli nie, skopiuj z przykładu
if [ ! -f .env ]; then
    echo "📝 Tworzenie pliku .env z przykładu..."
    cp .env.example .env
fi

# Załaduj zmienne środowiskowe
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# Wyświetl konfigurację
echo "📋 Konfiguracja:"
echo "   Port: ${PORT:-8000}"
echo "   CORS Origins: ${CORS_ORIGINS:-http://localhost:3000,http://localhost:2137,http://localhost:5173}"
echo "   Environment: ${ENVIRONMENT:-development}"
echo "   Debug: ${DEBUG:-false}"

# Zbuduj i uruchom kontenery
echo "📦 Budowanie i uruchamianie kontenerów..."
docker-compose up --build -d

# Sprawdź status
echo "⏳ Sprawdzanie statusu aplikacji..."
sleep 5

# Sprawdź czy aplikacja działa
if curl -f http://localhost:${PORT:-8000}/health &> /dev/null; then
    echo "✅ Aplikacja OCR Docling API jest uruchomiona!"
    echo " Dostępna pod adresem: http://localhost:${PORT:-8000}"
    echo "📚 Dokumentacja API: http://localhost:${PORT:-8000}/docs"
    echo " Health check: http://localhost:${PORT:-8000}/health"
    echo ""
    echo "Aby zatrzymać aplikację, uruchom: docker-compose down"
    echo "Aby zobaczyć logi: docker-compose logs -f"
else
    echo "❌ Aplikacja nie odpowiada. Sprawdź logi: docker-compose logs"
fi 