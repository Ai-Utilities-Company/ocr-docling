"""File jobs management API endpoints"""

from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from app.services.database_service import database_service, FileJobStatus, FileJobError
from app.config import logger

router = APIRouter(prefix="/file-jobs", tags=["File Jobs"])


class FileJobResponse(BaseModel):
    """File job response model"""

    id: str
    user_id: str
    file_id: str
    status: str
    created_at: datetime
    updated_at: datetime


class FileJobWithFileInfo(BaseModel):
    """File job with file information response model"""

    id: str
    user_id: str
    file_id: str
    status: str
    created_at: datetime
    updated_at: datetime
    file_url: str
    file_name: str
    file_type: str
    file_size: int


@router.get("/{job_id}", response_model=FileJobWithFileInfo)
async def get_file_job(job_id: str):
    """Gets file job with file information"""
    try:
        file_job = database_service.get_file_job_with_file_info(job_id)
        if not file_job:
            raise HTTPException(status_code=404, detail="File job not found")

        return FileJobWithFileInfo(**file_job)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting file job: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{job_id}/process")
async def set_file_job_to_process(job_id: str):
    """Sets file job status to TO_PROCESS"""
    try:
        success = database_service.set_file_job_to_process(job_id)
        if not success:
            raise HTTPException(status_code=404, detail="File job not found")

        return {
            "success": True,
            "message": f"File job {job_id} set to TO_PROCESS status",
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error setting file job to process: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=List[FileJobResponse])
async def get_file_jobs_to_process():
    """Gets all file jobs with TO_PROCESS status"""
    try:
        file_jobs = database_service.get_file_jobs_to_process()
        return [FileJobResponse(**job) for job in file_jobs]
    except Exception as e:
        logger.error(f"Error getting file jobs to process: {e}")
        raise HTTPException(status_code=500, detail=str(e))
