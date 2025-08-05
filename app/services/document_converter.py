"""Document conversion service with OCR"""

import os
import requests
import tempfile
from typing import Optional, Tuple
from pathlib import Path
from urllib.parse import urlparse
from datetime import datetime
from docling.document_converter import DocumentConverter
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.document_converter import PdfFormatOption
from app.config import logger, ALLOWED_EXTENSIONS
from app.services.database_service import database_service, FileJobStatus, FileJobError
from app.models.database_models import (
    FileJobStatus as StatusEnum,
    FileJobError as ErrorEnum,
)


class DocumentConverterService:
    """Service for document conversion with OCR"""

    def __init__(self):
        self._converter = None

    def _get_converter(self) -> DocumentConverter:
        """Initializes and configures document converter with OCR capabilities"""
        if self._converter is None:
            pipeline_options = PdfPipelineOptions()
            pipeline_options.do_ocr = True  # Enable OCR
            pipeline_options.do_table_structure = True
            pipeline_options.table_structure_options.do_cell_matching = True

            self._converter = DocumentConverter(
                format_options={
                    InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
                }
            )

        return self._converter

    def _get_file_extension_from_url(self, url: str) -> str:
        """Extracts file extension from URL"""
        parsed_url = urlparse(url)
        path = parsed_url.path
        extension = Path(path).suffix.lower()

        # If no extension in URL, try to get from Content-Type header
        if not extension or extension not in ALLOWED_EXTENSIONS:
            try:
                response = requests.head(url, timeout=10)
                content_type = response.headers.get("content-type", "").lower()

                # Map content types to extensions
                content_type_map = {
                    "application/pdf": ".pdf",
                    "image/png": ".png",
                    "image/jpeg": ".jpg",
                    "image/jpg": ".jpg",
                    "image/tiff": ".tiff",
                    "image/bmp": ".bmp",
                }

                if content_type in content_type_map:
                    extension = content_type_map[content_type]
            except:
                pass

        # Default to .pdf if no valid extension found
        if not extension or extension not in ALLOWED_EXTENSIONS:
            extension = ".pdf"

        return extension

    def _download_file_from_url(self, url: str) -> Tuple[bool, str, int]:
        """Downloads file from URL to temporary location"""
        try:
            # Create temporary file with proper extension
            extension = self._get_file_extension_from_url(url)
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=extension)
            temp_path = temp_file.name
            temp_file.close()

            # Download file with progress tracking
            response = requests.get(url, stream=True, timeout=60)
            response.raise_for_status()

            file_size = 0
            with open(temp_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        file_size += len(chunk)

            logger.info(
                f"Successfully downloaded file from {url} to {temp_path} ({file_size} bytes)"
            )
            return True, temp_path, file_size

        except Exception as e:
            logger.error(f"Error downloading file from {url}: {e}")
            return False, "", 0

    def convert_document_from_job_id(self, job_id: str) -> Optional[dict]:
        """Converts document from file job ID with status checking"""
        try:
            # Get file job with file information
            file_job = database_service.get_file_job_with_file_info(job_id)

            if not file_job:
                logger.warning(f"File job not found: {job_id}")
                return None

            if file_job["status"] != FileJobStatus.TO_PROCESS.value:
                logger.warning(
                    f"File job {job_id} is not in TO_PROCESS status. Current status: {file_job['status']}"
                )
                return None

            # Set status to PROCESSING
            if not database_service.set_file_job_processing(job_id):
                logger.error(f"Failed to set file job {job_id} to PROCESSING status")
                return None

            # Download file to temporary location
            success, temp_path, file_size = self._download_file_from_url(
                file_job["file_url"]
            )

            if not success:
                # Set status to ERROR
                database_service.set_file_job_error(job_id, ErrorEnum.DOWNLOAD_FAILED)
                return None

            try:
                # Convert document
                result = self.convert_document(temp_path)

                # Extract text
                extracted_text = result.document.export_to_markdown()
                page_count = (
                    len(result.document.pages)
                    if hasattr(result.document, "pages")
                    else 1
                )

                # Set status to PROCESSED
                if not database_service.set_file_job_processed(job_id):
                    logger.error(f"Failed to set file job {job_id} to PROCESSED status")
                    return None

                return {
                    "success": True,
                    "job_id": job_id,
                    "extracted_text": extracted_text,
                    "page_count": page_count,
                    "file_size": file_size,
                    "file_url": file_job["file_url"],
                    "file_name": file_job["file_name"],
                    "file_type": file_job["file_type"],
                }

            finally:
                # Clean up temporary file
                try:
                    if os.path.exists(temp_path):
                        os.unlink(temp_path)
                except Exception as e:
                    logger.warning(f"Failed to remove temporary file {temp_path}: {e}")

        except Exception as e:
            logger.error(f"Error processing file job {job_id}: {e}")

            # Set status to ERROR
            database_service.set_file_job_error(job_id, ErrorEnum.UNKNOWN_ERROR)

            return None

    def convert_document(self, file_path: str):
        """Converts document with OCR (for local files)"""
        try:
            converter = self._get_converter()
            result = converter.convert(file_path)
            return result
        except Exception as e:
            logger.error(f"Error during document conversion: {str(e)}")
            raise

    def process_file_job(self, job_id: str) -> Optional[dict]:
        """Processes file job (creates job if needed and processes)"""
        try:
            # Check if job exists
            file_job = database_service.get_file_job(job_id)

            if not file_job:
                logger.warning(f"File job {job_id} not found")
                return None

            # Process the file job
            return self.convert_document_from_job_id(job_id)

        except Exception as e:
            logger.error(f"Error processing file job {job_id}: {e}")
            return None
