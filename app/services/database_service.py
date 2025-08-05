"""Database service for managing file jobs and errors"""

import uuid
from datetime import datetime
from typing import Optional, List, Dict, Any
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError

from app.config import config_manager, logger
from app.models.database_models import (
    Base,
    UserFiles,
    FileJobs,
    FileJobErrors,
    FileJobStatus,
    FileJobError,
)


class DatabaseService:
    """Service for managing file jobs and errors in PostgreSQL"""

    def __init__(self):
        config = config_manager.config
        self.engine = create_engine(
            config.database.url,
            pool_size=config.database.pool_size,
            max_overflow=config.database.max_overflow,
            echo=config.database.echo,
        )
        self.SessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine
        )
        self._create_tables()

    def _create_tables(self):
        """Creates database tables if they don't exist"""
        try:
            Base.metadata.create_all(bind=self.engine)
            logger.info("Database tables created successfully")
        except Exception as e:
            logger.error(f"Error creating database tables: {e}")
            raise

    def get_session(self) -> Session:
        """Gets database session"""
        return self.SessionLocal()

    def create_file_job(
        self, user_id: str, file_id: str, status: FileJobStatus = FileJobStatus.PENDING
    ) -> Optional[str]:
        """Creates a new file job"""
        try:
            with self.get_session() as session:
                job_id = str(uuid.uuid4())
                file_job = FileJobs(
                    id=job_id, user_id=user_id, file_id=file_id, status=status
                )
                session.add(file_job)
                session.commit()
                session.refresh(file_job)

                logger.info(f"Created file job {job_id} for file {file_id}")
                return job_id
        except SQLAlchemyError as e:
            logger.error(f"Error creating file job: {e}")
            raise

    def get_file_job(self, job_id: str) -> Optional[Dict[str, Any]]:
        """Gets file job by ID"""
        try:
            with self.get_session() as session:
                file_job = session.query(FileJobs).filter(FileJobs.id == job_id).first()

                if file_job:
                    return {
                        "id": file_job.id,
                        "user_id": file_job.user_id,
                        "file_id": file_job.file_id,
                        "status": file_job.status.value,
                        "created_at": file_job.created_at,
                        "updated_at": file_job.updated_at,
                    }
                return None
        except SQLAlchemyError as e:
            logger.error(f"Error getting file job: {e}")
            raise

    def get_file_job_by_file_id(self, file_id: str) -> Optional[Dict[str, Any]]:
        """Gets file job by file ID"""
        try:
            with self.get_session() as session:
                file_job = (
                    session.query(FileJobs).filter(FileJobs.file_id == file_id).first()
                )

                if file_job:
                    return {
                        "id": file_job.id,
                        "user_id": file_job.user_id,
                        "file_id": file_job.file_id,
                        "status": file_job.status.value,
                        "created_at": file_job.created_at,
                        "updated_at": file_job.updated_at,
                    }
                return None
        except SQLAlchemyError as e:
            logger.error(f"Error getting file job by file ID: {e}")
            raise

    def update_file_job_status(self, job_id: str, status: FileJobStatus) -> bool:
        """Updates file job status"""
        try:
            with self.get_session() as session:
                file_job = session.query(FileJobs).filter(FileJobs.id == job_id).first()

                if not file_job:
                    logger.warning(f"File job not found: {job_id}")
                    return False

                file_job.status = status
                file_job.updated_at = datetime.now()
                session.commit()

                logger.info(f"Updated file job {job_id} status to {status.value}")
                return True
        except SQLAlchemyError as e:
            logger.error(f"Error updating file job status: {e}")
            raise

    def add_file_job_error(self, job_id: str, error: FileJobError) -> bool:
        """Adds error to file job"""
        try:
            with self.get_session() as session:
                error_id = str(uuid.uuid4())
                file_job_error = FileJobErrors(
                    id=error_id, file_job_id=job_id, error=error
                )
                session.add(file_job_error)
                session.commit()

                logger.info(f"Added error {error.value} to file job {job_id}")
                return True
        except SQLAlchemyError as e:
            logger.error(f"Error adding file job error: {e}")
            raise

    def get_file_jobs_to_process(self) -> List[Dict[str, Any]]:
        """Gets all file jobs with TO_PROCESS status"""
        try:
            with self.get_session() as session:
                file_jobs = (
                    session.query(FileJobs)
                    .filter(FileJobs.status == FileJobStatus.TO_PROCESS)
                    .all()
                )

                return [
                    {
                        "id": job.id,
                        "user_id": job.user_id,
                        "file_id": job.file_id,
                        "status": job.status.value,
                        "created_at": job.created_at,
                        "updated_at": job.updated_at,
                    }
                    for job in file_jobs
                ]
        except SQLAlchemyError as e:
            logger.error(f"Error getting file jobs to process: {e}")
            raise

    def get_file_job_with_file_info(self, job_id: str) -> Optional[Dict[str, Any]]:
        """Gets file job with file information"""
        try:
            with self.get_session() as session:
                file_job = (
                    session.query(FileJobs)
                    .join(UserFiles)
                    .filter(FileJobs.id == job_id)
                    .first()
                )

                if file_job:
                    return {
                        "id": file_job.id,
                        "user_id": file_job.user_id,
                        "file_id": file_job.file_id,
                        "status": file_job.status.value,
                        "created_at": file_job.created_at,
                        "updated_at": file_job.updated_at,
                        "file_url": file_job.file.file_url,
                        "file_name": file_job.file.file_name,
                        "file_type": file_job.file.file_type,
                        "file_size": file_job.file.file_size,
                    }
                return None
        except SQLAlchemyError as e:
            logger.error(f"Error getting file job with file info: {e}")
            raise

    def set_file_job_to_process(self, job_id: str) -> bool:
        """Sets file job status to TO_PROCESS"""
        return self.update_file_job_status(job_id, FileJobStatus.TO_PROCESS)

    def set_file_job_processing(self, job_id: str) -> bool:
        """Sets file job status to PROCESSING"""
        return self.update_file_job_status(job_id, FileJobStatus.PROCESSING)

    def set_file_job_processed(self, job_id: str) -> bool:
        """Sets file job status to PROCESSED"""
        return self.update_file_job_status(job_id, FileJobStatus.PROCESSED)

    def set_file_job_error(self, job_id: str, error: FileJobError) -> bool:
        """Sets file job status to ERROR and adds error record"""
        try:
            # Update status to ERROR
            success = self.update_file_job_status(job_id, FileJobStatus.ERROR)
            if success:
                # Add error record
                self.add_file_job_error(job_id, error)
            return success
        except Exception as e:
            logger.error(f"Error setting file job to error state: {e}")
            return False


# Initialize database service
database_service = DatabaseService()
