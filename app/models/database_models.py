"""SQLAlchemy database models for PostgreSQL"""

from datetime import datetime
from typing import Optional
from enum import Enum
from sqlalchemy import (
    create_engine,
    Column,
    String,
    Integer,
    DateTime,
    Text,
    Enum as SQLEnum,
    ForeignKey,
    Boolean,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.dialects.postgresql import UUID
import uuid

Base = declarative_base()


class User(Base):
    """User table model"""

    __tablename__ = "user"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    email_verified = Column(Boolean, default=False, nullable=False)
    image = Column(String)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.now, onupdate=datetime.now, nullable=False
    )


class Session(Base):
    """Session table model"""

    __tablename__ = "session"

    id = Column(String, primary_key=True)
    expires_at = Column(DateTime, nullable=False)
    token = Column(String, nullable=False, unique=True)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    ip_address = Column(String)
    user_agent = Column(String)
    user_id = Column(String, ForeignKey("user.id", ondelete="cascade"), nullable=False)


class Account(Base):
    """Account table model"""

    __tablename__ = "account"

    id = Column(String, primary_key=True)
    account_id = Column(String, nullable=False)
    provider_id = Column(String, nullable=False)
    user_id = Column(String, ForeignKey("user.id", ondelete="cascade"), nullable=False)
    access_token = Column(String)
    refresh_token = Column(String)
    id_token = Column(String)
    access_token_expires_at = Column(DateTime)
    refresh_token_expires_at = Column(DateTime)
    scope = Column(String)
    password = Column(String)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)


class Verification(Base):
    """Verification table model"""

    __tablename__ = "verification"

    id = Column(String, primary_key=True)
    identifier = Column(String, nullable=False)
    value = Column(String, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)


class UserFiles(Base):
    """User files table model"""

    __tablename__ = "user_files"

    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("user.id", ondelete="cascade"), nullable=False)
    file_id = Column(String, nullable=False)
    file_url = Column(String, nullable=False)
    file_name = Column(String, nullable=False)
    file_type = Column(String, nullable=False)
    file_size = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.now, onupdate=datetime.now, nullable=False
    )

    # Relationships
    user = relationship("User", backref="files")
    file_jobs = relationship("FileJobs", back_populates="file")


class FileJobStatus(Enum):
    """File job status enum values"""

    PENDING = "PENDING"
    TO_PROCESS = "TO_PROCESS"
    PROCESSING = "PROCESSING"
    PROCESSED = "PROCESSED"
    ERROR = "ERROR"
    CANCELLED = "CANCELLED"


class FileJobError(Enum):
    """File job error enum values"""

    DOWNLOAD_FAILED = "DOWNLOAD_FAILED"
    CONVERSION_FAILED = "CONVERSION_FAILED"
    OCR_FAILED = "OCR_FAILED"
    TIMEOUT = "TIMEOUT"
    INVALID_FILE = "INVALID_FILE"
    UNKNOWN_ERROR = "UNKNOWN_ERROR"


class FileJobs(Base):
    """File jobs table model"""

    __tablename__ = "file_jobs"

    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("user.id", ondelete="cascade"), nullable=False)
    file_id = Column(
        String, ForeignKey("user_files.id", ondelete="cascade"), nullable=False
    )
    status = Column(SQLEnum(FileJobStatus), nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.now, onupdate=datetime.now, nullable=False
    )

    # Relationships
    user = relationship("User", backref="file_jobs")
    file = relationship("UserFiles", back_populates="file_jobs")
    errors = relationship(
        "FileJobErrors", back_populates="file_job", cascade="all, delete-orphan"
    )


class FileJobErrors(Base):
    """File job errors table model"""

    __tablename__ = "file_job_errors"

    id = Column(String, primary_key=True)
    file_job_id = Column(
        String, ForeignKey("file_jobs.id", ondelete="cascade"), nullable=False
    )
    error = Column(SQLEnum(FileJobError), nullable=False)

    # Relationships
    file_job = relationship("FileJobs", back_populates="errors")
