# Użyj oficjalnego obrazu Python
FROM python:3.11-slim

# Ustaw zmienne środowiskowe
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Ustaw katalog roboczy
WORKDIR /app

# Zainstaluj systemowe zależności potrzebne dla Docling
RUN apt-get update && apt-get install -y \
    build-essential \
    libpoppler-cpp-dev \
    pkg-config \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Skopiuj plik requirements.txt
COPY requirements.txt .

# Zainstaluj zależności Python
RUN pip install --no-cache-dir -r requirements.txt

# Skopiuj kod aplikacji
COPY . .

# Utwórz użytkownika nie-root dla bezpieczeństwa
RUN useradd --create-home --shell /bin/bash app && chown -R app:app /app
USER app

# Eksponuj port
EXPOSE 8000

# Uruchom aplikację
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"] 