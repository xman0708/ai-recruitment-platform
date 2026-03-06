from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from database.session import get_db
from models.domain import Job, JobStatusEnum, Notification, NotificationTypeEnum
from schemas.job import JobCreate, JobOut, JobUpdate
from datetime import datetime

router = APIRouter()

@router.post("/", response_model=JobOut)
def create_job(job: JobCreate, db: Session = Depends(get_db)):
    """
    Create a new Job Description (JD)
    """
    db_job = Job(
        title=job.title,
        department=job.department,
        description=job.description,
        requirements=job.requirements,
        status=job.status
    )
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    
    # Trigger system notification
    notification = Notification(
        user_id=1,  # Mocking sending to the main admin/HR
        type=NotificationTypeEnum.JOB_CREATED,
        title="新职位已发布",
        message=f"你成功发布了新的招聘需求：{job.title} ({job.department})",
        reference_id=str(db_job.id)
    )
    db.add(notification)
    db.commit()
    
    # Calculate mock stats for UI compatibility
    setattr(db_job, 'candidates_count', len(db_job.candidates) if db_job.candidates else 0)
    setattr(db_job, 'new_candidates_count', 0)
    
    return db_job

@router.get("/", response_model=List[JobOut])
def get_jobs(status: Optional[str] = None, db: Session = Depends(get_db)):
    """
    Get all jobs, optionally filtering by status.
    """
    query = db.query(Job)
    if status:
        try:
            enum_status = JobStatusEnum(status.lower())
            query = query.filter(Job.status == enum_status)
        except ValueError:
            pass # Ignore invalid enum fitlers 

    # Sorting newest first
    jobs = query.order_by(Job.created_at.desc()).all()
    
    # Calculate mock stats for UI compatibility (Task 3.1)
    for job in jobs:
        setattr(job, 'candidates_count', len(job.candidates) if job.candidates else 0)
        setattr(job, 'new_candidates_count', 0)
        
    return jobs

@router.get("/{job_id}", response_model=JobOut)
def get_job(job_id: int, db: Session = Depends(get_db)):
    """
    Get specific job details
    """
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
        
    setattr(job, 'candidates_count', len(job.candidates) if job.candidates else 0)
    setattr(job, 'new_candidates_count', 0)
    
    return job

@router.put("/{job_id}", response_model=JobOut)
def update_job(job_id: int, update: JobUpdate, db: Session = Depends(get_db)):
    """
    Update job information (e.g. close the job or edit details)
    """
    db_job = db.query(Job).filter(Job.id == job_id).first()
    if not db_job:
        raise HTTPException(status_code=404, detail="Job not found")

    update_data = update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_job, key, value)
        
    db.commit()
    db.refresh(db_job)
    
    setattr(db_job, 'candidates_count', len(db_job.candidates) if db_job.candidates else 0)
    setattr(db_job, 'new_candidates_count', 0)
    
    return db_job
