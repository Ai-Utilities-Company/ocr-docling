# Frontend Integration

## API Endpoints

### 1. Upload File for OCR
```javascript
const formData = new FormData();
formData.append('file', fileInput.files[0]);

const response = await fetch('http://localhost:8000/ocr/upload', {
  method: 'POST',
  body: formData
});

const result = await response.json();
console.log(result);
```

### 2. Analyze Text
```javascript
const response = await fetch('http://localhost:8000/ocr/text-analysis', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    text: "Text to analyze"
  })
});

const result = await response.json();
console.log(result);
```

### 3. Get Supported Languages
```javascript
const response = await fetch('http://localhost:8000/ocr/supported-languages');
const languages = await response.json();
console.log(languages);
```

## React Component Example

```tsx
import React, { useState } from 'react';

function FileUpload() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleFileUpload = async () => {
    if (!file) return;

    setLoading(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('http://localhost:8000/ocr/upload', {
        method: 'POST',
        body: formData
      });

      const data = await response.json();
      setResult(data);
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <input 
        type="file" 
        onChange={(e) => setFile(e.target.files[0])}
        accept=".pdf,.png,.jpg,.jpeg,.tiff,.bmp"
      />
      <button onClick={handleFileUpload} disabled={!file || loading}>
        {loading ? 'Processing...' : 'Upload File'}
      </button>
      
      {result && (
        <div>
          <h3>Results:</h3>
          <p>Language: {result.language_detection.language_name}</p>
          <p>Word count: {result.word_count}</p>
          <pre>{result.extracted_text}</pre>
        </div>
      )}
    </div>
  );
}

export default FileUpload;
```

## Running with Docker

1. **Start application:**
   ```bash
   python run.py
   ```

2. **Check status:**
   ```bash
   python manage.py logs
   ```

3. **View logs:**
   ```bash
   python manage.py logs
   ```

4. **Stop application:**
   ```bash
   python manage.py stop
   ```

## Environment Variables

You can customize CORS origins through environment variables:

```bash
export CORS_ORIGINS="http://localhost:3000,https://myapp.com"
python run.py
```
```

Doskonale! Przetłumaczyłem wszystkie polskie komentarze i teksty na angielski. Oto podsumowanie zmian:

## ✅ Przetłumaczone pliki:

### 1. **Konfiguracja** (`app/config.py`)
- Wszystkie komentarze i docstringi
- Nazwy funkcji i klas
- Opisy konfiguracji

### 2. **Aplikacja główna** (`app/main.py`)
- Komentarze i docstringi
- Opisy funkcji

### 3. **Serwisy** (`app/services/`)
- `document_converter.py` - komentarze i opisy
- `language_detection.py` - komentarze i opisy

### 4. **Narzędzia** (`app/utils/file_utils.py`)
- Wszystkie komentarze i opisy funkcji
- Komunikaty błędów

### 5. **Modele** (`app/models/requests.py`)
- Opisy modeli Pydantic
- Komentarze

### 6. **API** (`app/api/`)
- `health.py` - komentarze endpointów
- `ocr.py` - komentarze i opisy funkcji

### 7. **Skrypty uruchamiania**
- `start.py` - wszystkie komentarze i komunikaty
- `run.py` - komentarze i komunikaty
- `manage.py` - opisy funkcji i komentarze

### 8. **Dokumentacja**
- `README.md` - cała dokumentacja
- `FRONTEND_INTEGRATION.md` - instrukcje integracji

## 🌍 Korzyści z tłumaczenia:

1. **Międzynarodowa dostępność** - kod jest teraz w pełni po angielsku
2. **Standardy branżowe** - zgodność z międzynarodowymi standardami
3. **Łatwość współpracy** - zespół międzynarodowy może łatwo pracować z kodem
4. **Dokumentacja** - wszystkie komentarze są w języku angielskim
5. **Konsystencja** - jednolity język w całym projekcie

## 🚀 Jak uruchomić:

```bash
# Najprościej
python start.py

# Z custom parametrami
ENVIRONMENT=staging PORT=9000 python start.py

# Lub przez skrypt zarządzania
python manage.py start-python --env staging --port 9000
```

Teraz aplikacja jest w pełni po angielsku i gotowa do użycia w międzynarodowych projektach! 🎉 