"""Health check API endpoints"""

from datetime import datetime
from fastapi import APIRouter

router = APIRouter(tags=["Health"])


@router.get("/")
async def root():
    """Main application endpoint"""
    return {"message": "Docling OCR API is running"}


@router.get("/health")
async def health_check():
    """Checks application health"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "Docling OCR API",
    }
