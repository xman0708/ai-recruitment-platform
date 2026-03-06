from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database.session import get_db
from models.domain import Notification
from schemas.notification import NotificationOut

router = APIRouter()

@router.get("/", response_model=List[NotificationOut])
def get_notifications(user_id: int = 1, db: Session = Depends(get_db)):
    """
    Get all notifications for a specific user (mocked as user 1 for now)
    """
    notifications = db.query(Notification).filter(Notification.user_id == user_id).order_by(Notification.created_at.desc()).all()
    return notifications

@router.put("/{notification_id}/read", response_model=NotificationOut)
def mark_notification_read(notification_id: int, db: Session = Depends(get_db)):
    """
    Mark a single notification as read
    """
    notification = db.query(Notification).filter(Notification.id == notification_id).first()
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
        
    notification.is_read = 1
    db.commit()
    db.refresh(notification)
    return notification

@router.post("/mark-all-read")
def mark_all_read(user_id: int = 1, db: Session = Depends(get_db)):
    """
    Mark all unread notifications as read for a specific user
    """
    db.query(Notification).filter(
        Notification.user_id == user_id, 
        Notification.is_read == 0
    ).update({"is_read": 1})
    db.commit()
    return {"message": "All notifications marked as read"}
