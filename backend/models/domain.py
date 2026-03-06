from sqlalchemy import Column, Integer, String, Text, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from database.session import Base
from datetime import datetime
import enum

class RoleEnum(str, enum.Enum):
    HR = "hr"
    MANAGER = "manager"
    ADMIN = "admin"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(Enum(RoleEnum), default=RoleEnum.HR, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    jobs = relationship("Job", back_populates="creator")


class JobStatusEnum(str, enum.Enum):
    OPEN = "open"
    CLOSED = "closed"
    DRAFT = "draft"

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    department = Column(String(100))
    description = Column(Text, nullable=False)
    requirements = Column(Text)
    status = Column(Enum(JobStatusEnum), default=JobStatusEnum.OPEN)
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    creator = relationship("User", back_populates="jobs")
    candidates = relationship("Candidate", back_populates="job")


class ProcessStatusEnum(str, enum.Enum):
    NEW = "new"
    SCREENING = "screening"
    INTERVIEW = "interview"
    OFFER = "offer"
    REJECTED = "rejected"

class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100))
    phone = Column(String(20))
    resume_url = Column(String(255)) # OSS or local path
    
    # AI Extracted Data
    education = Column(Text)
    experience = Column(Text)
    skills = Column(Text)
    
    # AI Screening results
    ai_score = Column(Integer) # 0-100
    ai_reasoning = Column(Text)
    
    status = Column(Enum(ProcessStatusEnum), default=ProcessStatusEnum.NEW)
    job_id = Column(Integer, ForeignKey("jobs.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    job = relationship("Job", back_populates="candidates")


class NotificationTypeEnum(str, enum.Enum):
    SYSTEM = "system"
    NEW_CANDIDATE = "new_candidate"
    INTERVIEW_SCHEDULED = "interview_scheduled"
    JOB_CREATED = "job_created"

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    type = Column(Enum(NotificationTypeEnum), default=NotificationTypeEnum.SYSTEM)
    title = Column(String(200), nullable=False)
    message = Column(Text, nullable=False)
    is_read = Column(Integer, default=0) # 0 for False, 1 for True
    reference_id = Column(String(50)) # e.g. job_id or candidate_id to link
    
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User")
