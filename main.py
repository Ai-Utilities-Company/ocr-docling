from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from pathlib import Path
import tempfile
import os
from typing import List, Dict, Any
import json
from datetime import datetime
import logging

# Docling imports
from docling.document_converter import DocumentConverter
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.document_converter import PdfFormatOption

# Language detection
from langdetect import detect, DetectorFactory
from langdetect.lang_detect_exception import LangDetectException

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Ensure consistent language detection results
DetectorFactory.seed = 0

app = FastAPI(
    title="Docling OCR API",
    description="API for OCR processing and language detection using Docling",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize document converter with OCR pipeline
def get_document_converter():
    """Initialize and configure the document converter with OCR capabilities"""
    pipeline_options = PdfPipelineOptions()
    pipeline_options.do_ocr = True  # Enable OCR
    pipeline_options.do_table_structure = True
    pipeline_options.table_structure_options.do_cell_matching = True
    
    doc_converter = DocumentConverter(
        format_options={
            InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
        }
    )
    return doc_converter

# Language code mapping
LANGUAGE_NAMES = {
    'af': 'Afrikaans', 'ar': 'Arabic', 'bg': 'Bulgarian', 'bn': 'Bengali',
    'ca': 'Catalan', 'cs': 'Czech', 'cy': 'Welsh', 'da': 'Danish',
    'de': 'German', 'el': 'Greek', 'en': 'English', 'es': 'Spanish',
    'et': 'Estonian', 'fa': 'Persian', 'fi': 'Finnish', 'fr': 'French',
    'gu': 'Gujarati', 'he': 'Hebrew', 'hi': 'Hindi', 'hr': 'Croatian',
    'hu': 'Hungarian', 'id': 'Indonesian', 'it': 'Italian', 'ja': 'Japanese',
    'kn': 'Kannada', 'ko': 'Korean', 'lt': 'Lithuanian', 'lv': 'Latvian',
    'mk': 'Macedonian', 'ml': 'Malayalam', 'mr': 'Marathi', 'ne': 'Nepali',
    'nl': 'Dutch', 'no': 'Norwegian', 'pa': 'Punjabi', 'pl': 'Polish',
    'pt': 'Portuguese', 'ro': 'Romanian', 'ru': 'Russian', 'sk': 'Slovak',
    'sl': 'Slovenian', 'so': 'Somali', 'sq': 'Albanian', 'sv': 'Swedish',
    'sw': 'Swahili', 'ta': 'Tamil', 'te': 'Telugu', 'th': 'Thai',
    'tl': 'Tagalog', 'tr': 'Turkish', 'uk': 'Ukrainian', 'ur': 'Urdu',
    'vi': 'Vietnamese', 'zh-cn': 'Chinese (Simplified)', 'zh-tw': 'Chinese (Traditional)'
}

def detect_language(text: str) -> Dict[str, Any]:
    """Detect language of the given text"""
    try:
        if not text or len(text.strip()) < 3:
            return {
                "language_code": "unknown",
                "language_name": "Unknown",
                "confidence": 0.0
            }
        
        detected_lang = detect(text)
        language_name = LANGUAGE_NAMES.get(detected_lang, detected_lang.upper())
        
        return {
            "language_code": detected_lang,
            "language_name": language_name,
            "confidence": 0.99  # langdetect doesn't provide confidence scores
        }
    except LangDetectException:
        return {
            "language_code": "unknown",
            "language_name": "Unknown",
            "confidence": 0.0
        }

@app.get("/")
async def root():
    return {"message": "Docling OCR API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.post("/ocr/upload")
async def upload_and_process_file(file: UploadFile = File(...)):
    """Upload a file and perform OCR processing with language detection"""
    
    # Validate file type
    allowed_extensions = {'.pdf', '.png', '.jpg', '.jpeg', '.tiff', '.bmp'}
    file_extension = Path(file.filename).suffix.lower()
    
    if file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type. Allowed types: {', '.join(allowed_extensions)}"
        )
    
    # Create temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as temp_file:
        try:
            # Save uploaded file
            content = await file.read()
            temp_file.write(content)
            temp_file.flush()
            
            logger.info(f"Processing file: {file.filename}")
            
            # Initialize converter
            converter = get_document_converter()
            
            # Convert document
            result = converter.convert(temp_file.name)
            
            # Extract text content
            extracted_text = result.document.export_to_markdown()
            
            # Detect language
            language_info = detect_language(extracted_text)
            
            # Get document metadata
            metadata = {
                "filename": file.filename,
                "file_size": len(content),
                "file_type": file_extension,
                "processed_at": datetime.now().isoformat(),
                "page_count": len(result.document.pages) if hasattr(result.document, 'pages') else 1
            }
            
            # Prepare response
            response_data = {
                "success": True,
                "metadata": metadata,
                "extracted_text": extracted_text,
                "language_detection": language_info,
                "text_length": len(extracted_text),
                "word_count": len(extracted_text.split()) if extracted_text else 0
            }
            
            logger.info(f"Successfully processed {file.filename}")
            return JSONResponse(content=response_data)
            
        except Exception as e:
            logger.error(f"Error processing file {file.filename}: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Error processing file: {str(e)}"
            )
        finally:
            # Clean up temporary file
            try:
                os.unlink(temp_file.name)
            except:
                pass

@app.post("/ocr/text-analysis")
async def analyze_text(data: Dict[str, str]):
    """Analyze provided text for language detection"""
    text = data.get("text", "")
    
    if not text:
        raise HTTPException(status_code=400, detail="No text provided")
    
    language_info = detect_language(text)
    
    return {
        "success": True,
        "text_length": len(text),
        "word_count": len(text.split()),
        "language_detection": language_info,
        "analyzed_at": datetime.now().isoformat()
    }

@app.get("/supported-languages")
async def get_supported_languages():
    """Get list of supported languages for detection"""
    return {
        "supported_languages": LANGUAGE_NAMES,
        "total_languages": len(LANGUAGE_NAMES)
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )