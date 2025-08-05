"""Document management API endpoints"""

from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from app.services.database_service import database_service, ProcessingStatus
from app.models.database import DocumentRecord, StatusUpdateRequest
from app.config import logger

router = APIRouter(prefix="/documents", tags=["Documents"])


class CreateDocumentRequest(BaseModel):
    """Create document request model"""

    url: str
    filename: str


class DocumentResponse(BaseModel):
    """Document response model"""

    id: int
    url: str
    filename: str
    status: ProcessingStatus
    created_at: datetime
    updated_at: datetime
    processed_at: Optional[datetime] = None
    extracted_text: Optional[str] = None
    language_detection: Optional[dict] = None
    error_message: Optional[str] = None
    file_size: Optional[int] = None
    page_count: Optional[int] = None


@router.post("/", response_model=DocumentResponse)
async def create_document(request: CreateDocumentRequest):
    """Creates a new document record"""
    try:
        document = database_service.create_document_record(
            request.url, request.filename
        )
        return DocumentResponse(
            id=document.id,
            url=document.url,
            filename=document.filename,
            status=document.status,
            created_at=document.created_at,
            updated_at=document.updated_at,
        )
    except Exception as e:
        logger.error(f"Error creating document: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{url:path}", response_model=DocumentResponse)
async def get_document(url: str):
    """Gets document record by URL"""
    try:
        document = database_service.get_document_by_url(url)
        if not document:
            raise HTTPException(status_code=404, detail="Document not found")

        return DocumentResponse(
            id=document.id,
            url=document.url,
            filename=document.filename,
            status=document.status,
            created_at=document.created_at,
            updated_at=document.updated_at,
            processed_at=document.processed_at,
            extracted_text=document.extracted_text,
            language_detection=document.language_detection,
            error_message=document.error_message,
            file_size=document.file_size,
            page_count=document.page_count,
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting document: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{url:path}/status")
async def update_document_status(url: str, status_update: StatusUpdateRequest):
    """Updates document processing status"""
    try:
        success = database_service.update_document_status(url, status_update)
        if not success:
            raise HTTPException(status_code=404, detail="Document not found")

        return {"success": True, "message": f"Status updated to {status_update.status}"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating document status: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{url:path}/process")
async def set_document_to_process(url: str):
    """Sets document status to TO_PROCESS"""
    try:
        success = database_service.set_document_to_process(url)
        if not success:
            raise HTTPException(status_code=404, detail="Document not found")

        return {"success": True, "message": "Document set to TO_PROCESS status"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error setting document to process: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=List[DocumentResponse])
async def get_documents_to_process():
    """Gets all documents with TO_PROCESS status"""
    try:
        documents = database_service.get_documents_to_process()
        return [
            DocumentResponse(
                id=doc.id,
                url=doc.url,
                filename=doc.filename,
                status=doc.status,
                created_at=doc.created_at,
                updated_at=doc.updated_at,
            )
            for doc in documents
        ]
    except Exception as e:
        logger.error(f"Error getting documents to process: {e}")
        raise HTTPException(status_code=500, detail=str(e))
