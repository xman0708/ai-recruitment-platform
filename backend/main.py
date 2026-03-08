from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from api.candidates import router as candidates_router
from api.jobs import router as jobs_router
from api.interviews import router as interviews_router
from api.notifications import router as notifications_router
from api.dashboard import router as dashboard_router

app = FastAPI(
    title="AI Recruitment Platform API",
    description="API for the AI-powered recruitment platform (Resume parsing, Candidate management, Interview scheduling).",
    version="1.0.0"
)

# Setup CORS for Vue frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(dashboard_router, prefix="/api/v1/dashboard", tags=["Dashboard"])
app.include_router(candidates_router, prefix="/api/v1/candidates", tags=["Candidates"])
app.include_router(jobs_router, prefix="/api/v1/jobs", tags=["Jobs"])
app.include_router(interviews_router, prefix="/api/v1/interviews", tags=["Interviews"])
app.include_router(notifications_router, prefix="/api/v1/notifications", tags=["Notifications"])

class ResumeText(BaseModel):
    text: str

@app.get("/")
def read_root():
    return {"message": "Welcome to the AI Recruitment Platform API"}

@app.get("/api/health")
def health_check():
    return {"status": "ok"}

@app.post("/api/v1/ai/test-parse", tags=["AI Testing"])
def test_ai_parse(resume: ResumeText):
    result = extract_resume_info(resume.text)
    return {"parsed_data": result}

