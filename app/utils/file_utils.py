"""File handling utilities"""

import os
import tempfile
from pathlib import Path
from typing import Tuple
from fastapi import UploadFile, HTTPException
from app.config import ALLOWED_EXTENSIONS, logger


class FileUtils:
    """File handling utilities"""

    @staticmethod
    def validate_file_type(filename: str) -> str:
        """Validates file type and returns extension"""
        file_extension = Path(filename).suffix.lower()

        if file_extension not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file type. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}",
            )

        return file_extension

    @staticmethod
    async def save_uploaded_file(file: UploadFile) -> Tuple[str, bytes]:
        """Saves uploaded file to temporary file"""
        try:
            content = await file.read()

            with tempfile.NamedTemporaryFile(
                delete=False, suffix=Path(file.filename).suffix
            ) as temp_file:
                temp_file.write(content)
                temp_file.flush()
                temp_path = temp_file.name

            return temp_path, content
        except Exception as e:
            logger.error(f"Error saving file {file.filename}: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error saving file: {str(e)}")

    @staticmethod
    def cleanup_temp_file(file_path: str):
        """Removes temporary file"""
        try:
            if os.path.exists(file_path):
                os.unlink(file_path)
        except Exception as e:
            logger.warning(f"Failed to remove temporary file {file_path}: {str(e)}")

    @staticmethod
    def get_file_metadata(filename: str, content: bytes, file_extension: str) -> dict:
        """Creates file metadata"""
        return {
            "filename": filename,
            "file_size": len(content),
            "file_type": file_extension,
        }
