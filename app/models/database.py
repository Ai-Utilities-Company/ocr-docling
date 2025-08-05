"""Database models for OCR processing status"""

from enum import Enum
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class ProcessingStatus(Enum):
    """Processing status enumeration"""

    PENDING = "PENDING"
    TO_PROCESS = "TO_PROCESS"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


class DocumentRecord(BaseModel):
    """Document record model"""

    id: Optional[int] = None
    url: str = Field(..., description="Document URL")
    filename: str = Field(..., description="Document filename")
    status: ProcessingStatus = Field(
        default=ProcessingStatus.PENDING, description="Processing status"
    )
    created_at: datetime = Field(
        default_factory=datetime.now, description="Record creation time"
    )
    updated_at: datetime = Field(
        default_factory=datetime.now, description="Record update time"
    )
    processed_at: Optional[datetime] = None
    extracted_text: Optional[str] = None
    language_detection: Optional[dict] = None
    error_message: Optional[str] = None
    file_size: Optional[int] = None
    page_count: Optional[int] = None


class StatusUpdateRequest(BaseModel):
    """Status update request model"""

    status: ProcessingStatus
    extracted_text: Optional[str] = None
    language_detection: Optional[dict] = None
    error_message: Optional[str] = None
    page_count: Optional[int] = None
