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
    
    return {
        "message": "File parsed successfully",
        "file_name": file.filename,
        "saved_path": file_path,
        "parsed_data": ai_parsed_data
    }
