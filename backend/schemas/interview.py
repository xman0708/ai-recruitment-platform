from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from models.domain import InterviewStatusEnum

class InterviewBase(BaseModel):
    candidate_id: int
    interviewer_id: int
    type: str
    scheduled_time: str
    location_or_link: Optional[str] = None

class InterviewCreate(InterviewBase):
    pass

class InterviewFeedback(BaseModel):
    status: InterviewStatusEnum
    feedback_score: Optional[int] = None
    feedback_content: Optional[str] = None
    recommendation: Optional[str] = None

class InterviewOut(InterviewBase):
    id: int
    status: InterviewStatusEnum
    feedback_score: Optional[int] = None
    feedback_content: Optional[str] = None
    recommendation: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
