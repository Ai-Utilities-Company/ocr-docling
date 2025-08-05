"""Pydantic models for API requests"""

from pydantic import BaseModel, Field
from typing import Optional


class TextAnalysisRequest(BaseModel):
    """Text analysis request model"""

    text: str = Field(..., description="Text to analyze", min_length=1)


class FileUploadResponse(BaseModel):
    """File upload response model"""

    success: bool
    metadata: dict
    extracted_text: str
    language_detection: dict
    text_length: int
    word_count: int


class TextAnalysisResponse(BaseModel):
    """Text analysis response model"""

    success: bool
    text_length: int
    word_count: int
    language_detection: dict
    analyzed_at: str


class SupportedLanguagesResponse(BaseModel):
    """Supported languages response model"""

    supported_languages: dict
    total_languages: int
