from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
import uuid
import datetime

router = APIRouter()

# Mock DB for Interviews
interviews_db = []

class InterviewSchedule(BaseModel):
    application_id: str
    interviewer_id: str
    scheduled_time: str
    location_or_link: str

class InterviewResponse(InterviewSchedule):
    id: str
    status: str
    feedback_score: int = None
    feedback_content: str = None

@router.post("/", response_model=InterviewResponse)
def schedule_interview(interview: InterviewSchedule):
    """
    安排面试，触发系统和邮件通知（Mock）
    """
    new_interview = InterviewResponse(
        id=str(uuid.uuid4()),
        status="SCHEDULED",
        **interview.dict()
    )
    interviews_db.append(new_interview)
    return new_interview

@router.get("/", response_model=List[InterviewResponse])
def get_interviews():
    """
    获取所有面试安排
    """
    return interviews_db

class InterviewFeedback(BaseModel):
    status: str
    feedback_score: int
    feedback_content: str

@router.put("/{interview_id}/status", response_model=InterviewResponse)
def update_interview_status(interview_id: str, feedback: InterviewFeedback):
    """
    更新面试状态与面评反馈
    """
    for idx, inv in enumerate(interviews_db):
        if inv.id == interview_id:
            inv_dict = inv.dict()
            inv_dict.update(feedback.dict())
            updated_inv = InterviewResponse(**inv_dict)
            interviews_db[idx] = updated_inv
            return updated_inv
    return None
