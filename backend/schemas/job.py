from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from models.domain import JobStatusEnum

class JobBase(BaseModel):
    title: str = Field(..., description="The title of the job")
    department: Optional[str] = Field(None, description="Department this job belongs to")
    description: str = Field(..., description="Job responsibilities and details")
    requirements: Optional[str] = Field(None, description="Job requirements")
    status: JobStatusEnum = Field(default=JobStatusEnum.OPEN)

class JobCreate(JobBase):
    pass

class JobUpdate(BaseModel):
    title: Optional[str] = None
    department: Optional[str] = None
    description: Optional[str] = None
    requirements: Optional[str] = None
    status: Optional[JobStatusEnum] = None

from pydantic import ConfigDict

class JobOut(JobBase):
    id: int
    created_by: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    
    # We might add computed fields like candidates count here later
    candidates_count: Optional[int] = 0
    new_candidates_count: Optional[int] = 0

    model_config = ConfigDict(from_attributes=True)
