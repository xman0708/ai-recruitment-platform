from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional
from models.domain import NotificationTypeEnum

class NotificationBase(BaseModel):
    title: str
    message: str
    type: NotificationTypeEnum
    reference_id: Optional[str] = None
    
class NotificationCreate(NotificationBase):
    user_id: int

class NotificationOut(NotificationBase):
    id: int
    user_id: int
    is_read: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
