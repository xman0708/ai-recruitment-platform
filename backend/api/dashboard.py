from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.session import get_db
from models.domain import Job, Candidate, JobStatusEnum, ProcessStatusEnum

router = APIRouter()

@router.get("/stats")
def get_dashboard_stats(db: Session = Depends(get_db)):
    """
    Get aggregated statistics for the dashboard
    """
    active_jobs_count = db.query(Job).filter(Job.status == JobStatusEnum.OPEN).count()
    new_candidates_count = db.query(Candidate).filter(Candidate.status == ProcessStatusEnum.NEW).count()
    pending_interviews_count = db.query(Candidate).filter(Candidate.status == ProcessStatusEnum.INTERVIEW).count()
    offers_count = db.query(Candidate).filter(Candidate.status == ProcessStatusEnum.OFFER).count()
    
    return {
        "active_jobs": active_jobs_count,
        "new_candidates": new_candidates_count,
        "pending_interviews": pending_interviews_count,
        "offers_this_week": offers_count # Simplified for now
    }
