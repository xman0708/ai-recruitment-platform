from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database.session import get_db
from models.domain import Interview, Candidate, Notification, NotificationTypeEnum, ProcessStatusEnum, User, RoleEnum
from schemas.interview import InterviewCreate, InterviewOut, InterviewFeedback

router = APIRouter()

@router.post("/", response_model=InterviewOut)
def schedule_interview(interview: InterviewCreate, db: Session = Depends(get_db)):
    """
    安排面试，触发系统和邮件通知并改变候选人状态
    """
    # Verify candidate exists
    candidate = db.query(Candidate).filter(Candidate.id == interview.candidate_id).first()
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
        
    # Verify interviewer exists
    interviewer = db.query(User).filter(User.id == interview.interviewer_id).first()
    if not interviewer:
        raise HTTPException(status_code=404, detail="Interviewer not found")

    new_interview = Interview(
        **interview.dict()
    )
    db.add(new_interview)
    
    # Update candidate status
    candidate.status = ProcessStatusEnum.INTERVIEW
    
    # Create notification for interviewer
    notification = Notification(
        user_id=interviewer.id,
        type=NotificationTypeEnum.INTERVIEW_SCHEDULED,
        title="新面试安排",
        message=f"您有新的面试被安排：候选人 {candidate.name} ({interview.type})",
        reference_id=str(candidate.id)
    )
    db.add(notification)
    
    db.commit()
    db.refresh(new_interview)
    return new_interview

@router.get("/", response_model=List[InterviewOut])
def get_interviews(db: Session = Depends(get_db)):
    """
    获取所有面试安排
    """
    return db.query(Interview).order_by(Interview.created_at.desc()).all()

@router.put("/{interview_id}/status", response_model=InterviewOut)
def update_interview_status(interview_id: int, feedback: InterviewFeedback, db: Session = Depends(get_db)):
    """
    更新面试状态与面评反馈
    """
    db_interview = db.query(Interview).filter(Interview.id == interview_id).first()
    if not db_interview:
        raise HTTPException(status_code=404, detail="Interview not found")
        
    update_data = feedback.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_interview, key, value)
        
    db.commit()
    db.refresh(db_interview)
    return db_interview
