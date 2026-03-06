from fastapi import APIRouter, UploadFile, File, BackgroundTasks, HTTPException
from sqlalchemy.orm import Session
from fastapi import Depends
from database.session import get_db
import os
import shutil
from datetime import datetime
import uuid

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload")
async def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # Validate extension
    allowed_extensions = {".pdf", ".doc", ".docx", ".txt"}
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in allowed_extensions:
        raise HTTPException(status_code=400, detail="File type not supported")
    
    # Save file locally
    # Generating unique string to avoid colisions
    unique_filename = f"{uuid.uuid4()}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)
    
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
    # Extract text and run AI extraction
    from ai.document_parser import extract_text_from_file
    from ai.extractor import extract_resume_info
    
    raw_text = extract_text_from_file(file_path)
    if not raw_text:
        raise HTTPException(status_code=422, detail="Failed to extract text from document.")
        
    ai_parsed_data = extract_resume_info(raw_text)
    
    # Save to database
    from models.domain import Candidate, ProcessStatusEnum
    
    # Extract mapped data from AI result (assuming a specific structure, if fails defaults to string)
    # The current extractor returns a dict. We'll extract basic fields safely
    name = ai_parsed_data.get("name", "Unknown")
    email = ai_parsed_data.get("email", "")
    phone = ai_parsed_data.get("phone", "")
    education = str(ai_parsed_data.get("education", ""))
    experience = str(ai_parsed_data.get("experience", ""))
    skills_list = ai_parsed_data.get("skills", [])
    skills = ", ".join(skills_list) if isinstance(skills_list, list) else str(skills_list)
    
    db_candidate = Candidate(
        name=name,
        email=email,
        phone=phone,
        resume_url=file_path,
        education=education,
        experience=experience,
        skills=skills,
        status=ProcessStatusEnum.NEW
    )
    db.add(db_candidate)
    db.commit()
    db.refresh(db_candidate)
    
    return {
        "message": "File parsed and saved successfully",
        "file_name": file.filename,
        "candidate_id": db_candidate.id,
        "parsed_data": ai_parsed_data
    }

@router.get("/", response_model=list)
def get_candidates(job_id: int = None, db: Session = Depends(get_db)):
    """
    Get all candidates, optionally filtering by job_id.
    """
    from models.domain import Candidate
    query = db.query(Candidate)
    if job_id:
        query = query.filter(Candidate.job_id == job_id)
        
    candidates = query.order_by(Candidate.created_at.desc()).all()
    # Pydantic serialization will be handled by response_model if we add it, or returning raw dicts/objects works in FastAPI directly
    return candidates

@router.get("/{candidate_id}")
def get_candidate(candidate_id: int, db: Session = Depends(get_db)):
    """
    Get specific candidate details
    """
    from models.domain import Candidate
    candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
        
    return candidate
