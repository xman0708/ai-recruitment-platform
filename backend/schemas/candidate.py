from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from models.domain import ProcessStatusEnum

class CandidateBase(BaseModel):
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    resume_url: Optional[str] = None
    education: Optional[str] = None
    experience: Optional[str] = None
    skills: Optional[str] = None
    job_id: Optional[int] = None

class CandidateCreate(CandidateBase):
    pass

class CandidateOut(CandidateBase):
    id: int
    ai_score: Optional[int] = None
    ai_reasoning: Optional[str] = None
    status: ProcessStatusEnum
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class CandidateUpdate(BaseModel):
    status: Optional[ProcessStatusEnum] = None
    job_id: Optional[int] = None
    ai_score: Optional[int] = None
    ai_reasoning: Optional[str] = None
