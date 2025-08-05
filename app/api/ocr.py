"""OCR API endpoints"""

from datetime import datetime
from typing import Dict, Optional
from fastapi import APIRouter, File, UploadFile, HTTPException, Query
from fastapi.responses import JSONResponse

from app.services.document_converter import DocumentConverterService
from app.services.language_detection import LanguageDetectionService
from app.utils.file_utils import FileUtils
from app.models.requests import (
    TextAnalysisRequest,
    FileUploadResponse,
    TextAnalysisResponse,
    SupportedLanguagesResponse,
)
from app.config import logger

router = APIRouter(prefix="/ocr", tags=["OCR"])

# Initialize services
document_converter_service = DocumentConverterService()
language_detection_service = LanguageDetectionService()


@router.post("/upload", response_model=FileUploadResponse)
async def upload_and_process_file(file: UploadFile = File(...)):
    """Uploads a file and performs OCR processing with language detection"""

    # Validate file type
    file_extension = FileUtils.validate_file_type(file.filename)

    # Save temporary file
    temp_file_path, content = await FileUtils.save_uploaded_file(file)

    try:
        logger.info(f"Processing file: {file.filename}")

        # Convert document
        result = document_converter_service.convert_document(temp_file_path)

        # Extract text
        extracted_text = result.document.export_to_markdown()

        # Detect language
        language_info = language_detection_service.detect_language(extracted_text)

        # Document metadata
        metadata = FileUtils.get_file_metadata(file.filename, content, file_extension)
        metadata.update(
            {
                "processed_at": datetime.now().isoformat(),
                "page_count": (
                    len(result.document.pages)
                    if hasattr(result.document, "pages")
                    else 1
                ),
            }
        )

        # Prepare response
        response_data = {
            "success": True,
            "metadata": metadata,
            "extracted_text": extracted_text,
            "language_detection": language_info,
            "text_length": len(extracted_text),
            "word_count": len(extracted_text.split()) if extracted_text else 0,
        }

        logger.info(f"Successfully processed {file.filename}")
        return JSONResponse(content=response_data)

    except Exception as e:
        logger.error(f"Error processing file {file.filename}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")
    finally:
        # Clean up temporary file
        FileUtils.cleanup_temp_file(temp_file_path)


@router.post("/process-job")
async def process_file_job(job_id: str = Query(..., description="File job ID")):
    """Processes file job (only if status is TO_PROCESS)"""
    try:
        logger.info(f"Processing file job: {job_id}")

        # Process file job (this will check status in database)
        result = document_converter_service.process_file_job(job_id)

        if result is None:
            raise HTTPException(
                status_code=400,
                detail="File job is not in TO_PROCESS status or not found in database",
            )

        # Detect language if text was extracted
        if result.get("extracted_text"):
            language_info = language_detection_service.detect_language(
                result["extracted_text"]
            )
            result["language_detection"] = language_info
            result["text_length"] = len(result["extracted_text"])
            result["word_count"] = len(result["extracted_text"].split())

        logger.info(f"Successfully processed file job: {job_id}")
        return JSONResponse(content=result)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing file job {job_id}: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Error processing file job: {str(e)}"
        )


@router.post("/text-analysis", response_model=TextAnalysisResponse)
async def analyze_text(request: TextAnalysisRequest):
    """Analyzes provided text for language detection"""

    language_info = language_detection_service.detect_language(request.text)

    return {
        "success": True,
        "text_length": len(request.text),
        "word_count": len(request.text.split()),
        "language_detection": language_info,
        "analyzed_at": datetime.now().isoformat(),
    }


@router.get("/supported-languages", response_model=SupportedLanguagesResponse)
async def get_supported_languages():
    """Returns list of supported languages for detection"""
    supported_languages = language_detection_service.get_supported_languages()

    return {
        "supported_languages": supported_languages,
        "total_languages": len(supported_languages),
    }
