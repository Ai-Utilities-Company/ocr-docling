# OCR Docling API

API for OCR processing and language detection using Docling library with PostgreSQL database integration.

## 🚀 Quick Start

### Option 1: Python (recommended)
```bash
# Development (default)
python start.py

# Staging
ENVIRONMENT=staging python start.py

# Production
ENVIRONMENT=production python start.py

# Custom port
PORT=9000 python start.py
```

### Option 2: Docker
```bash
# Development (default)
python run.py

# Staging
ENVIRONMENT=staging python run.py

# Production
ENVIRONMENT=production python run.py

# Custom port
PORT=9000 python run.py
```

### Option 3: Management script
```bash
# Start with Python
python manage.py start-python

# Start with Docker
python manage.py start

# Stop application
python manage.py stop

# View logs
python manage.py logs

# With custom parameters
python manage.py start --env staging --port 9000 --debug true
```

## 📋 Requirements

- Python 3.11+
- PostgreSQL database
- Docker (optional, only for containerized deployment)

## 🌐 API Access

After starting, the application will be available at:
- **API**: http://localhost:8000 (or port from configuration)
- **Documentation**: http://localhost:8000/docs
- **Health check**: http://localhost:8000/health

## 📄 File Job Processing Workflow

The application now uses PostgreSQL database with file jobs workflow:

### 1. File Job Statuses
- `PENDING` - Job created
- `TO_PROCESS` - Ready for processing
- `PROCESSING` - Currently being processed
- `PROCESSED` - Successfully processed
- `ERROR` - Processing failed
- `CANCELLED` - Cancelled

### 2. File Job Management
```bash
# Get file job details
python manage_file_jobs.py get --job-id "your-job-id"

# Set job to process
python manage_file_jobs.py set-to-process --job-id "your-job-id"

# Process job
python manage_file_jobs.py process --job-id "your-job-id"

# List jobs to process
python manage_file_jobs.py list
```

### 3. Database Schema
The application uses the following PostgreSQL tables:
- `user` - User accounts
- `user_files` - User uploaded files
- `file_jobs` - File processing jobs
- `file_job_errors` - Error records for failed jobs

## ⚙️ Configuration

The application uses a Python configuration system with three predefined environments:

### Environments

| Environment | Debug | Log Level | CORS Origins | Max File Size | Timeout |
|-------------|-------|-----------|--------------|---------------|---------|
| **Development** | ✅ | DEBUG | localhost:* | 50MB | 5 min |
| **Staging** | ❌ | INFO | staging.* | 100MB | 10 min |
| **Production** | ❌ | WARNING | production.* | 200MB | 15 min |

### Environment Variables (optional)

You can override default settings:

```bash
# Database
DATABASE_URL=postgresql://user:pass@host:port/db
DB_POOL_SIZE=10
DB_MAX_OVERFLOW=20
DB_ECHO=true

# Server
HOST=0.0.0.0
PORT=8000
DEBUG=true
LOG_LEVEL=INFO

# CORS
CORS_ORIGINS=http://localhost:3000,https://myapp.com

# File processing
MAX_FILE_SIZE=104857600
PROCESSING_TIMEOUT=300
```

## Project Structure

```
ocr-docling/
├── app/
│   ├── __init__.py
│   ├── main.py                 # Główna aplikacja FastAPI
│   ├── config.py               # Konfiguracja aplikacji
│   ├── api/                    # Endpointy API
│   │   ├── __init__.py
│   │   ├── health.py          # Endpointy sprawdzania stanu
│   │   └── ocr.py             # Endpointy OCR
│   ├── services/               # Warstwa biznesowa
│   │   ├── __init__.py
│   │   ├── document_converter.py  # Serwis konwersji dokumentów
│   │   └── language_detection.py  # Serwis wykrywania języka
│   ├── models/                 # Modele Pydantic
│   │   ├── __init__.py
│   │   └── requests.py         # Modele żądań i odpowiedzi
│   └── utils/                  # Narzędzia pomocnicze
│       ├── __init__.py
│       └── file_utils.py       # Narzędzia do obsługi plików
├── main.py                     # Punkt wejścia aplikacji
├── Dockerfile                  # Konfiguracja Docker
├── docker-compose.yml          # Konfiguracja Docker Compose
├── run.sh                      # Skrypt uruchamiania
├── requirements.txt
└── README.md
```

##  Endpointy API

### Health Check
- `GET /` - Główny endpoint
- `GET /health` - Sprawdzenie stanu aplikacji

### OCR
- `POST /ocr/upload` - Przesłanie i przetworzenie pliku
- `POST /ocr/text-analysis` - Analiza tekstu
- `GET /ocr/supported-languages` - Lista obsługiwanych języków

## 📝 Przykład użycia z frontendu

```javascript
<code_block_to_apply_changes_from>
```

## 🔧 Konfiguracja

### Zmienne środowiskowe
- `CORS_ORIGINS` - Lista dozwolonych originów CORS (domyślnie: localhost:3000,2137,5173)

### Obsługiwane formaty plików
- PDF (.pdf)
- Obrazy (.png, .jpg, .jpeg, .tiff, .bmp)

## 🐛 Rozwiązywanie problemów

### Sprawdź logi
```bash
docker-compose logs -f ocr-api
```

### Restart aplikacji
```bash
docker-compose restart ocr-api
```

### Sprawdź status
```bash
curl http://localhost:8000/health
```

##  Integracja z frontendem

Szczegółowe instrukcje integracji znajdują się w pliku `FRONTEND_INTEGRATION.md`.
```

Doskonale! Udało mi się zdockerizować aplikację OCR Docling API. Oto podsumowanie utworzonych plików:

## ✅ Pliki Docker utworzone:

### 1. **Dockerfile**
- Oparty na Python 3.11-slim
- Instaluje zależności systemowe potrzebne dla Docling
- Używa użytkownika nie-root dla bezpieczeństwa
- Eksponuje port 8000

### 2. **docker-compose.yml**
- Konfiguracja serwisu OCR API
- Mapowanie portów 8000:8000
- Zmienne środowiskowe dla CORS
- Health check dla monitorowania

### 3. **.dockerignore**
- Ignoruje niepotrzebne pliki podczas budowania
- Optymalizuje rozmiar obrazu Docker

### 4. **run.sh**
- Skrypt do automatycznego uruchamiania
- Sprawdza wymagania (Docker, docker-compose)
- Weryfikuje status aplikacji

### 5. **FRONTEND_INTEGRATION.md**
- Przykłady integracji z frontendem
- Kod JavaScript/React
- Instrukcje użycia API

##  Główne korzyści:

1. **Łatwe uruchomienie** - jeden skrypt `./run.sh`
2. **Izolacja środowiska** - wszystko w kontenerze Docker
3. **Elastyczna konfiguracja CORS** - przez zmienne środowiskowe
4. **Gotowe przykłady** - dla integracji z frontendem
5. **Monitoring** - health check i logi

## 🚀 Jak uruchomić:

```bash
# Automatyczne uruchomienie
chmod +x run.sh
./run.sh

# Lub ręcznie
docker-compose up --build -d
```

Aplikacja będzie dostępna pod adresem `http://localhost:8000` i gotowa do przyjmowania plików z frontendu! 